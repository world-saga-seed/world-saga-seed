# World Saga Seed: a method for writing a long-form novel with Claude Code

*"Saga" for long: a novel of 80,000 words or more, or a series, in any genre. "Seed" because a clone of the kit is the seed your book grows from.*

> **Alpha:** a work in progress, tested so far on one series, with its first outside testers starting now. Expect rough edges. What has been tested, what you need and what it costs are in [the wiki](https://github.com/world-saga-seed/world-saga-seed/wiki/Before-you-start).

This kit is for a fiction writer with existing material (a manuscript, a half-draft, a folder of notes) who wants to work with Claude Code without the story drifting, without the model's habits taking over the voice, and without losing their own decisions. You do not need to be technical. It suits long work best. You can also start from nothing: the method was first run with no manuscript at all, from the interview alone.

It is a set of workflows: procedures Claude Code runs on your book, each saying what it is for, when to run it, what it reads, its steps, its prompts, its checks and what it produces, with the lessons and failure modes that came out of using it. They were developed over many months on one long series. Everything specific to that series has been taken out. What is left is the procedures, some small tools, and one toy novel carried through every stage as an example.

**What it is not:** it does not write your book for you. Claude drafts the prose; you supply every scene and decision, and can write any chapter yourself and use only the checks and reader tests on it. Claude places your scenes, proposes what goes between them, drafts to your rulings and checks the result, and nothing is done until you say so.

## Before you start

What it costs in tokens and time, and how much of the bible a chapter reads, are in [kit/method/costs.md](kit/method/costs.md). What has been tested, what you need, where your manuscript goes, and **the content limits** (Anthropic's Usage Policy applies to everything drafted, whatever the setting) are in [the wiki](https://github.com/world-saga-seed/world-saga-seed/wiki/Before-you-start), with the [big ideas](https://github.com/world-saga-seed/world-saga-seed/wiki/The-big-ideas) behind the method and a [glossary](https://github.com/world-saga-seed/world-saga-seed/wiki/Glossary) of the words used here.

**During the alpha, until 15 December 2026,** issues, comments and pull requests are open to collaborators only. To comment, ask to be added as a collaborator in the Discord discussion where the alpha was shared; anyone can read, clone and fork the kit meanwhile.

**Feedback:** open an issue for anything that breaks, confuses you, or makes Claude do something odd. Say which workflow and step you were on. To give back an improvement you found (a better critic, a voice rule, a cheaper step), see [CONTRIBUTING.md](CONTRIBUTING.md): describe it in an issue, or send it yourself through your own fork, reviewed there first.

## How to start

A clone of the kit is the skeleton of your book: the workflows, templates and tools are already where the book needs them.

Claude does the technical steps; you say what you want. Open Claude Code in an empty folder named for your book and say: "Set up this folder as a book from the World Saga Seed kit at https://github.com/world-saga-seed/world-saga-seed, check Python 3 and git are installed, delete the example, and run the clean check." Behind that request, Claude clones the kit (a copy that remembers where it came from, so it can pull improvements later) into the folder, deletes the toy novel in `example/` (it stays readable in the kit's repository) and runs a check that nothing of the example is left.

Then you put your manuscripts in `existing/` (drag them into the folder) and give Claude the working title. Then, for your first chapter:

1. **The [intake](kit/interview/intake.md).** Say: "Read CLAUDE.md, then plan/workflows/README.md, then kit/interview/intake.md. Do the intake on my existing work in existing/: list what is there, what kind of material each file is, and what you would ask me first. Do not change any file in existing/. Write your report to plan/tasks/ and stop." You get a list of what is there and Claude's first questions.
2. **The [interview](kit/interview/README.md),** one or two sessions: your answers on the book, written down, and the style samples (passages of your own prose the voice is measured against), picked from the intake's candidates.
3. **[Set up `plan/`](kit/pipeline/03-set-up-plan.md):** the roadmap, the state of each chapter and the ledger of rulings, ready to use.
4. **Card the existing work:** one card per person, place and thing ([card-existing](plan/workflows/card-existing.md)); scene outlines taken back out of the prose you have already written ([scene-outlines](plan/workflows/scene-outlines.md), its "deconstruct" prompt); and a character sheet for the narrator ([character-sheet](plan/workflows/character-sheet.md)).
5. **Outline one chapter** ([scene-outlines](plan/workflows/scene-outlines.md), its "outline" prompt) and write its reader-test key: what a blind reader must get, must not get and may only guess ([reader-tests, the key](plan/workflows/reader-tests.md#1-the-key)). For the first chapter, the story's shape, its ending and the chapter list as far as you know them are enough, filled in by hand from the interview's answers.
6. **Fill in [rulings.md](plan/workflows/drafting/rulings.md),** the rules the drafter must keep, and draft the chapter ([drafter.md](plan/workflows/drafting/drafter.md)).
7. **Check it:** the scripted checks ([mechanical.md](plan/workflows/drafting/mechanical.md)), the facts critic and the voice critic ([critics.md](plan/workflows/drafting/critics.md)), the quote check ([verify.md](plan/workflows/drafting/verify.md)), and a revision that fixes only the verified findings ([reviser.md](plan/workflows/drafting/reviser.md)).
8. **Run the [blind probe](plan/workflows/reader-tests.md#3-the-blind-probe):** a fresh reader's answers on that chapter, scored against its key.
9. **Close the session** ([retrospective.md](plan/workflows/retrospective.md)): what was learned written down and the plan's state brought up to date.

Everything else is a Refinement; each says when to add it. To run the daily work from a phone once this is done, see [working from a phone](https://github.com/world-saga-seed/world-saga-seed/wiki/Working-from-a-phone) in the wiki. A book made from the kit can later pull improved workflows from it: ask Claude to update the kit, and it shows you any place where the new version meets your own edits.

## The workflows

The [kit/pipeline/](kit/pipeline/README.md) is the one map of stages to workflows, in order. The work runs as tasks and waves ([kit/method/tasks-and-waves.md](kit/method/tasks-and-waves.md)).

| Tier | Workflows | When |
|---|---|---|
| **Basic** | the intake and interview; [card-existing](plan/workflows/card-existing.md); [task-form](plan/workflows/task-form.md), [retrospective](plan/workflows/retrospective.md); [scene-outlines](plan/workflows/scene-outlines.md), [character-sheet](plan/workflows/character-sheet.md); the core of [drafting/](plan/workflows/drafting/README.md) (the drafter, mechanical checks, the facts and voice critics, verify, reviser); [reader-tests](plan/workflows/reader-tests.md) (the key and the blind probe) | from the first chapter |
| **Refinement** | everything else | each workflow's first line says when to add it; the full list is in [plan/workflows/](plan/workflows/README.md) |

## Map of the kit

| Folder | Holds |
|---|---|
| [plan/workflows/](plan/workflows/README.md) | **The kit.** Every procedure, complete in itself, with its prompts. [drafting/](plan/workflows/drafting/README.md) is the largest section. |
| [plan/templates/](plan/templates/README.md) | Empty forms for the plan, tasks, ledger, cards, sheets, outlines, the reader-test spec, reports. |
| [tools/](tools/README.md) | Nineteen small Python scripts that Claude runs, in three levels. **Basic**, for every chapter: broken links, card heads and the subject index, each run's reading list, quotes checked against the text, and an EPUB of your book for an ereader. **Refinement**, once a draft stands: the model's habit words and banned words, phrases and refrains repeated across chapters, the same phrase twice in a few paragraphs, any pattern shown in its context for a rule check or a cheap judge, words used before they are explained, and old drafts carried into a redraft. **Speciality**, only if your book needs it: sizes seen from a viewpoint that is not an adult's, written-out sounds, the attribution test for several viewpoints, the knowledge guard, a page marking each chapter's beats by whose they are, and a leak check for changes sent back to the kit. |
| [kit/interview/](kit/interview/README.md) | The intake and interview script. |
| [kit/pipeline/](kit/pipeline/README.md) | The stages in order: when each runs and which workflows it uses. |
| [kit/method/](kit/method/README.md) | The reasons Claude reads while it works: tasks and waves, cards, horizons, key frames, choosing a check, craft principles, closing cleanly. The rest of the reasons, and the setup guides, are in [the wiki](https://github.com/world-saga-seed/world-saga-seed/wiki). |
| [existing/](existing/README.md) | Where your manuscripts and notes go. Claude reads it and never changes it. |
| `example/` | A toy novel through every stage in miniature, with a worked run of the drafting chain and a reader-test spec. The only thing you delete to start a book; it stays readable in the kit's repository. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to give an improvement back: an issue, or a change sent through your own fork and reviewed there before it comes to the kit. |
| [CLAUDE.md](CLAUDE.md) | The instructions Claude reads in your book's folder. A template: the title now, the rest after the interview. |

## Tests

Every script and every prompt in the kit has a test, kept in a separate repo so the kit stays small: [world-saga-seed-test](https://github.com/world-saga-seed/world-saga-seed-test). It runs on an invented novel, so you can check a piece yourself before you trust it with your book.

- **The scripts:** planted cases with known answers. Clone the test repo beside this one and run `python3 -m pytest -q` in it. It is free and takes seconds; run it after you change a script.
- **The prompts:** a chapter with faults planted in it, an answer key, and a scorer for each. They spend tokens, and each records one baseline run to compare yours with.

Found a script or a prompt getting something wrong on your own book? Make the smallest invented case that shows it, with none of your book's text, and add it there.

## License

The docs are [CC BY 4.0](LICENSE): use and adapt them freely, with credit. The scripts in `tools/` are [MIT](tools/LICENSE). The license applies only to the files published in this repository. Anything you make with the kit is your own (your book, your notes, your cards and your plan/), and the license claims nothing over it. If you share the kit's files or an adaptation of them, give credit. For a book made with the kit, credit is asked, not required: *Made with World Saga Seed, by Karl Nelson.*
