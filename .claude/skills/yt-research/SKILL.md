---
name: yt-research
description: Search YouTube for videos on a topic and return metadata (titles, views, authors, durations, URLs). Use when the user asks to research YouTube videos, find trending videos, or search for video content on a topic.
---

# YouTube Research Skill

Search YouTube for videos on any topic and return structured metadata.

## Prerequisites

- `yt-dlp` must be installed (`pip install yt-dlp`)

## IMPORTANT: Topic Required

If the user does NOT specify a research topic, you MUST ask them:
> "What topic would you like me to research on YouTube?"

Do NOT proceed without a topic.

## How to Use

Run the search script:

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/yt-research/scripts/search.py" "<search query>" [num_results]
```

- **search query** (required): The YouTube search terms
- **num_results** (optional): Number of results to return. Default: 25

### Example

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/yt-research/scripts/search.py" "Ambulatory Bone Marrow Transplant" 25
```

## Output Format

The script outputs JSON with an array of video objects:

```json
[
  {
    "title": "Video Title",
    "author": "Channel Name",
    "views": 12345,
    "duration": 600,
    "url": "https://www.youtube.com/watch?v=...",
    "upload_date": "20260101"
  }
]
```

## Presenting Results

After running the search, present the results to the user as a formatted table:

| # | Title | Author | Views | Duration | URL |
|---|-------|--------|-------|----------|-----|

- Sort by view count (highest first) unless the user requests otherwise
- Format duration as MM:SS or HH:MM:SS
- Format view counts with commas (e.g., 1,234,567)
- Format upload_date as readable date (e.g., Jan 1, 2026)

## Pipeline Integration

After presenting results, if the user wants to send videos to NotebookLM, collect the YouTube URLs and pass them to the `notebooklm` skill.
