# Card existing: the named people, places and things, from the existing work

*Basic.*

The first card pass. Every named person, place and thing in the writer's existing work gets a card in `world/`, in the form of `plan/templates/card.md`, marked, each fact with the quote it comes from. Nothing is invented: a card holds what the pages say, and the gaps become questions.

**Grade.** Mechanical for the quotes (each resolves in `existing/`) and the card heads (`tools/cards.py check`); a judgment for what counts as one thing and what a passage states.

## The loop

1. **Open a task** naming the live files in `existing/` (the interview said which are live) and the card folders: `world/people/`, `world/places/`, `world/things/`, `world/animals/` (named creatures, and the species the book describes), and any the book needs.
2. **Fresh agents, at most two,** split by card folder (people and animals in one, places and things in the other), each reading every live file ([prompt](#prompt)). Run them on a mid-sized model (Sonnet): carding is careful reading and exact quoting, which a cheap finder model skimps and a top model does not improve enough to pay for.
3. **Verify:** every quote resolves (`python3 tools/quotes.py <the report> --in existing/*`); no line is marked settled without a ledger row.
4. **Index:** copy `plan/templates/card-folder-README.md` into each card folder as its `README.md` and fill in its one line; then run `python3 tools/cards.py build` and `python3 tools/cards.py check`, which must print 0.
5. **Put the questions to the writer** in batches, with the disagreements between files quoted on both sides. Each answer goes on the ledger first, then onto its card.

## Prompt

> You are carding the existing work of a novel, in the folder {REPO}. Read `README.md`, `plan/README.md` (the marks), `plan/templates/card.md` (the form) and the live files in `existing/`: {SOURCES} (read-only). Write only new cards in {FOLDERS} and your report, {REPORT}. Run no git commands; do not launch agents. For each named person, place or thing the files hold, write one card in the form of `plan/templates/card.md`: the five-line head, then the facts the files state, each marked *(Drafted.)* and followed by its source file and line. Mark an inference *(My reading, to confirm.)*. A name met once with nothing to say about it is a crowd figure: list it in the report, do not card it. A thing met in one chapter that is no clue gets a stub: the five-line head, the line `Stub: build when a scene needs it.`, and its cited lines; a full card goes to what appears in two or more chapters or is a clue. A card holds what is true of its subject (nature, traits, skills, possessions, relations, dated changes); events and scenes stay out, since they belong to the outline. Card each thing under the name the book gives it, wherever the files first name it, not under a description used before the name. Where two files disagree, card neither version: quote both in the card's **Open** line. Invent nothing; a gap is a question. Keep lore on the card, however long. In the report, write every quote you used on its own line as `- quote: the exact words`, under the card it supports; then the crowd figures, the disagreements, and the open questions, each with your recommendation where the files support one.
