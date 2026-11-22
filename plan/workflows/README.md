# Workflows: the procedures

A workflow is a procedure a task cites instead of restating: its loop, its prompts, its checks and its lessons. It comes with the clone of the kit, as `plan/workflows/`; a book can later pull the kit's improved workflows with git. When a task develops a method worth keeping, the method comes here and the task cites it; each run's lessons are appended to the workflow's Lessons.

**Rules every workflow follows:** the marks; the ledger first; at most two agents, none spawning another (but for lookup assistants, [the librarian](drafting/prompts/librarian.md)), each with a named file list; every run logged in the token log; no git commands in any agent; fresh agents (not forks) for critics and readers; every finding quotes the text, and the quote is checked; work inside the horizon.

The two largest are **[drafting/](drafting/README.md)**, the drafting and criticism chain, and **[reader-tests](reader-tests.md)**, unit tests for a novel by chapter. Which stage uses which workflow is in `kit/pipeline/`.

## Every workflow

Each workflow has three labels.

- **Phase**, where the book is: **Intake** (knowing the existing work), **Exploration** (developing the world and story: frames, dictation, proposals, checks on the plan), **Synthesis** (outlines and drafts), **Finishing** (reading, polishing and release), or **Any** (upkeep and housekeeping, at every phase). The stages in `kit/pipeline/` fall under these phases: 01 to 04 Intake, 05 and 07 Exploration, 06 and 08 Synthesis, 09, 10 and 12 Finishing, 11 Any.
- **Level**, whether your book needs it: **Basic** workflows run from the first chapter; a **Refinement** is added when its trigger shows up in any book; a **Speciality** only when the book is of a kind that needs it. Each workflow's first line says which.
- **Status**, how far it is proven, on the one series the kit came from: **Proven**, tested against a control (planted faults, a key written before the prose) and used repeatedly; **Tested** against a control but run only once or twice; **Used** repeatedly, never against a control; **Experimental**, run only a few times. None is yet proven on a second book. If you run one against a control, log the result in its Lessons.

| Workflow | Phase | Level | Status | Add it when |
|---|---|---|---|---|
| [capture-notes](capture-notes.md) | Intake | Refinement | Experimental | the writer brings an outside document |
| [card-existing](card-existing.md) | Intake | Basic | Used |  |
| [source-language](source-language.md) | Intake | Speciality | Experimental | the book is made from a source in another language |
| [character-sheet](character-sheet.md) | Intake | Basic | Used |  |
| [arc-pitch](arc-pitch.md) | Exploration | Refinement | Used | an arc has enough frames to lay out |
| [consistency-check](consistency-check.md) | Exploration | Refinement | Used | several chapters are outlined and a horizon is about to be drafted |
| [daily-life-study](daily-life-study.md) | Exploration | Refinement | Experimental | scenes default to the reader's own world |
| [dictation](dictation.md) | Exploration | Refinement | Used | a chapter is graded thin or none |
| [echo-audit](echo-audit.md) | Exploration | Speciality | Experimental | an outcome rhymes with real history |
| [logic-check](logic-check.md) | Exploration | Refinement | Used | the arc turns on timing, travel or who-knows-what, or an outline already broke on a date or a cause |
| [proposals](proposals.md) | Exploration | Refinement | Experimental | the setting needs a set of things the notes leave thin |
| [reveal-pacing](reveal-pacing.md) | Exploration | Speciality | Experimental | the book withholds a large truth |
| [ripple](ripple.md) | Exploration | Refinement | Used | a settled change contradicts earlier notes |
| [telephone-decay](telephone-decay.md) | Exploration | Speciality | Tested | an in-world text (a scripture, a legend, an old record) must hide the truth beneath it |
| [actor-log](actor-log.md) | Synthesis | Basic (the light pass of the three critics); Refinement (the full log) | Proven | every horizon; the full log when an offstage actor drives a beat |
| [aims-sweep](aims-sweep.md) | Synthesis | Refinement | Experimental | a critic or drafter treats a "the reader feels…" line as already done |
| [draft-cards](draft-cards.md) | Synthesis | Refinement | Used | a second chapter meets people a drafter made up |
| [drafting/](drafting/README.md) | Synthesis | Basic | Proven | the core; its later steps are Refinements, each marked |
| [habits](habits.md) | Synthesis | Refinement | Used | one character's tic shows up on another |
| [outline-clean](outline-clean.md) | Synthesis | Refinement | Used | outlines written before a restructure are about to be redrafted from |
| [reader-tests](reader-tests.md) | Synthesis | Basic | Proven | the key and the blind probe; the story questions, reread test and quiz are Refinements, each marked |
| [scene-outlines](scene-outlines.md) | Synthesis | Basic | Used |  |
| [ereader](ereader.md) | Finishing | Refinement | Used | a stretch is long enough to read as a book |
| [markup](markup.md) | Finishing | Speciality | Experimental | you want to see or show whose beats a chapter carries |
| [interest-check](interest-check.md) | Finishing | Refinement | Proven | a volume is refined and a dull stretch is feared |
| [publication](publication.md) | Finishing | Refinement | Experimental | a volume is about to be released (once per volume) |
| [series-critic](series-critic.md) | Finishing | Speciality | Experimental | a clue's plant and payoff are both drafted |
| [voice-render](voice-render.md) | Finishing | Speciality | Experimental | the writer wants to listen |
| [apply-terms](apply-terms.md) | Any | Refinement | Experimental | a placeholder name is settled |
| [card-audit](card-audit.md) | Any | Refinement | Used | cards pass about 1,500 words |
| [distill](distill.md) | Any | Refinement | Used | a card collects restatements |
| [ledger-roll](ledger-roll.md) | Any | Refinement | Used | a ledger file runs past its day |
| [readings-inventory](readings-inventory.md) | Any | Refinement | Experimental | readings pile up |
| [restructure](restructure.md) | Any | Refinement | Used | a topic file passes about 5,000 words with two subjects |
| [retire](retire.md) | Any | Refinement | Used | closed tasks pile up |
| [retrospective](retrospective.md) | Any | Basic | Used |  |
| [next](next.md) | Any | Basic | Experimental |  |
| [task-form](task-form.md) | Any | Basic | Used |  |

## Belongs here, and does not

- **Belongs:** a reusable procedure (`name.md`), its prompt files (`name/`), and its lessons.
- **Does not:** a run's output (that goes to the task's folder), lore (to the cards), rulings (to the ledger).

**One kind of thing per folder.** `workflows/` holds procedures and what they run on: prompts, tools, and the config files the tools read (a word list, a field form). What a run produces goes elsewhere, by what it proves:
- **A test's or a study's evidence** (its drafts, critic reports, prompts, bundles) stays in its task's folder and is archived with the task.
- **What the standing flows produce on the book** goes to `plan/records/`, which is generated and never edited by hand: the token log, and for each drafted chapter the bundle manifest (`records/drafting/NNNNN-bundle.tsv`) and its critics' trace (`NNNNN-trace.md`).
- **Nothing a decision rests on lives only in a session's scratch space.**
