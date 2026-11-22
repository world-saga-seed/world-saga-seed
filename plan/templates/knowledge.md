# Knowledge guard: [head's name]

*Lives at `story/voice/knowledge/<head>.md`.*

*`story/voice/knowledge/<head>.md`, one per narrating head, named by the POV file. What the head knows, what it believes wrongly, and what it does not know, each with the chapter it starts and, where it changes, the chapter it ends. The drafter voices the beliefs on purpose; every critic judges the head's narration against this file before the cards. A wrong line listed under Believes is the narrator's, kept on purpose: never a finding, never corrected. A wrong line listed nowhere is a drafter's slip or a new belief, and goes to the writer to rule. Without it, a critic that knows the world corrects an unreliable narrator into a reliable one. Every entry carries its span as `*From* NNNNN` and, where it ends, `*until* NNNNN`; an entry with no From holds from the book's start. `python3 tools/knowledge.py N` prints the entries in force at chapter N, which is what the drafter and critics are given; an entry that ends at N is marked as turning in that chapter. One file per head, never a copy per chapter: copies drift. Fill in each line; delete the guidance.*

## Knows (true)
- [What the head knows.] *From* [NNNNN]: [where they learned it: seen, told by whom, lived]. *until* [NNNNN, only if they lose it].

## Believes (wrong, kept on purpose)
1. [What the head believes, in their words.] *Truth:* [what is so, with its card or key entry]. *From* [NNNNN] *until* [NNNNN, where it is corrected; leave it off if never]. *Reader:* [must not see through it / may / should, and by which clue].

## Does not know
- [True things kept from this head, by key entry where there is one.] *until* [NNNNN, where they learn it; leave it off if never].
