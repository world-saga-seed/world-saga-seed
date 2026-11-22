# Scene outlines: deconstruct existing prose, outline the rest

*Basic.*

Puts an arc into one form so it can be read, sorted and marked up together. **Drafted prose is taken apart** into a scene outline (this is how a writer's existing manuscript enters the method), and **undrafted beats are outlined fresh**.

**Grade.** A judgment. Agents propose; the writer marks up. Nothing here edits prose. Output goes to `story/outline/` and `story/notes/`, marked.

## The form

- **Outline** (`story/outline/NNNNN-slug.md`): a title, `# <Name> (outline)`; one paragraph saying where it sits, the narrator and tense, and how points are marked; then `## Outline`, numbered `### N. <Beat>` sections of short marked bullets.
- **Notes** (`story/notes/NNNNN-slug.md`, same number): `# <Name> (notes)`; `## Notes for drafting` (what the scene does, where it sits, cast, words, pacing, length, clues); `## Open and flags`.
- Marks: *(Drafted.)* for what the writer's existing prose holds; *(Source.)* for what a third-party source holds (a public-domain original outlined beat by beat); *(Settled …)* for what the writer ruled; *(Proposal.)*; *(My reading, to confirm.)*.

## The loop

1. **Open a task** naming the arc, its settled order, and the file list with one number per chapter.
2. **Fresh agents, at most two,** each owning a contiguous span, so a span's hand-offs are one hand's. Each has its own scratch folder.
3. **Verify:** every quote resolves (`tools/quotes.py`), every link resolves, every beat is marked, and each file's first and last beats meet its neighbors'.
4. **Present** to the writer as one list in story order, with each file's open questions, and the drift the deconstructions found.
5. **Fold back** the writer's markup. Log the run; add lessons here.

## Prompt D: deconstruct

> You are taking drafted prose of a novel back into a scene outline, in the folder {REPO}. Read `README.md`, `plan/README.md`, `plan/workflows/scene-outlines.md` (the form), the example outline {SHAPE}, `story/voice/voice.md`, and your drafts in full: {SOURCES} (read-only). Write only {FILES}. Run no git commands; do not launch agents. For each draft: (1) the beats the prose actually holds, in order, each marked *(Drafted.)* and anchored by a short exact quote; (2) where the notes say something the prose does not do, or the prose holds something the notes lack, mark it; (3) **drift**: every place the prose disagrees with the notes or cards, quoted on both sides; (4) the notes for drafting; (5) open and flags. Do not judge the prose and do not rewrite it. Keep lore in the notes. Verify every quote with `grep -F`. Finish with a short report: beats per file, drift, open questions.

## Prompt O: outline

> You are writing scene outlines for undrafted chapters of a novel, in the folder {REPO}. Read `README.md`, `plan/README.md`, this workflow (the form), the example outline {SHAPE}, `story/voice/voice.md`, the sheets of the main characters, `story/voice/banned.txt`, the settled order in {ORDER}, and the cards each beat uses. Write only {FILES}. Run no git commands; do not launch agents. Build each outline from what the notes settle first, quoted and marked; fill the tweens with marked *(Proposal.)* beats; never present an invention as settled. Hold to the book's rules: the narrator's reach (what they can see and know); chance with a cause, not convenience; lore in the notes, not on the page; the setup check (no beat arrives on cue without a cause; see [outline critics](drafting/critics.md#outline-critics)). If the book uses comedy, give each scene's comedy a quiet, build, release shape. Outline only; dialogue only as gist, in italics. Verify every quote. Finish with a short report: beats per file, proposals made, open questions, and a key-frame grade per chapter: **yes** (the writer has settled the chapter's main beat), **thin** (a beat is named, but not how it plays) or **none** (no writer-settled beat).

## Prompt J: resolve by judgment

*Only when the writer asks, or is away.*

> For every open item in your files: write two or three explanations, each built from what the notes settle, quoted; pick the most probable and say why in one line; record the runner-up; apply the pick, marked *(Resolved by judgment, {DATE}; overturnable.)*. **Hold** an item, marked *(Held for the writer.)*, when the pick would change the story (a death, a betrayal, a reveal, who knows what). Leave settled lines alone. List seams with neighboring files last.
