#!/usr/bin/env python3
"""YouTube search using yt-dlp. Returns video metadata as JSON."""

import json
import sys

import yt_dlp


def search_youtube(query, num_results=25):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{num_results}:{query}", download=False)
        results = []
        for v in info.get("entries") or []:
            if v is None:
                continue
            results.append(
                {
                    "title": v.get("title"),
                    "author": v.get("uploader") or v.get("channel"),
                    "views": v.get("view_count"),
                    "duration": v.get("duration"),
                    "url": f"https://www.youtube.com/watch?v={v['id']}" if v.get("id") else None,
                    "upload_date": v.get("upload_date"),
                }
            )
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [num_results]", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    results = search_youtube(query, count)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
