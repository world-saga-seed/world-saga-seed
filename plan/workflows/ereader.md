# Ereader: the writer reads the volume as a reader would

*Refinement. Add this when a stretch is long enough to read as a book.*

## Purpose and when

Drafted volumes go to the writer as EPUB books. The writer reads them on an ereader, as a reader would meet them, not as files, and comes back with comments. This is how a volume reaches the writer's markup.

**Grade.** The build is mechanical: it reproduces the prose files or it does not. Filing the comments is a judgment.

Run it when a volume (or any stretch the writer wants to read) is refined. Build once; while the writer is reading and sending notes, do not rebuild after each fix. Rebuild when the notes stop, and say so.

## Build

```bash
python3 tools/epub.py --title "Volume 1" --author "Your Name" --series "Your Series" --index 1 \
    --front story/volume/front-matter.md \
    --prose story/prose --outline story/outline --from 100 --to 2000 \
    --out build/volume-1.epub
```

- **What goes in:** each prose file's text only. The draft tag in the title and `<!-- comments -->` are dropped; `---` becomes a scene break.
- **Gaps show:** with `--outline`, a chapter that has an outline and no prose gets a "[Not yet drafted.]" page under its title, so the gaps fall where they will be.
- **Front matter:** `--front` sets a page before the first chapter (only what follows its first `---`, so the top of the file can hold writer-side notes). **A later volume opens on the story so far** (the interest check's recap), so a reader who comes back after a break is not lost.
- **Series metadata** groups the books on readers that support it.
- **Tracing a comment back:** each chapter is its own page, and every paragraph carries its source line as an id (`p87` is line 87). A highlight names its page; its quoted text finds the line.
- **Kobo readers:** every build also makes the `.kepub.epub` when kepubify is installed (`--no-kepub` to skip it); send the `.kepub.epub`, which the device's own renderer reads with the reader's settings. Put only one of the two files on the device.
- Keep `build/` out of git.
- Check a build with epubcheck if you have it.

## The read: comments from the phone

The writer reads on the device and types comments on a phone as they go, into a Claude Code session running in the book's folder. Claude files each one as it lands, so nothing waits for the end of the read and nothing is lost to memory.

### Before the read

1. **Build** the volume (above) and put it on the device: copy it over USB, or by the device's own send-to service. Check that it shows up in the device's library before the writer sits down.
2. **Start the session on the computer,** in the book's folder, with Remote Control on: `claude --remote-control "Volume 1 read"` (or `claude remote-control --name "Volume 1 read"`). Open the session in the Claude app on the phone, or at claude.ai/code. The session runs on the computer, with the book's files; the phone only types and reads.
3. **Open a task for the read** (`plan/tasks/task-YYYYMMDD-NN-volume-N-read.md`) with the build's commit hash, so every comment is filed against the text the writer actually saw.
4. **Tell Claude the read is starting:** "I'm reading volume 1 from the ereader. File my comments; don't change prose during the read."

### The comment form

Short, so a phone can carry it. One comment per message is easiest, but several in one message are fine:

```text
01200 "the long climb to the gate" pacing: drags here, the climb goes on too long
01400 lore: the ferry runs twice a day, not once
01300 reshoot: she would never say this to her father's face
01200 "as other people say grace" line: too knowing for him
01500 q: does he know about the debt yet?
```

- **Where:** the chapter's number or title as the device shows it, and a few words copied from the page if the comment is about a line. Claude finds the line by those words.
- **Kind:** `lore` (a fact wrong or missing), `pacing` (slow, rushed, skimmed, confusing), `reshoot` (the scene is wrong, not the words), `line` (a wording), `q` (a question for Claude). Leave it off and Claude infers it.
- **Phone typing is fine.** Autocorrect swaps words. Claude reads each comment by the scene it points at, and asks only when a misread word could change a ruling.

### How Claude files each kind

| Kind | Claude does | Lands in |
|---|---|---|
| **lore** | Greps the cards for the fact and quotes what they say. A new or corrected fact is a ruling: ledger row first, then the card, then a grep of the drafts for the old fact | the ledger; the card; a drift row in `plan/state.md` for each draft that now disagrees |
| **pacing** | Finds the passage, quotes it, and notes whether it holds a clue (never trimmed, only made livelier around) | the chapter's Next pass list; the read task's pacing list, for the trim pass or the next interest check |
| **reshoot** | Reads the chapter's outline and notes for what the scene was meant to do, and writes the question the reshoot raises | the outline, as a reshoot note; a brief for [dictation](dictation.md) if the scene needs the writer's new frame |
| **line** | Quotes the line | the Next pass list, as a reading item |
| **q** | Answers from the cards and outlines, quoting each source; "not in the notes" when it is not, and the question held | the reply; `plan/state.md` "Questions held" if open |

**Reply in a line or two per comment,** so the phone screen holds it: what was filed where, and any question back. For example: "filed: lore, the ferry card says twice a day and 01400 says once; ledger row added, 01400 on the drift list. Was it ever once, in winter?"

**No prose changes during the read.** The writer is reading one build; changing the files under it breaks the trace from comment to line. The exceptions are the ledger and cards, which a lore comment changes at once.

### After the read

1. **Summarize** in the read task: comments by kind and chapter, the rulings made, the questions held, the reshoots proposed.
2. **Put the open questions and reshoots to the writer** at the keyboard, a few at a time, each with a recommendation.
3. **Fix as a task:** reshoots through dictation and the drafting chain, and a reshoot's new beats go into the outline and through the [three critics](actor-log.md#the-three-critics) (the light pass, on the changed beats) before the redraft, since the prose critics judge the page against the outline and never ask whether the people would do it; trims and line fixes through the reviser, from the Next pass lists. Then rebuild once and say so.

### From the device's own notes instead

A writer who prefers to highlight on the device: export the highlights and notes (most readers store them in a database or an export file: the book, the page, the highlighted text, any typed note), and file each the same way, by its highlighted words.

## Lessons and failure modes

- **Set an explicit base font size** in the stylesheet (`html` 100%, `body` 1em). Without one, some readers render a sideloaded book at a very different size from their other books.
- **A copy on the device may not appear until the device imports it,** usually on disconnect.
- **Keep comments traceable** to page and paragraph, or filing them becomes guesswork.
- **File as the comments come.** A writer who saves comments for the end remembers the last chapters best and the first ones vaguely; a comment filed at once keeps its place.
- **A reading session loses its place if it is closed.** Keep the Remote Control session open for the whole read; `claude remote-control --continue` reattaches to the last one in the folder within a few hours.
