# Dictation: key frames for a chapter that has none

*Refinement. Add this when a chapter is graded thin or none.*

The writer dictates the scene a chapter needs, and Claude cards it as key frames. Claude's work is the brief before the dictation and the carding after it; neither may invent a beat.

**When.** For every chapter graded **thin** or **none** for key frames, in story order, up to the horizon. In conversation, with the writer at the keyboard. No agents.

## The volume walk

Before drafting a volume, every chapter in it needs a writer's key frame. The walk gets there one chapter at a time:

1. **Grade the volume.** List every chapter in the horizon with its key-frame grade from its outline: **yes** (the writer has settled the main beat), **thin** (a beat is named, not how it plays) or **none**. Put the list in the task, gaps first, then in story order, and show it to the writer: how many of each, and where they cluster.
2. **One gap a session, or as many as the writer has in them,** in story order, by the loop below. Story order matters: each dictation changes what the next chapter starts from.
3. **Regrade as you go.** A dictation often settles a neighbor's beat too. Mark it and skip it.
4. **The writer's own frames come first.** If the writer arrives with a scene in mind for any chapter, take it then, out of order, and card it the same way.
5. **Ripple after every few,** and at the end ([ripple](ripple.md)).
6. **Done when** no chapter in the volume is graded none, and every thin chapter has been offered a brief. The writer may leave a thin one thin, and says so. Then the volume goes to the gate.

Keep a pace the writer can hold. A key frame a day across a few weeks fills a volume and leaves the writer fresh for each scene.

## The loop

1. **Gather what is already settled for the chapter** before writing the brief: its outline and notes, and every paper that settled something for it without landing it in the outline. `grep` the chapter number in `plan/settled/ledger/`, the actor logs and the task papers. A settled beat found there goes into the outline now, under its ID.
2. **The brief,** under 250 words:
   - where the chapter sits: time, place, ages;
   - the state at the start and at the end;
   - the reveals: what may be learned and what is held;
   - the writer's beats already in the outline;
   - what is only proposed, so the writer knows what is not theirs;
   - **three or four questions, each aimed at a character's goal in the scene and how far they push** ("what is she after?", "how far would she push him?"). A recommendation only where the canon supports one.
3. **The writer dictates.** Read it as key frames, in the writer's words. Where a line has two readings, take the one that fits the canon and mark it *(My reading, to confirm.)*.
4. **Answer the writer's questions from canon.** "Does that fit her?" is answered from her sheet and the settled lines, with each source named. When the writer asks how something would be done, give the plain, obvious way first.
5. **The interview** ([arc pitch](arc-pitch.md#the-interview)): scan the dictation for the gaps it leaves (motive, cause, knowledge, the end state, conflicts, what is held) and put them to the writer, a few at a time with a recommendation each, until nothing is open or the writer says "next chapter".
6. **Card it, in order:**
   1. the ledger row, written as the ruling;
   2. the outline: the writer's lines as *(Settled R….)* bullets; Claude's fills as proposals; delete any reading the dictation supersedes; if the scene's order changes, renumber and fix inbound links;
   3. any rule the dictation states, at its home: a setting rule on its card, a drive on the sheet, a voice rule in the voice sheet; forward threads on the chapter that pays them off;
   4. the notes' drift line: what a redraft needs that the existing draft lacks;
   5. `python3 tools/links.py`;
   6. the task log: the chapter, its IDs, one line of what it settled, and the next chapter.
7. **Report in a few lines,** then **offer the next chapter** ("next chapter?"), and give its brief on that word so the loop keeps moving.

## Lessons

- **Dictations reach past the chapter.** Grep the thread before carding, and card each rule at its home.
- **The writer's asides are key frames too.** An aside about where a beat lands later is its own ledger row.
- **After a run of dictations, run a ripple scan** before drafting ([ripple](ripple.md)).
- **A performance skips the checks unless they are run again.** A dictation, or a read-aloud of a drafted chapter that changes what happens, is the writer acting the scene; its beats are new to the outline. Put the changed beats into the outline first, then run the [three critics](actor-log.md#the-three-critics) on them (the character invariant above all: would this person do this?) before the prose is redrafted. The prose critics check the page against the outline, so a beat out of character that came in with a performance passes all of them.
- **A recording stays out of git.** An audio file or a raw transcript of the writer's voice is kept in `tmp/` (ignored) or outside the repository; only the carded key frames, in the writer's words as read, are committed. A recording once committed stays in the history until the history is rewritten.
