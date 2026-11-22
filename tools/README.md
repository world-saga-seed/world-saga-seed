# Tools

Twenty-four small Python scripts. Standard library only (Python 3.8 or later), no paths written into them, everything set by arguments. Four of them (`sounds.py`, `refrains.py`, `scale.py` and the banned-word scan in `tells.py`) read the page through `context.py`, the shared reader and pattern matcher, so keep it in the same folder as they are; a fix to how a chapter is read, split into sentences or searched is made there once. They come with the clone, in `tools/`; run each from the book's top folder. Every script answers `--help`.

They give the method its mechanical checks: verdicts nobody argues with, under every judgment a critic or reader makes. **Try each one on a case it must catch before you trust a clean result from it** (a planted broken link, a planted banned word).

Every script is tested as code, on a planted case in the kit's `example/` (the list is at the end). Only `scale.py` has also been proven on a real book's prose, against planted faults and in a sweep; the rest are proven as code, not yet as craft.

They come in three levels. Start with the basic ones; add the refinement checks when a draft stands; take a speciality tool only when your book needs it.

### Basic

*For every book and every chapter: the links hold, the cards are in form, each run's reading list, quotes that are really in the text, and an ereader build to read from.*

| Script | Does | Typical run |
|---|---|---|
| `links.py` | counts broken links (missing file or missing `#heading`) in every `.md` file; skips web links and links inside code | `python3 tools/links.py -v` |
| `cards.py` | checks every card's five-line head, builds each card folder's index table from the heads, finds cards by word, writes the subject index; checks each kind's fields, gets fields from cards by name, question and mark, and checks a card's integrity | `python3 tools/cards.py check` · `build` · `find tide` · `index` |
| `reading.py` | one chapter's reading list: its outline's and notes' links resolved to files and line ranges, the cards and sheets it names, the chapter before, the digest | `python3 tools/reading.py 00400 --step facts --digest story/volume/1-digest.md` |
| `quotes.py` | checks that every quote in a report is really in the text it quotes | `python3 tools/quotes.py findings.md --in story/prose/00400-*.md` |
| `epub.py` | builds an EPUB of chosen chapters, each paragraph tagged with its source line | `python3 tools/epub.py --title "Volume 1" --out build/v1.epub story/prose/00*.md` |
| `tokens.py` | a session's token totals (input, cache written, cache read, output; by model; the agents inside it apart) from its Claude Code transcript, as a row for the token log; a call written as several lines counted once | `python3 tools/tokens.py ~/.claude/projects/BOOK/SESSION.jsonl --step "session close" --log plan/tokens.md --append` |
| `check_commit.py` | refuses a commit that stages a recording, anything under `tmp/`, a Zone.Identifier file or a file over 10 MB; setup installs it as the pre-commit hook | `python3 tools/check_commit.py` |
| `check_clean.py` | checks that a book cloned from the kit has nothing left of the example: no `example/`, no name from it, no link into it | `python3 tools/check_clean.py` |

### Refinement

*For the prose over a volume: the model's texture and habit words, phrases and refrains repeated across chapters, setting words used before they are set up, and old drafts carried into a redraft. Run them once a draft stands, before the critics.*

