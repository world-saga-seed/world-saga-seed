# Actor logs: the timelines behind the narrator's view

*The three critics' [light pass](#the-light-pass-basic) is Basic. The full log is a Refinement: add it when an offstage actor drives a beat.*

The outline is the narrator's view, so anyone else's work shows only where it crosses theirs. Between crossings nothing tracks them: a character can be in two places, know what they could not, act on no motive, or sit idle while the plot needs them. An actor log is the writer-side record of one actor's doing, knowing and wanting across a horizon, checked against the outline.

**Who gets one.** Anyone whose offstage work crosses the narrator's view and drives a beat. A group (a family, a firm, a faction) gets one by the same test. The writer chooses the list per horizon.

## When it runs

The check runs on outlines, so it runs **every time a horizon's outlines change in bulk, before anything is drafted from them**: after a restructure, an [outline clean](outline-clean.md) or a consistency batch that moves beats, and at each new horizon. The drafting gate waits on it.

- **Rerun, not patched.** A log is rebuilt by the loop below from the current outlines, not mended row by row; spot fixes between runs do not count as a run.
- **Each log's head records its last run:** `Last run: <commit> <date>`. The log is stale once any outline in its horizon changes after that commit.
- **The extraction reads the current outlines, notes, cards and ledger only, never a retired draft,** so a superseded beat cannot come back through the log.
- **Then the cross-log check.** Once every log of the horizon is rebuilt, two agents read the logs against each other **at the scenes where two actors meet** (from each log's Where and Trace columns), not every pair in full, for conflicts of time, place, knowledge, event and want.

## The three critics

The audit asks three questions of every row and every beat the actor drives, one critic each:

- **Logistics and physics.** Can they get there in the time (*presence*, *timing*: travel, work hours, the calendar)? Do they have the supplies, tools, money and hands the act needs (*means*)? How long does the act itself take, and does the calendar hold it (*duration*)? Are they idle where they would act, or carrying more threads than one person could (*load*)?
- **Causal chain.** What started them on the path that leads here (*trigger*)? Do they know what the act needs, from an earlier row that says when and from whom (*knowledge*; for a group, through a channel its Knows column names)? Do they know how to do it, by training or trade (*know-how*)? Does a want drive the beat (*motive*)?
- **Character invariant.** Is the act consistent with the person's [sheet](character-sheet.md): their center, goals and habits? The critic names the sheet line the act breaks or stretches. **It flags, it does not block:** an act out of character can be deliberate (a mask, a breaking point), so the writer rules, and a stretch ruled deliberate goes on the sheet so it is not raised again. It reads the person's sheet; a person with no sheet (a book carded from an existing work often has cards, not sheets) is judged by their card in `world/people/`, its traits, habits and dated changes, and the critic says it read the card.

**Development, optional** (for a book with child characters): a fourth critic, run beside the three when the writer turns it on. For each act a minor drives, is it within what a person of that age and upbringing can do, know, judge and endure? It names the age (the sheet's table, the calendar), quotes the act, and says what a child of that age would plausibly do instead. It checks:
  - **the body:** strength, stamina, reach (sizes are [scale.py's](../../tools/scale.py) job; this is what the body can do);
  - **judgment:** planning ahead, weighing risk, reading adults' motives;
  - **feeling:** how they carry fear, grief and shame, and how long they can hold it in;
  - **talk:** the words and the rhetoric they could command;
  - **the adults:** whether the adults around them treat them as the child they are.

  **It flags, it never blocks,** like the character invariant. A gap can be deliberate, and the writer rules on it. A gap ruled deliberate goes in the sheet's author-side section, so only the critics see it and it is not raised again; it never reaches a drafter's bundle. It runs on outlines only, never on prose.

**The interview is forced.** Every finding of rank (a) (step 5) is written to the task's `interview.md`: both sides quoted, the plain fix first, and a recommendation. The [drafting gate](drafting/README.md#the-gate) refuses "draft" while any item there is open. **The interview is where the human creativity comes in.** A finding is not just a fault to patch: each item asks the writer why the person did it, what moved them, and how they thought it through. The recommendation is there to accept or overrule, never a substitute for that answer, and the answer goes into the log's Wants and Knows rows and the sheet, so the drafter writes from it.

## The light pass (Basic)

Without full logs, the three critics run over the horizon's outlines at one of three settings, the writer's choice; **Quick is the default.** They ask their questions of every beat and every person who acts, including the offstage moves a beat rests on: who must have gone somewhere, carried something, learned something or decided something off the page for this beat to happen. Findings that change an outline line go into `interview.md` as the full audit's do. When offstage actors drive many beats, add the full log.

| Setting | What runs | Tokens per chapter | Found, in the kit's test | The writer's time |
|---|---|---|---|---|
| **Quick** (default) | the **staging agent** once: one agent takes the chapters in order; for each, it reads the chapter, collects the state (who is where, holds what, knows what from whom, wants what), critiques it, and writes its findings and a handoff before reading the next | about 45k | 60 to 73% of planted faults in a run | one interview |
| **Thorough** | the staging agent twice, merged | about 90k | 80% together | about the same, since duplicates merge |
| **Deep** (Refinement) | the **chain**: one fresh agent per critic per chapter, each reading the handoff of the one before | about 100k a critic, 300k for all three | finds different faults, not more; with Thorough, 93% | one interview |

The numbers come from one test, on one book: fifteen faults planted in three chapters' outlines, each setting run twice. Run the [injection test](#the-injection-test) on your own book to get yours. When to recommend a higher setting is in [choosing a check](../../kit/method/choosing-a-check.md).

- **Merge before the writer reads.** Every run of a pass goes into one `interview.md`, duplicates merged, so your time follows the distinct faults, not the number of runs.
- **The drops.** A critic argues real faults away ("reachable", "plausible"). On merging, a drop that another run raised is promoted into the interview with both reasons; the rest follow the interview as a one-line appendix, the drops that cite no rule marked for a skim.
- **What none of them catch.** A cause removed, a beat with nothing to start it, escaped every run in the test. The interview's question (why did they?) and your own read are the check for it.

## The injection test

To measure a setting on your book: copy a few chapters' outlines somewhere the critics will read instead of the real ones (a separate checkout works); plant ten to fifteen faults, a couple for each question, each a plausible one-line change; keep the key where no critic can read it; run each setting twice; score how many plants each run found, how many it raised that were not plants, and its tokens and minutes. Claude can do all of it; ask it to "run the injection test on the three critics".

## The log

`story/calendar/<actor>/<arc>.md`, a table in date order, one row per event or span:

| Column | Holds |
|---|---|
| **When** | the date or span, and the chapter the narrator's thread is in |
| **Where / doing** | where they are and what they do |
| **Knows** | what they know that bears on the plot, and from whom (new knowledge in bold). For a group, the channel: their own eyes, an agent, a witness |
| **Wants** | what they are after, and what they fear |
| **Trace** | what the narrator could see of it, or "none" |
| **Source** | the outline, note, draft or ruling it rests on, quoted |

A row with no source is a tween, marked *(Proposal.)*.

## The loop

1. **Extract** (one agent per actor, read-only): every line in the horizon's outlines, notes, drafts and cards that says or implies where they are, what they do, know or want, with its quote and date.
2. **Check** every quote; drop what does not resolve.
3. **Build** the log in date order.
4. **Audit** with [the three critics](#the-three-critics), and for **no trace** (a long run the narrator could have glimpsed and did not).
5. **Fill the gaps** with proposed rows, and rank every fault and fix by page impact:
   - (a) a fault whose fix changes an outline line, or who knows what, when, or who is present;
   - (b) a stale line that a newer ruling already overrules;
   - (c) a tween that changes no line.

   Only (a) goes to the writer, through `interview.md`, with the character critic's flags. Strike (b) at once by the newer ruling. Write (c) into the log as a reading, listed in the task but not asked, since a drafter never sees it.
6. **Check acceptance:** every beat the actor drives on the page traces to a row; nothing left open in `interview.md` without the writer's ruling.

**The log is never on the page.** The narrator sees only its traces. A reader is never put inside a character the narrator only watches.
