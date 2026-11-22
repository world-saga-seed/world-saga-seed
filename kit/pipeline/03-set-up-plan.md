# 03 Set up plan/

*Basic.*

**When:** after the interview.

**Uses:** [plan/templates/](../../plan/templates/README.md); [task-form](../../plan/workflows/task-form.md); the scaffolding in [kit/method/tasks-and-waves.md](../method/tasks-and-waves.md).

**What happens:** a fresh clone already holds `plan/workflows/`, `plan/templates/`, `tools/`, `kit/` and `existing/`, and the interview's first act made `plan/settled/ledger/` and `plan/state.md` from the templates. Claude creates only what is still missing: the ledger folder and `state.md` (if the interview did not), `roadmap.md`, `tasks/`, `archive/`, `story/` and `world/`, and the rest of the layout:

```
your-book/
  CLAUDE.md  README.md            the instructions, and the index of every folder
  existing/                       read-only (came with the clone)
  world/                          new: cards in people/, places/, things/, and topic files
  story/                          new: outline/ notes/ notes/characters/ prose/ voice/ voice/samples/ calendar/
  plan/   README.md roadmap.md reread-hooks.md            new
          settled/ tasks/ archive/ reader-tests/          new
          settled/ledger/ state.md                        from the interview
          workflows/ templates/                           came with the clone
  tools/  kit/                                            came with the clone
  scripts/  sources/                                      made when first needed (below)
```

`tools/` is the kit's. A script the book needs for itself (fetching a source, converting it to paragraph-numbered text, a one-off sweep) goes in `scripts/`, with a line at its head saying what it is for; a script that would serve any book is offered back to the kit (CONTRIBUTING.md). Text a script makes from `existing/` goes in `sources/<source>/`, so it can be made again. Neither goes in a task folder or a scratch folder: a later session finds them by the layout.

Then: the rest of `CLAUDE.md` filled in from the interview's answers, with the horizon (by the writer, or by Claude on the writer's word in this session: when the writer directs the work through another session, Claude's harness may refuse to edit `CLAUDE.md` on a peer's word, so the writer confirms the fields here or fills them in themself); `plan/README.md` and `roadmap.md` from the templates; `README.md` made the index of every folder; the style samples the writer picked in the interview copied, unchanged, to `story/voice/samples/` (each with its source file and line); the card folders' indexes in place (`tools/cards.py build`); the pre-commit hook installed, so no recording, `tmp/` file or large scan enters the history (`printf '#!/bin/sh\nexec python3 tools/check_commit.py\n' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`); and the page section of [rulings.md](../../plan/workflows/drafting/rulings.md) (point of view and tense, spelling, contractions, the name forms, the banned words) filled by a short interview before any render, a calibration render included, so no chapter is drafted against the template. The clone is already a git repository, one for the whole folder.

**Done when:** a fresh session given only "read CLAUDE.md and continue" can say where the work stands; `tools/links.py` and `tools/cards.py check` print 0; `rulings.md`'s page section is filled in.
