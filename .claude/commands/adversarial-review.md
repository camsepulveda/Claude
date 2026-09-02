---
description: Adversarially review a diff — attack the change, verify each candidate defect, report only what survives
argument-hint: "[staged|worktree|head|branch[:base]|<commit>|<a>..<b>|<path>] [--fix]"
allowed-tools: Bash(./.claude/scripts/adversarial-review-diff.sh:*), Bash(git log:*), Bash(git show:*), Bash(git blame:*), Bash(git diff:*), Read, Grep, Glob, Edit
---

Adversarially review a change. Arguments: `$ARGUMENTS`

You are not the author's ally here. Your working assumption is that this diff
is **wrong** and your job is to find out how. A review that finds nothing is a
valid result, but only after a genuine attempt to break the change.

## 1. Collect the diff

If `$ARGUMENTS` contains `--fix`, remember it and strip it. Pass everything
else through unchanged:

```
./.claude/scripts/adversarial-review-diff.sh <remaining arguments>
```

The script prints the resolved target, a file summary, and the path to the
full patch. Read that patch file. If it reports `no changes to review`, say so
and stop — do not invent a target.

## 2. Establish intent before attacking

Read the surrounding code, not just the diff. For each changed file, open
enough of it to know what the code did before and what callers expect. Use
`git log` / `git blame` on the touched lines when the change removes or
inverts existing behavior — code that looks pointless is often load-bearing.

Write down, for yourself, one sentence on what the change is *trying* to do.
Every later finding is measured against that intent.

## 3. Attack

Work through these deliberately. Most diffs fail on the first three.

- **Inverted or off-by-one logic** — boundary values, `<` vs `<=`, negated
  conditions, loop bounds, slice/index arithmetic.
- **The unhandled path** — empty input, zero, null/None, missing key, empty
  collection, single element, duplicate, unicode, very large value.
- **Error handling** — swallowed exceptions, an error path that leaves state
  half-written, a retry that isn't idempotent, a `catch` that hides the real
  failure.
- **Contract breaks** — every caller of a changed signature, return type,
  thrown error, or nullability. Grep for the callers; do not assume the diff
  shows them all.
- **State and lifetime** — mutation of a shared or borrowed structure,
  resource left unclosed, cache invalidated wrongly, ordering assumptions
  between two calls.
- **Concurrency** — check-then-act races, non-atomic read-modify-write,
  assumptions that a handler runs once.
- **Data integrity** — partial writes, missing transaction boundaries,
  migrations that are not reversible or not safe to run twice.
- **Security** — untrusted input reaching a query, path, command, or
  deserializer; authz checks removed or bypassed; secrets or PII in logs,
  errors, or committed files.
- **Deletions** — what did the removed lines protect against? A removed
  guard, test, or validation is a finding until proven redundant.
- **Tests** — does the new test actually fail without the fix? Is the assert
  reachable? Is a genuine behavior change left uncovered?

Do not report: formatting, naming taste, "consider extracting", or a rewrite
of working code in your preferred style. Redundant, dead, or duplicated logic
counts only when you can point at the concrete cost.

## 4. Verify — this is the part that matters

Every candidate you found in step 3 is a *hypothesis*. Now try to disprove it.

For each one:
1. Re-read the actual code paths involved, at full context, in the real files.
2. Construct a concrete failure: specific inputs or state → the exact wrong
   output, exception, or corrupted state that results.
3. Look for what makes it safe anyway — a caller-side guard, an earlier
   validation, a type constraint, a framework guarantee. Grep for it.
4. Classify:
   - **CONFIRMED** — you traced the failing path end to end.
   - **PLAUSIBLE** — the path is real but one link rests on an assumption you
     could not verify. State the assumption in the finding.
   - Anything weaker: **discard it silently.** Do not pad the report.

A finding you cannot express as "given X, the code does Y, which is wrong
because Z" is not a finding.

## 5. Report

Most severe first. For each finding:

- `path/to/file.ext:LINE` — one-sentence statement of the defect
- **Trigger:** the concrete inputs or state
- **Consequence:** what breaks, and how badly
- **Verdict:** CONFIRMED or PLAUSIBLE
- **Fix:** the minimal change, as a short patch or precise description

Then a closing line: what you attacked and found solid, so the author knows
the review's coverage rather than just its complaints. If nothing survived
verification, say that plainly and name the areas you probed.

If `--fix` was passed: after reporting, apply the CONFIRMED findings to the
working tree, smallest change per finding, and list what you changed. Leave
PLAUSIBLE findings alone — those are the author's call.
