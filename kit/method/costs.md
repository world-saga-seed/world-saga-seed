# Costs: tokens, time, and how much a chapter reads

*Measured on the series the kit came from. The wiki's [Before you start](https://github.com/world-saga-seed/world-saga-seed/wiki/Before-you-start) links here; these are the figures a session inside the clone can read.*

## A pass, a chapter, a volume

One pass over a chapter of 2,000 to 5,000 words (the drafter, then the critics) took 350,000 to 600,000 tokens and about 15 to 25 minutes of Claude working on its own; you need not watch. A chapter usually takes more than one pass: a revision and a second check bring it to about a million tokens, and reruns add more. A volume of twenty chapters runs to tens of millions.

- **On a Pro or Max plan** this draws on your usage limit, not a bill, and a volume will not fit in one day's allowance.
- **On the API,** at Claude Opus 5.5's listed price (checked on 2026-11-15: $4 per million tokens read, $20 per million written, and much less for text read again from cache), a pass costs at most a few dollars. Most of what Claude reads is read again from cache, so a volume comes to tens of dollars; with nothing cached it could reach about $100.
- **Your own time** is the interview, your key frames, and reading and ruling on what the critics find. It has not been measured yet; if you test the kit, log yours.

## What a chapter reads

On the same series, about 300,000 words of drafted prose stand on about 1.75 million words of lore: some 520,000 in about 600 cards, 450,000 in notes and character sheets, 570,000 in outlines (drafted chapters and some seventy ahead) and 200,000 in calendars, with the ledger of the author's rulings a further 300,000. No run reads it all. A drafter or critic run reads 150,000 to 200,000 tokens (roughly 110,000 to 150,000 words, so some 30 to 40 words read for each word written), and the brief and its named file list choose that slice, under a tenth of the lore. That intake has stayed flat between runs on the first volume and runs on the third, while the lore kept growing. A chapter's own outline and notes are small, usually one to two and a half times its prose; nearly all of a run's reading is the cards, sheets and earlier chapters the brief names. So the thing to watch as the book grows is how much each brief names, more than how big the lore gets. Log each run's tokens and look for a rise.

## Measure your own

Prices and limits change, so measure: render one chapter, then type `/usage` in Claude Code (or check the bill) to see what share it took, before you start a volume. The token log (its form is [plan/templates/tokens.md](../../plan/templates/tokens.md)) records what each step cost on your book.