| Script | Does | Typical run |
|---|---|---|
| `tells.py` | texture numbers for chapters (similes, "and" chains, negations, sentence spread, kicker endings, short-sentence clusters, triplets), each against the voice samples with `--sample`, and a scan for banned words | `python3 tools/tells.py story/prose/00400-*.md --banned story/voice/banned.txt` |
| `repeats.py` | phrases of 5 to 8 words found in N or more chapters, and stock patterns counted per chapter | `python3 tools/repeats.py story/prose/0*.md --min-files 3 --narration` |
| `refrains.py` | a volume's refrains counted per chapter from a watch list, and sentences repeated near word for word in three chapters or more | `python3 tools/refrains.py story/prose/01*.md --list story/voice/refrains.txt --batch 3` |
| `stutters.py` | the same short phrase twice within a few paragraphs of one chapter, a capped frame ("as if", "the way X") twice in a paragraph, and the chapter's count against each cap | `python3 tools/stutters.py story/prose/00400-*.md --clues plan/reread-hooks.md` |
| `context.py` | every match of a pattern with its sentences or paragraphs around it, by line: a rule from your rulings checked by script ("ties" unless "black"), or the windows a cheap judge reads instead of whole chapters (every mention of a character, for one judge holding their sheet) | `python3 tools/context.py story/prose/*.md --patterns plan/guards.tsv --fail` |
| `firstuse.py` | words a chapter is the first to use that the cards use too: setting words that may need setting up | `python3 tools/firstuse.py story/prose/*.md --batch 1` |
| `aged.py` | outline, note and card lines that may carry an old draft into a redraft | `python3 tools/aged.py story/outline/00*.md --cutoff 2027-04-01 --retired story/prose/00*.md` |
| `gaps.py` | each critic finding traced to the drafter's bundle (given, field not given, not included, chapter, rules, earlier page), and the includes and fields to add so the next draft gets the fact | `python3 tools/gaps.py critics/*.md --manifest plan/records/drafting/00400-bundle.tsv --rules story/voice/voice.md --chapter 00400` |
| `uses.py` | when a card changes, the drafted chapters whose bundle gave the changed field, and the lines of their pages that name the card: where to look again | `python3 tools/uses.py --manifests plan/records/drafting --since HEAD~5 --called plan/workflows/cards/called.tsv` |
| `sizes.py` | what is too big to work with: fields over 500 words (the distill answer test), cards over 3,000, outline and design files over 8,000 (to page); with saved manifests, each field marked with the chapters that read it | `python3 tools/sizes.py [--manifests DIR]` |

### Speciality

*For some books only, by what the book does: a viewpoint whose size is not an adult's, sounds written out in letters, a chapter's beats marked by source, several viewpoint heads, a narrator who knows less or believes wrongly, and a change sent back to the kit.*

| Script | Does | Typical run |
|---|---|---|
| `scale.py` | the viewpoint's height and body landmarks at a chapter, and every size phrase on its page, with repeats of the crowd-from-below view within two chapters marked | `python3 tools/scale.py 00400 --height 139 --other Ada=141 --prose story/prose` |
| `sounds.py` | every sound span (phonetic letters between slashes) with its line, speech or narration, earlier uses and forbidden symbols; flags a volume where the device is rare | `python3 tools/sounds.py story/prose/*.md --batch 3 --forbid "ɒ ː ɹ"` |
| `attribution.py` | unlabeled paragraphs for a blind attribution test in a book with several viewpoint heads, and the key to score it | `python3 tools/attribution.py story/prose/03*.md --heads "03100-x.md:1-40=Ada,03100-x.md:41-200=Ben" --out attribution.md --key key.md` |
| `knowledge.py` | the knowledge-guard entries in force at one chapter (what each narrating head knows, believes wrongly and does not know), for the drafter's and critics' briefs | `python3 tools/knowledge.py 00500 --out tmp/knowledge-00500.md` |
| `markup.py` | a chapter as local HTML coloured by whose beat each passage carries (keyframe, assisted, tween), the clues highlighted, lore underlined, every source in a tooltip, from the finds of cheap locators ([markup](../plan/workflows/markup.md)) | `python3 tools/markup.py items 00400` · `render 00400` |
| `check_leak.py` | checks that a change meant for the kit carries nothing of your book: names from its cards and sheets, runs of words from its prose and notes, email addresses ([CONTRIBUTING](../CONTRIBUTING.md)) | `git diff upstream/master \| python3 tools/check_leak.py --book ../my-book` |

## Notes on each

**links.py.** `--root DIR` checks another folder; `--exclude 'existing/*'` skips files (repeatable). Exits 1 when anything is broken, so it can stop a script. A heading's anchor is made the way common markdown viewers make it: lower case, punctuation dropped, spaces to hyphens, a repeated heading gets `-1`, `-2`.

**cards.py.** Card folders are the subfolders of `--root` (default `world`). The head form and the table markers are at the top of the script. `check -v` also lists keywords the card's text already uses (a keyword should be a word a search would try that the card does *not* already contain).

