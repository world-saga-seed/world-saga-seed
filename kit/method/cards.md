# Cards: one fact, one home

## The rule

Each fact about the story lives in exactly one file. Every other file that needs it links there. When the fact changes, it changes once.

The files that hold facts are **cards**: one short file per person, place, object or rule, in folders under `world/` (`world/people/`, `world/places/`, `world/things/`, `world/animals/` for a named creature or a species the book describes, and whatever your book needs). Larger subjects that many cards lean on (how the town's year runs, how the law works) get **topic files** at the top of `world/`.

The main characters get fuller **character sheets** in `story/notes/characters/`.

## The card head

Every card opens with the same five lines, so a script can check it and build the index:

```
# The mill ford: the crossing below the mill

*Knee-deep in a dry summer, shut for days after heavy rain; a rope strung between two posts.*

Keywords: river, crossing, shallows, wading, flood, rope
```

- **Line 1:** the name, a colon, what it is.
- **Line 3:** one italic summary line.
- **Line 5:** keywords: the words a search would reach for that the card does not already use. When a search misses a card, add the missed word here.

Each card folder's `README.md` holds an index table built from the heads by `tools/cards.py build`. Nobody edits the table by hand.

The first cards come from the writer's existing work, by [card-existing](../../plan/workflows/card-existing.md): each named person, place and thing, marked, with the quote it comes from.

## One version of each concept

A card is refined through discussion. The writer talks an idea through several times until the pieces fit. Once they fit, the card holds **one** clean statement of the result: one sentence, one mark. Not the first version, then the correction, then the reading of the correction. Several versions of one thing on a card is mud.

History lives in git. A card that has been cleaned says so at its head: *(Distilled from abc1234.)*, and that commit holds the longer past.

Write tight. Every word on a card is read by every agent that opens it.

## What a card holds, and what it does not

- **It holds** what is true about the thing, what the page shows of it, who uses it, where it appears, and what is still open.
- **It does not hold** a scene. Story beats go in the outline. A card holds what is true of its subject (its nature, traits, skills, possessions, relations, and the dated changes to them); "he asks whether the engineer can swim" is an event, and stays in the outline, and the card says at most which chapter changed something.
- **It does not restate** a rule that lives on another card. It states the consequence and links the home.
- **Lore stays in the notes.** A card can hold far more than any scene shows. That is the point: the detail is there for later scenes to draw on. Do not treat a long card as a pacing problem.

## Stubs: card what recurs, stub the rest

Carding a long work in full spends most of its tokens on things no scene will use. A thing met in one chapter that is no clue gets a **stub**: the card head, a line `Stub: build when a scene needs it.`, and the lines that cite it. A full card goes to what recurs (two or more chapters) or is a clue. Before a chapter is drafted, any stub its outline or notes link is built from its cited lines; `tools/reading.py` names each linked stub and lists it to build first.

## Big cards open with an index

A sheet or card too long to read whole opens with **At a glance**: a few lines, each linking to the section that holds the detail. An agent reads that first and opens only the section its task needs.

## Common causes have one home

When two or more cards lean on the same mechanism (the ford shuts because the hills drain into the river; prices rise every winter because the road closes), that mechanism has one home card. Every other card states its consequence and links the home. A card that states the cause differently from its home is a contradiction, and gets fixed.

## Drafted details get carded

A drafter will invent small things: the carter's pony, the name of the inn, the stair with a loose tread. If the next drafter does not know, the stair will be in a different place in chapter nine. So, once [draft-cards](../../plan/workflows/draft-cards.md) is in use (a Refinement), the invented people, objects and places are carded after each drafting batch, marked *(Proposal, from the draft, 00400.)*, with the quote. The writer can strike any of them, and then the prose is fixed to match.

## The world is no fool

A card that explains why something in the setting is backward, slow or strange gives the right strategy under the setting's rules, never ignorance ([craft.md](craft.md#causes-not-convenience)).
