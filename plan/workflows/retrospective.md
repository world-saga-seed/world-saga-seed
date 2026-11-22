# Retrospective: closing a task, a wave and a session

*Basic.*

A skipped close leaves debris: finished tasks still "Executing", stopped runs whose remaining steps are carried nowhere, rulings never written down, notes citing task papers. Each list runs in order. A step that cannot be done is written down, never skipped silently.

## Closing a task

1. **Resolution:** one paragraph on what was done, what was not, and why. Status: Closed, or Stopped with the reason.
2. **Undone steps** are quoted into the roadmap's Next or Waiting, with the task named.
3. **Rulings** are on the ledger, each as one sentence.
4. **Results are in canon:** facts on their cards (one clean version each), beats in their outlines. `grep -rn "tasks/task-<id>" world story` finds nothing.
5. **Methods are kept:** a procedure worth repeating goes to `plan/workflows/` with its lessons; a script a second task will need goes to `tools/`.
5a. **Update a workflow's status** in [the workflows index](README.md#every-workflow) when the task changed it: a workflow run against a control (planted faults, a key written first) moves up to Tested, and to Proven once it has also been used repeatedly; a workflow used for the fifth time moves from Experimental to Used.
6. **Move the closed task** to `plan/archive/` (Basic). Retire it fully ([retire](retire.md)) once closed tasks pile up (Refinement).
7. **Rebuild the indexes:** `python3 tools/cards.py build`.
8. **Check:** `python3 tools/links.py` prints 0 broken.

## Closing a wave

1. Every member task is closed by the list above, or carried by name into the next wave.
2. The wave file says why its order held or changed. That reason is the part worth keeping, because the roadmap is rewritten.
3. The wave is retired like any task.

## Closing a session

1. **Agents:** every result is in and checked (links, counts, a read of the rows). None is left running. Any breach of a brief (a git command, a write outside its list) is logged in the task.
2. **Ledger:** every ruling the writer gave this session has its row, applied.
3. **Cards:** every card touched holds one version, its head in form; indexes rebuilt.
4. **Plan:** rewrite `plan/roadmap.md`: **Now** (where the work stands and where the next session starts), **Next** (in order), **Waiting** (on the writer, each with its question). Delete what is done. Update `plan/state.md` for every chapter that changed stage or drifted.
5. **Tasks:** close every task this session finished; a task left open says so in its status, with its next step.
6. **Keep what worked:** ask "what did this session do that is worth keeping?" Promote the answer to a workflow's lessons or a rule in `plan/README.md`.
7. **Links:** `python3 tools/links.py` prints 0 broken (or the known baseline).
8. **Tokens:** append the session's row to the token log: `python3 tools/tokens.py TRANSCRIPT --step "what the session did" --log plan/tokens.md --append`. The transcript is the session's file under `~/.claude/projects/` (the newest `.jsonl` in the book's folder there); name an agent's own transcript too if it has one.
9. **Commit** when the writer says so, never before. Check `git status` is clean afterward, and report the hash as `git log -1` shows it.

## Accepting a volume

When the writer accepts a volume, its prose is the readers' canon. The reader tests and the interest check first (so any reshoot is drafted while the outlines exist), then tag the commit, then shrink each chapter's outline and notes to one short summary of what later work needs (truths behind the scenes, setups for later volumes, clues, also in the register). Mark the chapters accepted in `plan/state.md`. Nothing reopens one but a new task that says so.
