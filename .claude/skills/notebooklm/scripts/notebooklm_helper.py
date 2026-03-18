#!/usr/bin/env python3
"""NotebookLM helper script for Claude Code integration.

Usage:
    notebooklm_helper.py create <name>
    notebooklm_helper.py add-youtube <notebook_id> <url1> [url2 ...]
    notebooklm_helper.py ask <notebook_id> <question>
    notebooklm_helper.py generate-infographic <notebook_id> [options]
    notebooklm_helper.py generate-slides <notebook_id> [options]
    notebooklm_helper.py generate-flashcards <notebook_id> [options]
    notebooklm_helper.py generate-quiz <notebook_id> [options]
    notebooklm_helper.py generate-audio <notebook_id> [options]
    notebooklm_helper.py generate-report <notebook_id> [options]
"""

import argparse
import asyncio
import json
import os
import sys

from notebooklm import NotebookLMClient


OUTPUT_DIR = os.path.join(os.getcwd(), "output")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


async def cmd_create(args):
    async with await NotebookLMClient.from_storage() as client:
        nb = await client.notebooks.create(args.name)
        notebook_id = nb.id if hasattr(nb, "id") else str(nb)
        print(json.dumps({"notebook_id": notebook_id, "name": args.name}))


async def cmd_add_youtube(args):
    async with await NotebookLMClient.from_storage() as client:
        added = []
        for url in args.urls:
            print(f"Adding source: {url}", file=sys.stderr)
            await client.sources.add_youtube(args.notebook_id, url, wait=True)
            added.append(url)
            print(f"  Done: {url}", file=sys.stderr)
        print(json.dumps({"added": len(added), "urls": added}))


async def cmd_ask(args):
    async with await NotebookLMClient.from_storage() as client:
        result = await client.chat.ask(args.notebook_id, args.question)
        answer = result.answer if hasattr(result, "answer") else str(result)
        print(answer)


async def cmd_generate_infographic(args):
    ensure_output_dir()
    output = args.output or os.path.join(OUTPUT_DIR, "infographic.png")
    async with await NotebookLMClient.from_storage() as client:
        kwargs = {}
        if args.orientation:
            kwargs["orientation"] = args.orientation
        if args.detail:
            kwargs["detail_level"] = args.detail
        if args.instructions:
            kwargs["instructions"] = args.instructions
        status = await client.artifacts.generate_infographic(args.notebook_id, **kwargs)
        if hasattr(status, "task_id"):
            await client.artifacts.wait_for_completion(args.notebook_id, status.task_id)
        await client.artifacts.download_infographic(args.notebook_id, output)
        print(json.dumps({"type": "infographic", "path": output}))


async def cmd_generate_slides(args):
    ensure_output_dir()
    output = args.output or os.path.join(OUTPUT_DIR, "slides.pdf")
    fmt = "pdf" if output.endswith(".pdf") else "pptx"
    async with await NotebookLMClient.from_storage() as client:
        kwargs = {}
        if args.format:
            kwargs["format"] = args.format
        if args.length:
            kwargs["length"] = args.length
        status = await client.artifacts.generate_slide_deck(args.notebook_id, **kwargs)
        if hasattr(status, "task_id"):
            await client.artifacts.wait_for_completion(args.notebook_id, status.task_id)
        await client.artifacts.download_slide_deck(args.notebook_id, output, output_format=fmt)
        print(json.dumps({"type": "slide_deck", "path": output}))


async def cmd_generate_flashcards(args):
    ensure_output_dir()
    output = args.output or os.path.join(OUTPUT_DIR, "flashcards.json")
    fmt = output.rsplit(".", 1)[-1] if "." in output else "json"
    async with await NotebookLMClient.from_storage() as client:
        kwargs = {}
        if args.quantity:
            kwargs["quantity"] = args.quantity
        if args.difficulty:
            kwargs["difficulty"] = args.difficulty
        status = await client.artifacts.generate_flashcards(args.notebook_id, **kwargs)
        if hasattr(status, "task_id"):
            await client.artifacts.wait_for_completion(args.notebook_id, status.task_id)
        await client.artifacts.download_flashcards(args.notebook_id, output, output_format=fmt)
        print(json.dumps({"type": "flashcards", "path": output}))


async def cmd_generate_quiz(args):
    ensure_output_dir()
    output = args.output or os.path.join(OUTPUT_DIR, "quiz.json")
    fmt = output.rsplit(".", 1)[-1] if "." in output else "json"
    async with await NotebookLMClient.from_storage() as client:
        kwargs = {}
        if args.quantity:
            kwargs["quantity"] = args.quantity
        if args.difficulty:
            kwargs["difficulty"] = args.difficulty
        status = await client.artifacts.generate_quiz(args.notebook_id, **kwargs)
        if hasattr(status, "task_id"):
            await client.artifacts.wait_for_completion(args.notebook_id, status.task_id)
        await client.artifacts.download_quiz(args.notebook_id, output, output_format=fmt)
        print(json.dumps({"type": "quiz", "path": output}))


