---
name: notebooklm
description: Interact with Google NotebookLM to create notebooks, upload sources (YouTube URLs, PDFs, websites), get AI analysis, and generate deliverables like infographics, slide decks, flashcards, quizzes, audio overviews, and reports. Use when the user wants to analyze content with NotebookLM or generate research deliverables.
---

# NotebookLM Skill

Create notebooks, upload sources, get AI analysis, and generate deliverables using Google NotebookLM.

## Prerequisites

- `notebooklm-py[browser]` must be installed (`pip install "notebooklm-py[browser]"`)
- User must have authenticated via `notebooklm login` in a separate terminal
- If authentication fails, remind the user to run `notebooklm login` first

## How to Use

Use the helper script for all NotebookLM operations:

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" <command> [args...]
```

## Commands

### Create a Notebook

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" create "Notebook Name"
```

Returns the notebook ID. Save this for subsequent commands.

### Add YouTube URLs as Sources

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" add-youtube <notebook_id> "https://youtube.com/watch?v=..." "https://youtube.com/watch?v=..."
```

Accepts multiple URLs. Each is added and indexed before continuing.

### Ask a Question / Get Analysis

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" ask <notebook_id> "What are the top findings across these sources?"
```

Returns NotebookLM's analysis as text.

### Generate Infographic

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" generate-infographic <notebook_id> [--orientation portrait|landscape|square] [--detail 1|2|3] [--instructions "handwritten chalkboard style"]
```

Downloads to `./output/infographic.png` by default.

### Generate Slide Deck

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" generate-slides <notebook_id> [--format detailed|presenter] [--length 10] [--output ./output/slides.pdf]
```

### Generate Flashcards

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" generate-flashcards <notebook_id> [--quantity more] [--difficulty medium] [--output ./output/flashcards.json]
```

### Generate Quiz

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" generate-quiz <notebook_id> [--quantity 10] [--difficulty hard] [--output ./output/quiz.json]
```

### Generate Audio Overview

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" generate-audio <notebook_id> [--format deep-dive|brief|critique|debate] [--length medium] [--output ./output/audio.mp3]
```

### Generate Report / Study Guide

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/notebooklm/scripts/notebooklm_helper.py" generate-report <notebook_id> [--template study_guide|briefing|blog_post|custom] [--instructions "Focus on X"] [--output ./output/report.md]
```

## Typical Pipeline Workflow

1. **Create** a notebook with a descriptive name
2. **Add sources** — YouTube URLs from yt-research skill, or other URLs/files
3. **Ask** NotebookLM for analysis on key findings
4. **Generate** deliverables (infographic, slides, flashcards, etc.)
5. Present the analysis and deliverable file paths to the user

## Error Handling

- If you get an authentication error, tell the user: "Please run `notebooklm login` in a separate terminal to authenticate with your Google account, then try again."
- If source indexing times out, retry with the same command.
- Output files are saved to `./output/` directory by default. The directory is created automatically.