**cards.py fields, get and integrity.** A card's **fields** are its top-level list items that open with a bold label and a full stop (`- **Body.** ...`), before its second `##` heading.
- `fields FORMS` checks each kind's cards against a forms file (`world/beast<TAB>Body; Size?; Threat; Name`, a `?` for optional). A field missing or out of order is a problem; a label the form does not name is listed as the card's own, not a problem.
- `get CARD ...` prints only what is asked: `--fields` by name, or by question through `--aliases` (`size`, `usage`, `danger`: one row for each kind's own fields); `--settled` keeps only settled and unmarked text; `--strip links,marks,ids` cuts the annotations an agent that only checks facts does not need. Its first line says what was cut. `--table` gives one row per card and a column per field or question, each cell cut to `--cell` words (default 30); with no `--fields` it is a brief index, each card's name and first field. A critic that searches (sizes in a scene, which beasts are dangerous) reads the table and opens a card only when a row needs it. `--sections FILE` (for `fields` and `get`) maps a card's field to where that card keeps it: its own `##` sections, a field of its own under another name (`**Danger**`), or `-` where the field does not apply. A long sheet keeps its voice in sections; the map lets the check pass it and lets `get` pull those sections.
- `integrity` checks what an agent must be able to trust: the head, the fields, the links (to the heading too), every ruling ID cited in the ledger, no task cited. On a card whose head says it is finished (`--finished`, default `Distilled from|Finished`), it also fails a proposal left or a field with no status mark. It lists, to check, Appears in against the prose both ways and runs of words two cards share.

**tells.py.** Prints a `knot` line under a file's numbers for each narration sentence of 35 words or more holding a semicolon. Measures **narration** only: text inside double quotes (straight or curly) is set aside. Stops at a line starting `## Notes` (change with `--stop`). The banned list: one word or phrase per line, matched as whole words, case ignored; `re:` starts a regular expression; `#` starts a comment. `--all-text` scans dialogue for banned words too. `--count NAME=REGEX` (repeatable) also counts a habit of your own narrator in narration, per 10,000 words: a word the narrator leans on, or a gesture. `short/k` and `run` are the short narration sentences (under 8 words) per 1,000 words and their longest run in a row; `trip/k` is rhythm triplets ("dry, warm, and snug") per 1,000 words, lists of things included. `--sample FILE ...` (the voice samples, pooled) prints under each chapter an "over the sample" line where short/k, run or trip/k runs well past the samples' own, and a "spelling" line for each word the samples spell another way. **There is no universal good value for any number:** run it on the writer's own pages and use their range.

**repeats.py.** Give the chapters in reading order. `--skip-title '^# Interlude'` leaves out pieces in another voice. `--tics FILE` replaces the built-in pattern list with your own (one per line: `name<TAB>regex`). Sort what it finds: motifs keep their words, habits keep the gesture, tics go.

**cards.py index.** Writes `world/INDEX.md` (with `--root DIR`, `DIR/INDEX.md`): every card under its name, the parts of its "what it is" and each keyword, every folder's README title, and every character sheet (`--sheets DIR`, default `story/notes/characters`), A to Z. Rebuild it whenever heads change; a missing subject is fixed by a keyword on the card's head, never in the index.

**refrains.py.** Give the volume's chapters so far, in order; `--batch K` makes the last K the batch, so a repeated run is reported only when it reaches the batch. Thresholds: `--volume-max` (default 8) and `--chapter-max` (default 3). The repeated runs skip six-word runs made mostly of small words and join overlapping runs into one. `repeats.py` finds shared phrases across any files; this one is aimed at a volume's refrains and at whole descriptions repeated.

**context.py.** For a check that hangs on a word. Give patterns (`--pattern LABEL=REGEX`, or a file of `LABEL<TAB>REGEX` lines with `near=`, `unless=`, `within=` and `narration=1` options) and it prints each match with its window: `--before`/`--after` sentences, or `--para N`, the match's paragraph and the N before it (use 2 when the grounds of a claim must come before it). `--near` keeps a match only when a second pattern is within `--within` words; `--unless` keeps it only when one is not, which states a rule ("a ribbon" unless "blue"). `--narration` matches outside dialogue. A guard file run with `--fail` exits 1 on any match. `--tags` prints a position tag under each match for a later tool to find the edit point: `@ file:line:col-col anchor=«…»`, where the anchor is the shortest run of words around the match (at least `--anchor-min`, default 4) found only once in the file, so it still finds the spot after the lines above it move; it is the unique string an edit replaces. `--jsonl` gives one record per match (file, line, col, end, label, match, anchor, unique, window) for a script or a judge's harness. The last line says how many words the windows hold against the whole: a judge given the windows reads that fraction. A match is a candidate: read the ruling's scope before calling it a breach. A fault that leaves no mark in the words, such as a claim with no grounds on the page, still needs a reader.

**stutters.py.** The other repeat tools see a volume; this one sees a page. It lists every run used again within `--window` words (default 250): three words with two that are not filler, or longer runs. A run used `--standing` times or more in the chapter (default 6) is a name or a tag and listed apart. `--clues` takes your clue register or a chapter's planted lines and marks a hit whose words are in one. `--notes DIR` adds each chapter's own notes (the files in DIR whose names start with the chapter's number) to its clues. It finds candidates; you judge them, and rerun after the fix.

**sounds.py.** Give the whole book so far, so a span can be checked against earlier chapters; `--batch K` reports the last K files and `--volume V` sets the last V files as the volume for the rarity flag. `--span` and `--chars` change what counts as a span, for a book with its own notation. A span inside double quotes counts as speech.

**firstuse.py.** `--cards DIR` (default `world`) is the folder whose words count as the setting's; `--min-cards N` (default 3) how many cards must use a word. Expect plain words among the hits; the critic sorts them.

**reading.py.** Run from the book's top folder; reads `story/outline/N-*.md`, `story/notes/N-*.md` and `story/prose/`. A linked file over `--large` words (default 1,500) is listed by the sections its links name, with line ranges. A file over `--large` whose listed sections are 90% of it is listed whole. A card counts as named when the outline or notes use its name or (for a two-word proper name) the first name; named cards are listed apart, not to read (`--named read` reads them, for a book whose notes link little; `--named off` leaves them out). Keywords do not count: they are search words and match far too much. For a drafter or setup critic, a long sheet is read by `--sheet-sections` up to `--sheet-budget` words (default 2,200); a sheet's own subfolder counts only when linked. `--not-before` keeps a pattern (fragments, say) from being taken as the chapter before; `--samples` and `--rules` name your style samples and rule files. `--step` gives each critic its share.

**reading.py --bundle.** Prints the text a role reads instead of a list of files: each linked card's fields cut by the role's recipe, the sections the chapter links on a card without fields, the sheets' sections, and the rules and prose still as files. The built-in recipes:
- the drafter keeps proposals and marks, so it knows what it may not change;
- the facts and procedures critics get settled text only, with link targets, marks and ruling IDs cut;
- every role but habits and scale drops the bookkeeping fields (Appears in, Origin and lineage, History, Open);
- the habits role gets only Habits;
- scale gets only sizes.

`--inline` puts the chapter's outline and notes in the bundle instead of naming the files. They are cut for the role: the navigation line, struck text (`~~withdrawn~~`), parentheticals that only cite a source, and every section whose heading matches `--drop` (default: author-side, reference, notes for markup, note changes implied, cards), plus the role's own cuts. The drafter never sees author-side text: a passage marked `*(… author-side …)*` is cut from its mark to the next mark, in the chapter and on every card and sheet. A mark that makes only a figure author-side ("the count author-side") keeps its text. The critics keep author-side text, so they can check the draft against it for leaks and conflicts.

The drafter's pull has no paths: a path is an invitation to open a file or grep, and a raw file holds what the bundle cut. Each card or sheet is headed by its name and kind, its fields come as `Field: text` in the form's order, and the header tells the drafter that everything is there and that a missing fact is a question for its report. The pull also holds only the book so far. A chapter number on a trait says where it is shown, not when it became true, so traits stay. What goes is the page from this chapter on: a quoted line from this chapter or a later one, a line marked "from the draft" of one, and in On the page fields and instance lists, an item that cites only those chapters. A redraft never reads its own old draft, and no chapter reads ahead. Citations, file names and appearance lists are cut. The critics keep all of it, paths included, because a citation is how they check.

`--recipes FILE` overrides a role (role, fields, sheets, settled, cut). An **include** in the notes, `- [selkie](../../world/beast/selkie.md): Body, Size`, names the fields the chapter needs, and a role that reads everything reads only those. Needs `cards.py` in the same folder.

**reading.py, the drafter's extras.** `--manifest FILE` writes what the bundle gave of each file (`fields: A; B`, `sections: ...`, `whole`, `cited: not given`, `named, not given`, `the chapter, inline`) with a `# commit` line; save one per chapter (`plan/records/drafting/NNNNN-bundle.tsv`) for `gaps.py` and `uses.py`. `--called FILE` (card<TAB>names, `;`-separated) heads each card and sheet by what the page calls it, since a title is your label and can name what the page has not shown yet ("the man from the fork" before the fork). The drafter's blocks also drop Open, Appears in, Origin and History (Name stays: it holds what the page calls a thing), and any field that looks ahead ("In volume 3", "Later"); the critics keep them. An include may name a character sheet's fields too (`- [Ada](characters/ada.md): Who, Habits`; Habits comes as its section when the sheet keeps it as one), and `: cited` keeps any linked card or sheet out of the bundle. The sheets and the section cards the outline links are most of a bundle, so they are where includes save the most. A field label with a comma in it is matched whole. With `--inline`, the drafter loses the author-side sections; every critic keeps them, to check the page against. `--suggest [N]` prints candidate include lines for the notes' Cards heading: cards the outline or notes name, or match by a Keywords word, but do not link. It is a list to choose from, not to paste whole.

**gaps.py.** A finding's `against:` line must name a file; the critic prompts ask for one. A short name (`selkie.md`) resolves to the one file it ends with. A page fact from an earlier chapter the drafter did not read is listed as one to put on its card. A finding is a lead: check it against the page before changing a source.

**uses.py.** `--since REV` compares each card's fields at REV with now; a chapter whose bundle gave other fields of the card, or cited it, is listed apart, since its drafter never saw the change. Lines are matched by the card's name, its Keywords of five letters or more, and `--called`.

**aged.py.** `--ledger DIR` (default `plan/settled/ledger`) dates ruling IDs from the ledger rows, so a line marked only with an old ruling counts as old. `--proposals` also flags every undated proposal. `--tsv OUT` writes one row per flagged line for the agents.

**attribution.py.** `--heads` names whose head each stretch of lines is in; a file with one head throughout is given as `file.md=Name`. It takes at least five paragraphs from each head that has them, then fills to `--count`. The key goes in a file the reader is never given. The prompt and how to score it are in [the attribution test](../plan/workflows/drafting/prompts/attribution.md).

**knowledge.py.** Reads every guard in `story/voice/knowledge/` ([the template](../plan/templates/knowledge.md)), or only `--heads`. An entry is in force from its `*From* NNNNN` (from the start when it has none) through its `*until* NNNNN`; at its until chapter it is printed marked as turning there. An Open section is skipped. One guard per head with spans, never a copy per chapter: when a belief changes, one line changes.

**quotes.py.** Reads quotes from lines like `- quote: the exact words`; with `--backticks`, also from every backticked span (for fold-back lists and card extracts; run it on a file or section that holds only quotes in backticks, or every backticked command will be checked too). Matching ignores spacing, curly against straight quotes, and `*` and `_`. Exits 1 if any quote is missing, and prints "0 quotes found" and exits 1 when the report holds none, since that usually means the quotes are not in the `- quote:` form.

**check_leak.py.** Run from your fork of the kit, never from the book. It reads a unified diff (standard input, or `--diff FILE`) and checks only the lines the change adds. Names are the proper names in the headings of the book's cards (`world/`) and character sheets (`story/notes/characters/`), matched as whole words, case kept; a shared run is `--words` words (default 8) found in the book's `story/`, `world/` or `existing/` text. A hit is not always a leak (a word that is also a name, a stock phrase): Claude reads each one with the writer. Exits 1 on any hit, prints `clean` otherwise.

**check_clean.py.** Run it once, after deleting `example/` from a fresh clone; it must print `clean`. `--root DIR` checks another folder. Each hit is listed as `file:line` with what it found; exits 1 on any hit. The example's names (title, people, places, chapter slugs) are written into the script, with a comment on how to rebuild the list if the example changes; the script does not scan itself.

**epub.py.** Its options and how to use the build are in [plan/workflows/ereader.md](../plan/workflows/ereader.md#build). No cover image (that would need an image library); readers show the title page.

## Tested

Each script was run on the kit's `example/` folder:

- `links.py --root example`: 0 broken; a planted broken link was found.
- `cards.py check --root example/world`: stale tables found before `build`, then 0 problems; `find tide` returns the two cards whose heads hold it, then the one whose text does.
- `tells.py` on the scene and the writer's sample, with the banned list: numbers for both, 0 hits; on a planted file, all three planted phrases found, and the same phrase inside dialogue left alone.
- `repeats.py` on the sample and the scene: one stock pattern counted; on two copies of one file, the shared phrases found.
- `quotes.py` on the facts critic's report against draft 1: 2 of 3 resolve, the invented quote reported missing (exit 1); on the keep list against draft 2: 6 of 6; on a file with no quote lines: "0 quotes found" (exit 1).
- `check_leak.py`: on a diff adding a line that names a person and a place from the example's cards, and an email address, with `--book example`, the full name, the place and the email found; a line about critics found clean.
- `check_clean.py`: in the kit, fails on `example/` (exit 1); on a copy with `example/` deleted, `clean`; a planted example name and a planted link into `example/` each found.
- `cards.py index --root example/world --sheets example/story/notes/characters`: 29 entries, each linking its card; `cards.py check` still 0 problems.
- `refrains.py` on the scene and two planted chapters, with a one-line watch list: the planted refrain counted 6 and flagged over the volume limit and in the chapter that showed it 4 times; a 25-word description planted in all three reported once, as one joined run.
- `stutters.py` on the scene: 3 hits; on a copy with a ten-word run planted again 96 words later and "as if" twice in one paragraph, both found, and a hit marked `clue?` when its words were in the `--clues` file.
- `sounds.py` on the same three, with `--forbid "ɒ ː ɹ ɚ ɝ ɛə"`: the planted span found, in speech, with its forbidden symbol; the volume flagged as rare.
- `firstuse.py` on the same three, `--min-cards 2`: the planted setting words found at their first use (a possessive read as its word); words of the scene itself not repeated as first uses in the later chapters.
- `tells.py` on a planted 62-word sentence with a semicolon: one knot line.
- `reading.py 00400` on the example: the outline and notes, the two cards the notes name without linking, the narrator's sheet, the arc outline listed as not to read; `--step habits` lists only the sheet's Habits section with its lines; a chapter with no outline exits with a message.
- `aged.py` on the example's outlines with a cutoff after its ledger day: the lines marked only by older rulings flagged as aged; a planted "from the draft" line linking a retired chapter flagged for both.
- `attribution.py` on a two-head draft with a paragraph planted in the wrong head's voice: 15 paragraphs, 10 and 5, the planted one among them, the key holding each line and head. A cold reader given the file put all 15 in the right head and named the planted one as wrong for its head.
- `knowledge.py` on the example's guard at 00100, 00500 and 00600: 6, 8 and 6 entries, the right ones; at 00500 the belief and the not-known that end there marked as turning.
- `markup.py` on the example's 00400 with four planted finds: 20 items listed (8 keyframe sources, 12 assisted); three finds placed with their colours, the planted one with words not on the page dropped and listed.
- `tokens.py` on a planted transcript of five lines (one call written twice, one agent call, one call later, one line not JSON): 3 calls, the doubled one once, the agent's summed apart, the bad line reported and skipped; `--until` before the last call keeps 2, a `--since` with no zone read as local keeps 1, a `--since` after them all exits 1; `--append` adds one row under the template's header.
- `epub.py`: a numbered build with one drafted chapter and one placeholder, and a file-list build, with the `.kepub.epub` made by default; every XML part parsed as well-formed.
