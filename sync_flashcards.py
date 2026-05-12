#!/usr/bin/env python3
"""Sync flashcards.md to Anki via AnkiConnect.

Parses fenced code blocks under "## ..." headings in flashcards.md, extracts
tab-separated Q/A pairs, and adds new cards to Anki. Idempotent: cards whose
"Front" field already exists in Anki (in any deck, same note type) are skipped.

Requirements:
- Anki desktop running with the AnkiConnect addon installed
  (Tools -> Add-ons -> Get Add-ons -> code 2055492159 -> restart)
- Python 3.8+

Usage:
    python sync_flashcards.py                  # add new cards
    python sync_flashcards.py --dry-run        # parse only, no Anki calls
    python sync_flashcards.py --deck-prefix Foo --tag bar
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request


ANKICONNECT_URL = "http://localhost:8765"


def anki(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(
        ANKICONNECT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
    except urllib.error.URLError as e:
        sys.exit(
            f"AnkiConnect not reachable at {ANKICONNECT_URL}. "
            f"Is Anki running with the AnkiConnect addon? ({e})"
        )
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect error on '{action}': {data['error']}")
    return data["result"]


def parse_flashcards(text):
    """Yield (section_id, question, answer) for each Q/A line in fenced blocks under '## ...'."""
    section_re = re.compile(r"^##\s+(\S+)")
    section = None
    in_block = False
    for line in text.splitlines():
        if not in_block:
            m = section_re.match(line)
            if m:
                section = m.group(1)
                continue
        if line.startswith("```"):
            in_block = not in_block
            continue
        if not in_block or section is None:
            continue
        if line.startswith("#") or not line.strip():
            continue
        if "\t" not in line:
            print(
                f"  WARN: skipping malformed line in {section}: {line[:80]}",
                file=sys.stderr,
            )
            continue
        q, a = line.split("\t", 1)
        yield section, q.strip(), a.strip()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", default="flashcards.md")
    p.add_argument("--deck-prefix", default="Tamilore", help="hierarchical mode: cards go to '<prefix>::<section>'")
    p.add_argument("--deck", help="flat mode: put ALL cards in this single deck (overrides --deck-prefix); section becomes a tag")
    p.add_argument("--note-type", default="Basic", help="Anki note type (must have Front/Back fields)")
    p.add_argument("--tag", default="tamilore", help="tag added to every card; empty string disables")
    p.add_argument("--dry-run", action="store_true", help="parse and print, do not call Anki")
    args = p.parse_args()

    try:
        with open(args.file) as f:
            md = f.read()
    except FileNotFoundError:
        sys.exit(f"File not found: {args.file}")

    cards = list(parse_flashcards(md))
    if not cards:
        sys.exit(f"No cards found in {args.file}.")

    by_section = {}
    for section, q, a in cards:
        by_section.setdefault(section, []).append((q, a))

    print(f"Parsed {len(cards)} card(s) across {len(by_section)} section(s):")
    for s, items in by_section.items():
        print(f"  {s}: {len(items)}")

    if args.dry_run:
        for s, items in by_section.items():
            for q, a in items:
                print(f"  [DRY] {s}  Q: {q[:60]}  A: {a[:60]}")
        return

    version = anki("version")
    print(f"AnkiConnect v{version} reachable.")

    existing_decks = set(anki("deckNames"))
    added = skipped = errors = 0

    for section, q, a in cards:
        deck = args.deck if args.deck else f"{args.deck_prefix}::{section}"
        if deck not in existing_decks:
            anki("createDeck", deck=deck)
            existing_decks.add(deck)
        tags = []
        if args.tag:
            tags.append(args.tag)
        if args.deck:
            tags.append(section)  # preserve section as tag in flat mode
        note = {
            "deckName": deck,
            "modelName": args.note_type,
            "fields": {"Front": q, "Back": a},
            "options": {"allowDuplicate": False},
            "tags": tags,
        }
        try:
            anki("addNote", note=note)
            added += 1
        except RuntimeError as e:
            msg = str(e).lower()
            if "duplicate" in msg or "cannot create note because it is a duplicate" in msg:
                skipped += 1
            else:
                print(f"  ERROR adding '{q[:50]}': {e}", file=sys.stderr)
                errors += 1

    print(f"Done. Added: {added}, Skipped (duplicates): {skipped}, Errors: {errors}")


if __name__ == "__main__":
    main()
