# Templates

Empty forms. They come with the clone, in `plan/templates/`. Each names, under its title, the file it becomes, so a brief that places a file elsewhere can be checked against it. Fill in the brackets; delete the italic guidance. The kit's example (in the kit's repository, `example/`) shows most of them filled in; the last column gives where.

| Template | Becomes | Filled-in example |
|---|---|---|
| [plan-README.md](plan-README.md) | `plan/README.md`: the operating rules, marks and conventions | |
| [roadmap.md](roadmap.md) | `plan/roadmap.md` | |
| [state.md](state.md) | `plan/state.md`: the chapter state table, drift, calibration | `example/plan/state.md` |
| [task.md](task.md) | `plan/tasks/task-YYYYMMDD-NN-slug.md` | |
| [wave.md](wave.md) | a wave: a task that orders other tasks | |
| [ledger-day.md](ledger-day.md) | `plan/settled/ledger/YYYY-MM-DD.md` | `example/plan/settled/ledger/2027-03-02.md` |
| [settled-decision.md](settled-decision.md) | `plan/settled/settled-YYYYMMDD-slug.md` | |
| [card.md](card.md) | a card in `world/<folder>/` | `example/world/` |
| [card-folder-README.md](card-folder-README.md) | a card folder's index | `example/world/people/README.md` |
| [character-sheet.md](character-sheet.md) | `story/notes/characters/<name>.md` | `example/story/notes/characters/` |
| [voice-sheet.md](voice-sheet.md) | `story/voice/voice.md` | `example/story/voice/voice.md` |
| [banned.txt](banned.txt) | `story/voice/banned.txt` | `example/story/voice/banned.txt` |
| [arc-outline.md](arc-outline.md) | `story/outline/<n>-<arc>.md` | `example/story/outline/` (the arc outline) |
| [chapter-outline.md](chapter-outline.md) | `story/outline/NNNNN-slug.md` | `example/story/outline/` (chapter 00400) |
| [chapter-notes.md](chapter-notes.md) | `story/notes/NNNNN-slug.md` | `example/story/notes/` (chapter 00400) |
| [reread-hooks.md](reread-hooks.md) | `plan/reread-hooks.md`: the clue register | |
| [reader-key.md](reader-key.md) | `plan/reader-tests/key.md` | `example/plan/reader-tests/key.md` |
| [reader-questions.md](reader-questions.md) | `plan/reader-tests/questions.md` | `example/plan/reader-tests/questions.md` |
| [critic-report.md](critic-report.md) | a critic's output | `example/reports/critic-facts-00400.md` |
| [interest-merged.md](interest-merged.md) | the interest check's merged report | `example/reports/interest-merged.md` |
| [pov.md](pov.md) | `story/voice/pov.md` for the book, and `story/voice/pov-NNNNN.md` for a chapter told another way: the narration the drafter and every critic judge by | `example/story/voice/pov.md` |
| [knowledge.md](knowledge.md) | `story/voice/knowledge/<head>.md`: what a narrating head knows, believes wrongly and does not know, chapter by chapter; the drafter voices the beliefs, the critics spare them | `example/story/voice/knowledge/wren.md` |
| [volume-digest.md](volume-digest.md) | `story/volume/<volume>-digest.md`: what the volume's pages have set, read in place of its earlier chapters | |
| [refrains.txt](refrains.txt) | `story/voice/refrains.txt`: the refrains `tools/refrains.py` counts | |
| [tokens.md](tokens.md) | `plan/tokens.md`: every agent run's cost, by step | |

The rulings of the page are a template too, kept with the drafting workflows: `plan/workflows/drafting/rulings.md`.
