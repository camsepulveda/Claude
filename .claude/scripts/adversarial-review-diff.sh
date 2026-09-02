#!/usr/bin/env bash
# Collect a scoped diff for the /adversarial-review command.
#
# Usage: adversarial-review-diff.sh [target] [-- <path>...]
#
# target:
#   (omitted)      staged changes if any, else working-tree changes, else the
#                  current branch against its merge-base with the default branch
#   staged         staged changes only
#   worktree       unstaged changes plus untracked files
#   head           the most recent commit
#   branch         current branch vs merge-base with the repo's default branch
#   branch:<base>  current branch vs merge-base with <base>
#   <commit>       that single commit
#   <a>..<b>       an explicit revision range
#   <path>         a file or directory: auto target, limited to that path
#
# Environment:
#   REVIEW_CONTEXT  lines of context per hunk (default 8)
#
# Writes the full patch to a temp file and prints a summary plus its path.

set -euo pipefail

target=""
paths=()
while [ $# -gt 0 ]; do
  case "$1" in
    --) shift; paths+=("$@"); break ;;
    -h|--help) sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) if [ -z "$target" ]; then target="$1"; else paths+=("$1"); fi; shift ;;
  esac
done

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "adversarial-review: not inside a git repository" >&2
  exit 1
fi
cd "$(git rev-parse --show-toplevel)"

# -U<n> implies --patch, so it belongs only on the full-patch pass, never on --stat.
DIFF_OPTS=(--no-color -M)
PATCH_OPTS=(--patch "-U${REVIEW_CONTEXT:-8}")

default_base() {
  local ref candidate
  ref=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)
  if [ -n "$ref" ]; then echo "${ref#refs/remotes/}"; return 0; fi
  for candidate in origin/main origin/master main master; do
    if git rev-parse --verify --quiet "$candidate" >/dev/null 2>&1; then
      echo "$candidate"; return 0
    fi
  done
  return 1
}

set_branch_mode() {
  local base="$1"
  if [ -z "$base" ]; then
    echo "adversarial-review: cannot determine a default base branch; use branch:<base>" >&2
    exit 1
  fi
  if ! git rev-parse --verify --quiet "$base" >/dev/null 2>&1; then
    echo "adversarial-review: base '$base' does not exist" >&2
    exit 1
  fi
  mode=branch
  rev="${base}...HEAD"
  label="branch vs merge-base with ${base}"
}

mode=""
rev=""
label=""
case "$target" in
  staged|--staged|cached) mode=staged; label="staged changes" ;;
  worktree|--worktree|unstaged|working) mode=worktree; label="working tree (unstaged + untracked)" ;;
  head|HEAD) mode=commit; rev=HEAD; label="most recent commit" ;;
  branch|--branch) set_branch_mode "$(default_base || true)" ;;
  branch:*) set_branch_mode "${target#branch:}" ;;
  *..*) mode=range; rev="$target"; label="range $target" ;;
  "") : ;;
  *)
    if git rev-parse --verify --quiet "${target}^{commit}" >/dev/null 2>&1; then
      mode=commit; rev="$target"; label="commit $target"
    elif [ -e "$target" ]; then
      paths=("$target" ${paths[@]+"${paths[@]}"})
    else
      echo "adversarial-review: '$target' is neither a known revision nor an existing path" >&2
      exit 1
    fi
    ;;
esac

if [ -z "$mode" ]; then
  if ! git diff --cached --quiet -- ${paths[@]+"${paths[@]}"}; then
    mode=staged; label="staged changes (auto-detected)"
  elif ! git diff --quiet -- ${paths[@]+"${paths[@]}"} \
    || [ -n "$(git ls-files --others --exclude-standard -- ${paths[@]+"${paths[@]}"})" ]; then
    mode=worktree; label="working tree, unstaged + untracked (auto-detected)"
  else
    set_branch_mode "$(default_base || true)"
    label="$label (auto-detected: nothing uncommitted)"
  fi
fi

# emit_diff <patch|stat>
emit_diff() {
  local kind="$1"
  local -a extra=()
  case "$kind" in
    patch) extra=("${PATCH_OPTS[@]}") ;;
    stat)  extra=(--stat) ;;
  esac
  case "$mode" in
    staged)
      git diff --cached "${DIFF_OPTS[@]}" "${extra[@]}" -- ${paths[@]+"${paths[@]}"}
      ;;
    worktree)
      git diff "${DIFF_OPTS[@]}" "${extra[@]}" -- ${paths[@]+"${paths[@]}"}
      emit_untracked "$kind"
      ;;
    commit)
      # -m --first-parent so a merge commit shows its change instead of nothing.
      git show -m --first-parent "${DIFF_OPTS[@]}" "${extra[@]}" "$rev" \
        -- ${paths[@]+"${paths[@]}"}
      ;;
    branch|range)
      git diff "${DIFF_OPTS[@]}" "${extra[@]}" "$rev" -- ${paths[@]+"${paths[@]}"}
      ;;
  esac
}

# Untracked files have no index entry, so they are diffed against /dev/null.
# git renders that as a "/dev/null => path" pathname change in --stat output,
# which reads as a rename, so the stat line is built by hand from --numstat.
emit_untracked() {
  local kind="$1" file added
  while IFS= read -r -d '' file; do
    if [ "$kind" = stat ]; then
      added=$(git diff --no-index --numstat -- /dev/null "$file" 2>/dev/null | cut -f1 || true)
      [ "$added" = "-" ] && added="binary"
      printf ' %s | %s (new file)\n' "$file" "${added:-0}"
    else
      git diff --no-index "${DIFF_OPTS[@]}" "${PATCH_OPTS[@]}" -- /dev/null "$file" || true
    fi
  done < <(git ls-files --others --exclude-standard -z -- ${paths[@]+"${paths[@]}"})
}

out=$(mktemp "${TMPDIR:-/tmp}/adversarial-review.XXXXXX.diff")
emit_diff patch > "$out"

if [ ! -s "$out" ]; then
  rm -f "$out"
  echo "TARGET: $label"
  echo "RESULT: no changes to review"
  exit 0
fi

echo "TARGET: $label"
echo "BRANCH: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '(detached)')"
echo "HEAD:   $(git log -1 --no-color --format='%h %s' 2>/dev/null || echo '(no commits)')"
echo "PATCH:  $out ($(wc -l < "$out" | tr -d ' ') lines)"
echo
echo "FILES:"
emit_diff stat | sed 's/^/  /'