async def cmd_generate_audio(args):
    ensure_output_dir()
    output = args.output or os.path.join(OUTPUT_DIR, "audio.mp3")
    async with await NotebookLMClient.from_storage() as client:
        kwargs = {}
        if args.format:
            kwargs["format"] = args.format
        if args.length:
            kwargs["length"] = args.length
        status = await client.artifacts.generate_audio(args.notebook_id, **kwargs)
        if hasattr(status, "task_id"):
            await client.artifacts.wait_for_completion(args.notebook_id, status.task_id)
        await client.artifacts.download_audio(args.notebook_id, output)
        print(json.dumps({"type": "audio", "path": output}))


async def cmd_generate_report(args):
    ensure_output_dir()
    output = args.output or os.path.join(OUTPUT_DIR, "report.md")
    async with await NotebookLMClient.from_storage() as client:
        kwargs = {}
        if args.template:
            kwargs["template"] = args.template
        if args.instructions:
            kwargs["custom_instructions"] = args.instructions
        status = await client.artifacts.generate_report(args.notebook_id, **kwargs)
        if hasattr(status, "task_id"):
            await client.artifacts.wait_for_completion(args.notebook_id, status.task_id)
        await client.artifacts.download_report(args.notebook_id, output)
        print(json.dumps({"type": "report", "path": output}))


def build_parser():
    parser = argparse.ArgumentParser(description="NotebookLM helper for Claude Code")
    sub = parser.add_subparsers(dest="command", required=True)

    # create
    p = sub.add_parser("create", help="Create a new notebook")
    p.add_argument("name", help="Notebook name")

    # add-youtube
    p = sub.add_parser("add-youtube", help="Add YouTube URLs as sources")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("urls", nargs="+", help="YouTube URLs to add")

    # ask
    p = sub.add_parser("ask", help="Ask a question about notebook sources")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("question", help="Question to ask")

    # generate-infographic
    p = sub.add_parser("generate-infographic", help="Generate an infographic")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("--orientation", choices=["portrait", "landscape", "square"])
    p.add_argument("--detail", type=int, choices=[1, 2, 3])
    p.add_argument("--instructions", help="Style instructions (e.g., 'handwritten chalkboard style')")
    p.add_argument("--output", help="Output file path")

    # generate-slides
    p = sub.add_parser("generate-slides", help="Generate a slide deck")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("--format", choices=["detailed", "presenter"])
    p.add_argument("--length", type=int, help="Number of slides")
    p.add_argument("--output", help="Output file path")

    # generate-flashcards
    p = sub.add_parser("generate-flashcards", help="Generate flashcards")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("--quantity", help="Number of flashcards (e.g., 'more')")
    p.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    p.add_argument("--output", help="Output file path")

    # generate-quiz
    p = sub.add_parser("generate-quiz", help="Generate a quiz")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("--quantity", type=int, help="Number of questions")
    p.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    p.add_argument("--output", help="Output file path")

    # generate-audio
    p = sub.add_parser("generate-audio", help="Generate an audio overview")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("--format", choices=["deep-dive", "brief", "critique", "debate"])
    p.add_argument("--length", choices=["short", "medium", "long"])
    p.add_argument("--output", help="Output file path")

    # generate-report
    p = sub.add_parser("generate-report", help="Generate a report or study guide")
    p.add_argument("notebook_id", help="Notebook ID")
    p.add_argument("--template", choices=["study_guide", "briefing", "blog_post", "custom"])
    p.add_argument("--instructions", help="Custom instructions for the report")
    p.add_argument("--output", help="Output file path")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    cmd_map = {
        "create": cmd_create,
        "add-youtube": cmd_add_youtube,
        "ask": cmd_ask,
        "generate-infographic": cmd_generate_infographic,
        "generate-slides": cmd_generate_slides,
        "generate-flashcards": cmd_generate_flashcards,
        "generate-quiz": cmd_generate_quiz,
        "generate-audio": cmd_generate_audio,
        "generate-report": cmd_generate_report,
    }

    try:
        asyncio.run(cmd_map[args.command](args))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if "auth" in str(e).lower() or "credential" in str(e).lower() or "login" in str(e).lower():
            print(
                "\nPlease run 'notebooklm login' in a separate terminal to authenticate.",
                file=sys.stderr,
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
