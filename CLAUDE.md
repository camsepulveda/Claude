# YouTube Research + NotebookLM Pipeline

This project provides two Claude Code skills for automated research:

## Available Skills

### `yt-research` — YouTube Video Search
Search YouTube for videos on any topic. Returns metadata including titles, views, authors, durations, and URLs.

**Important:** If the user does not specify a research topic, always ask them what topic they want to research before proceeding.

### `notebooklm` — Google NotebookLM Integration
Create notebooks, upload sources, get AI analysis, and generate deliverables (infographics, slide decks, flashcards, quizzes, audio overviews, reports).

**Requires authentication:** The user must run `notebooklm login` in a separate terminal before using this skill.

## Full Pipeline Workflow

When the user requests a research pipeline (e.g., "find videos on X and send them to NotebookLM"):

1. **Search** — Use the `yt-research` skill to find YouTube videos on the topic
2. **Present** — Show the user the results in a formatted table
3. **Create notebook** — Use `notebooklm` skill to create a new notebook
4. **Add sources** — Add the YouTube URLs as sources to the notebook
5. **Analyze** — Ask NotebookLM for analysis on key findings
6. **Generate deliverables** — Create any requested outputs (infographic, slides, etc.)
7. **Report** — Present the analysis and file paths to the user

## Dependencies

Install with: `pip install yt-dlp "notebooklm-py[browser]" && playwright install chromium`
