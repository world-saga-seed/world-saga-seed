# Intake: the first look at the existing work

*Claude does this alone, before the interview. It changes nothing in `existing/`.*

## Purpose

Know what the writer has before asking them anything. The interview is short and pointed only if it starts from the material.

## Steps

1. **List everything** in `existing/`: file, size in words, and a one-line guess at what it is.
   A folder with a `SOURCE.md` is a third-party text, not the writer's own work: list it as a source with its edition and status, check its files against `SHA256SUMS` (`sha256sum -c`), and keep it apart from the writer's files below: it is a style sample only if the writer names it one, and where it disagrees with the writer's notes, quote both and ask.
2. **Sort each file into a kind:**
   - **manuscript** (drafted prose meant for the book)
   - **notes** (setting, characters, plot ideas)
   - **outline** (a plan of events)
   - **fragments** (scenes or lines without a place yet)
   - **old versions** (earlier drafts the writer has moved past)
   - **other** (research, inspiration, letters)
   - **source** (a text that is not the writer's, in its own folder with a `SOURCE.md`; see [existing/README.md](../../existing/README.md))
3. **For each manuscript:** the point of view and tense; the chapters or scenes in order; the named people, places and objects; the dates or seasons named. Pick the two or three passages that sound most like the writer at their best. These are candidate **style samples**.
4. **For notes and outlines:** the facts they state, and where two files disagree. Quote both sides. Do not decide which is right.
5. **Guess the shape** of the book: how much exists, where it starts and stops, what seems fixed and what seems loose. Mark every guess *(My reading, to confirm.)*.
6. **Draft the interview's first batch:** the five questions that matter most, given what you found, each with why.

## Report

Write `plan/tasks/task-YYYYMMDD-01-intake/intake.md`:

- the file table (file, words, kind, one line);
- per manuscript: point of view, tense, chapters, cast, places, time markers;
- the candidate style samples, each with its file and line;
- the disagreements between files, both sides quoted;
- the shape, as readings;
- the first batch of questions.

Write every quote on its own line in the form `tools/quotes.py` reads, `- quote: the exact words`, so `python3 tools/quotes.py plan/tasks/task-YYYYMMDD-01-intake/intake.md --in existing/*` checks them all.

## Acceptance

- Every file in `existing/` appears in the table.
- Every quote resolves (`tools/quotes.py` or `grep -F`).
- Nothing in `existing/` changed.
- No fact is stated that the files do not hold.

## Common failures

- **Summarizing the plot back to the writer.** They know it. Say what is fixed, what is loose and what disagrees.
- **Choosing between disagreeing files.** Only the writer knows which version is current.
- **Taking an old version for the current one.** Ask which files are live.
- **Picking style samples for polish instead of voice.** The best sample is the passage most like the writer, not the smoothest.
