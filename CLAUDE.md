# [Working title]

*Template. In a fresh clone of the kit, fill in the title line now, before the intake. Fill in the rest (the pen name, the horizon in rule 8, "About the writer") from the interview's answers, at stage 03 (`kit/pipeline/03-set-up-plan.md`). Delete this paragraph then.*

A novel in progress by [your pen name]. The setting's facts are in `world/`. The story is in `story/`, one folder per type of information: `outline/`, `notes/`, `prose/`, `voice/`, `calendar/`. A chapter has one number in every folder: `00100` is chapter 1, in steps of 100, so a chapter added between 00300 and 00400 is `00350`. The index is [README.md](README.md). The procedures are in `plan/workflows/`, the forms in `plan/templates/`, the scripts in `tools/`; the method's stages and reasons are in `kit/`.

**Read `plan/README.md` at the start of every session**, then `plan/roadmap.md` and `plan/state.md`. Check them against `git log`: they are written by Claude and can be wrong. When the writer asks "what now?" or "what next?", or a session starts with no task named, run [next](plan/workflows/next.md).

## The writer's existing work

`existing/` holds the writer's manuscripts and notes as they were handed over. It is **read-only**. Never edit, move, rename or reformat a file in it. Material from it is carried into `world/` and `story/` by the workflows, with a link back.

A text that is not the writer's (a public-domain edition, a translation) sits in `existing/<source>/` with a `SOURCE.md`; plain text made from it goes in `sources/<source>/`, by a script in `scripts/` (the book's own scripts; `tools/` is the kit's). See [existing/README.md](existing/README.md).

## Rules

1. **The notes are the facts.** `world/` and `story/` say what is true. A chapter is checked against them, never the reverse. Each fact lives in one file; other files link to it, never to a task paper. When a fact changes, grep `story/prose/` for the old fact and log drift in `plan/state.md`; do not edit drafts to match unless asked.
2. **Mark every line you add.** *(Settled R<MMDD>-NN.)* for a ruling on the ledger; *(Proposal.)* for your invention; *(My reading, to confirm.)* for your reading of the writer's shorthand; *(Resolved by judgment, overturnable.)* when the writer asked you to decide; *(Aim.)* for an intended effect on the reader; *(Proposal, from the draft, NNNNN.)* for a drafter's invention, carded; *(Drafted.)* for what existing prose holds; *(Settled by the writer, date.)* for a ruling from before the ledger. Never present an invention as settled. The writer settles in place by changing the mark.
3. **The ledger first.** A ruling the writer gives goes on today's ledger file, `plan/settled/ledger/YYYY-MM-DD.md`, as one plain sentence, before any file is edited to match it. Run `date` before the first ruling of a session. Write the ruling, not the writer's words.
4. **Ask when the writer is present.** Collect open questions. Put them a few at a time, each with its context, the canon lines it rests on (quoted), and your recommendation, the plain option first. Do not send agents to decide what the writer could answer now.
5. **Check every recommendation against the notes** before you make it. Grep the facts it depends on and quote them.
6. **Gaps are asked, not invented.** The writer likely has an answer. Where a chapter has no key frame from the writer, write a brief and ask for a dictation; do not fill it.
7. **Lore stays in the notes.** Background detail goes in `world/` and the notes, not into drafted scenes, unless the scene needs it or the writer asks.
8. **Outlines before prose.** Stay in outlines until the writer says to draft. Work inside the current horizon: `[name the horizon, e.g. volume 1, chapters 00100 to 02000]`.
9. **Delete stale text.** When a later ruling replaces an older line, delete the older line. Git keeps the history. Do not put superseded text to the writer as a question.
10. **Every critic finding quotes the text.** Drop any finding whose quote does not resolve (`python3 tools/quotes.py`).
11. **Never trim a clue.** No cut, trim or revision removes a line listed in `plan/reread-hooks.md` or a chapter's clue notes. A line that looks like a clue and is listed nowhere is kept and reported.
12. **Agents.** At most two at a time. None may spawn its own. Each gets a named list of the files it may read and the files it may write. Use fresh agents, not forks, for critics and readers, so they cannot see the writer's reasoning. Every prompt says: run no git commands.
13. **Commit only when the writer says so.** Edit, summarize, say it is uncommitted, and offer.
14. **Close every session** by `plan/workflows/retrospective.md`.
15. **When the writer is on a phone** (a Remote Control session), reply in a few lines: the verdict first, then one question or finding at a time with its recommendation. Never paste a diff or a whole report; say where it is and what it says.
16. **Ages are stated where a scene touches sex or romance.** Anthropic's Usage Policy applies to all drafting, whatever the setting's world, species or laws. Any outline or notes touching sex or romance names the parties and their true ages at the head; a character's sheet holds every age at once, so never rely on the reader of a bundle to infer it. Where the ages are unclear, ask the writer before drafting. An age is the story's truth, never a label to make a scene pass.

## About the writer

*Fill in what helps Claude work with you. Leave out anything you would rather not say.*

- Genre and what the book promises its reader: [ ]
- What you dislike in books like this: [ ]
- How you read drafts (screen, ereader, audio), and anything that makes reading hard for you (for example, unmarked jumps in time): [ ]
- How you like questions put to you (a few at a time; by structure, not by asking you to recall exact words): [ ]
- Where your expertise is (a trade, a place, a period), so Claude takes your calls there as fact: [ ]
