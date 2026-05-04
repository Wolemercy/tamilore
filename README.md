# tamilore

Personal learning project: building a distributed key-value store from raw sockets to consensus, following the [Topic Graph Curriculum](systems_curriculum_topic_graph_corrected.pdf).

## Layout

```
kvstore/        # the system — grows topic by topic into a distributed KV store
notebooks/      # one .ipynb per topic that needs experiments or measurements
notes/          # one .md per topic (concept, build summary, mastery answers)
notes/concept-map.md   # running synthesis log
books/          # reading material (Beej's Guide, etc.)
```

## Per-topic flow

1. Read the topic in the curriculum PDF + the linked book section.
2. Open `notes/<topic>.md`, write *Concept in my own words* (3–5 sentences).
3. Build the BUILD task — extend `kvstore/server.py` and/or run experiments in `notebooks/<topic>.ipynb`.
4. Fill in *Build summary* with what you observed (numbers, errors, surprises).
5. Answer *Mastery check* questions from memory, no notes.
6. Partner runs the verbal mastery check; mark Status as Mastery Verified.
7. Append one paragraph to `notes/concept-map.md` if there's a connection worth noting.

## Curriculum

61 topics across 13 domains (TCP, HTTP, storage, concurrency, replication, partitioning, observability, etc.) plus 6 retrieval exercises and 2 automaticity gates. Mastery is partner-verified, not self-assessed.
