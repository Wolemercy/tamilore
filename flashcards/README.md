# Flashcards

Running record of every flashcard generated for the curriculum, plus a sync script that pushes new cards to Anki.

## Files

- [`cards.md`](cards.md) — the canonical record. Cards are organized by topic (A1, A2, A3, OS, …) under `## SECTION` headings. Each fenced code block under a heading is one Anki-importable tab-separated batch. Append new cards here; do not delete old ones after import.
- [`sync.py`](sync.py) — pushes new cards from `cards.md` into Anki via the AnkiConnect addon. Idempotent: cards already in Anki (matched by exact "Front" field) are skipped.

## One-time setup

1. Install Anki desktop if you don't have it (https://apps.ankiweb.net).
2. Install the **AnkiConnect** addon:
   - Anki → Tools → Add-ons → Get Add-ons
   - Enter code `2055492159`
   - Restart Anki
3. Keep Anki running while you sync.

Verify AnkiConnect is reachable:

```
curl localhost:8765
```

Should return something (not "connection refused").

## Daily usage

From the repo root, after adding cards to `flashcards/cards.md`:

```bash
python flashcards/sync.py --dry-run   # sanity-check parse, no Anki calls
python flashcards/sync.py             # push to Anki
```

Output looks like:

```
Parsed 41 card(s) across 4 section(s):
  A1: 15
  A2: 10
  A3: 8
  OS: 6
AnkiConnect v6 reachable.
Done. Added: 12, Skipped (duplicates): 29, Errors: 0
```

Subsequent runs only add what's new.

## Deck modes

| Command | Result |
|---|---|
| `python flashcards/sync.py` | Hierarchical: `Tamilore::A1`, `Tamilore::A2`, ... |
| `python flashcards/sync.py --deck-prefix Systems` | Hierarchical with custom parent: `Systems::A1`, ... |
| `python flashcards/sync.py --deck "Systems Curriculum"` | Flat: all cards in one deck, section preserved as a tag |

In flat mode, study just A1 cards via Anki search: `deck:"Systems Curriculum" tag:A1`.

Other flags:

- `--note-type Basic` — Anki note type (must have Front/Back fields). Default `Basic`.
- `--tag tamilore` — tag applied to every card. Empty string disables.
- `--file path/to/cards.md` — override the source file (defaults to the `cards.md` next to `sync.py`).

## Cards file format

Each section uses this structure:

````markdown
## A1 — Socket creation and binding

```
#separator:tab
#html:false
What is a file descriptor?	A small integer the OS gives you as a handle to an I/O resource.
What does AF_INET stand for?	Address Family for IPv4.
```
````

- The `## SECTION-ID …` heading: the first whitespace-separated token (`A1`, `A2`, `OS`, …) becomes the section ID and is used for the sub-deck name or tag.
- The fenced block: lines starting with `#` (Anki directives) are ignored. Every other non-empty line is `question<TAB>answer`.
- The directives `#separator:tab` and `#html:false` are kept so the same block can be copy-pasted into Anki's manual text-import dialog if you ever want to bypass the script.

## Quality rules

See the preamble in `cards.md` for the full list. Summary: one fact per card, specific atomic answer, no tangents, no long enumerations, avoid yes/no questions when reframing is clean.

## Caveats

- **Refactored cards become new cards.** Splitting an old combined card into two atomic ones means the new questions don't match the original "Front" — Anki adds the new cards as new and the old combined card is left orphaned. Clean up orphans manually in Anki's browser.
- **Dedup is by exact Front match across the entire collection** (not per-deck). So cards you previously imported into a "Default" deck won't be double-added, but they also won't migrate to the new deck. Move them manually via Anki's browser if you want consolidation.
- **Anki must be running** when you run `sync.py`. AnkiConnect is in-process.
