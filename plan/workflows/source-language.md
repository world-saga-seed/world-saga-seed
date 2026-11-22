# Source language: a book made from a work in another language

*Speciality. Add this when the book is made from a source in another language (a translation restored against its original, a retelling from a foreign text).*

## Purpose and when

A run that reads a French source all day starts writing French: a clause in the narration, a card's keywords, a note's heading. And a translation's departure lists, made by aligning it to the original, undercount what a patch has to fix. This workflow keeps the working language clean and the patches whole.

**Grade.** The sweep is mechanical (`tools/foreign.py`); sorting its finds and judging a translated line are judgments.

## The working language

`CLAUDE.md` names it ("Working language"). Everything the run writes is in it: prose, cards, keywords, notes, the ledger, reports. The source language appears only inside quotes, each one cited to its file and line, so `tools/quotes.py` can check it. A name keeps the form the book prints (the cards hold the forms).

## The sweep

1. **Find:** `python3 tools/foreign.py story/ world/ plan/ --lang fr` (or `de`, `es`, `it`; `--words LIST` for another language). It lists every unquoted run of the source language, setting aside quoted text and the kit's `- quote:` lines.
2. **Sort** each find: a quotation that lost its marks (restore them, with the cite), a name (keep it), or drift (put it in the working language). A cheap finder may sort; a script or a stronger reviewer applies.
3. **Review the applied lines,** and keep only a review that stays in the working language. A reviewer asked to judge a translated line tends to put the source back: in the run that found this, 149 of 176 suggestions did.
4. **Run it again** until it prints only names and the quotations you keep.

## Patching a translation against its original

When an old translation is restored against the original, its departures (cuts, summaries, mistranslations, print slips) are patched one by one, each a row with the old and new text. An alignment that lists the departures chapter by chapter is a start, not the list: in the run that found this, the alignment listed 7 departures in one chapter and the patcher and its critics needed 63.

- **The patcher reads the chapter whole against the original,** using the alignment's list only as a start, and lists every departure it finds, with the original's words quoted.
- **Label every departure where the alignment pairs a passage** (each paired passage, not only the first per paragraph), so the count is the text's, not the aligner's attention.
- **A facts critic on each patched chapter** reads it against the original again, and the patcher's list is checked against the critic's finds; a large gap means the pass read the list, not the chapter.

## Lessons

- **Drift starts in the metadata.** Keywords and headings drift first, since they are written quickest; sweep `world/` as well as the prose.
- **A source's own beat is marked *(Source.)*,** apart from *(Drafted.)* for the writer's prose ([CLAUDE.md](../../CLAUDE.md), rule 2).
