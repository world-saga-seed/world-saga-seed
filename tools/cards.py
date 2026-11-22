#!/usr/bin/env python3
"""Check the heads of the cards, build each folder's index from them, and find cards.

A card is one short file about one thing (a person, a place, an object, a rule).
It opens with a fixed head of five lines:

    # <Name>: <what it is>
    (blank)
    *<one-line summary>*
    (blank)
    Keywords: <words a search would reach for that the card does not use>

Card folders are the subfolders of --root (for example world/people/,
world/places/). Each card folder has a README.md that holds its index table
between these two markers; the table is built by this tool, never edited by hand:

    <!-- cards: built by tools/cards.py; do not edit -->
    <!-- /cards -->

(Any comment starting "<!-- cards:" opens the table, so the wording is yours.)

Usage:
  python3 tools/cards.py check [--root DIR] [-v]   exit 1 on a head out of form or a stale table;
                                                   -v also lists keywords the card's text already uses
  python3 tools/cards.py build [--root DIR]        rewrite every folder's table from the heads
  python3 tools/cards.py find WORD ... [--root DIR]  cards whose head holds every word,
                                                   then cards whose text does
  python3 tools/cards.py index [--root DIR] [--sheets DIR]
                                                   write DIR/INDEX.md, the subject index: every
                                                   card by its name, what it is and its keywords,
                                                   every folder and every character sheet, A to Z
  python3 tools/cards.py build --index ...         build, then write the subject index
  --root DIR defaults to "world".
  --mark WORD   a status mark a card's name may end with, "(WORD)", left out of
                the tables and the index (repeatable; for example --mark proposal)

The subject index also lists the loose files at the top of --root (a guide, a
glossary) by their title.

Fields. A card or sheet may hold its facts as fields: top-level list items that
open with a bold label ending in a full stop, "- **Body.** ...", with any
indented lines under them, before the file's second "## " heading (bold items
further on are content, not fields). Two commands read them:

  python3 tools/cards.py fields FORMS [--only FOLDER]
      check every card in each folder FORMS names against its kind's fields: a
      field missing (one not marked optional) or out of order is a problem; a
      label the kind does not name is listed as the card's own field, not a problem. FORMS is a tab-separated file, one kind a row:
          world/beast<TAB>Family; Body; Size?; Threat; Name; Appears in; Open?
      (a trailing ? marks a field optional; # starts a comment). Exit 1 on a problem.

  python3 tools/cards.py get CARD ... [--keyword WORD] [--fields F,F] [--aliases FILE]
                                      [--settled] [--strip links,marks,ids]
      print the lines asked for. CARD is a card's file name without .md (selkie),
      its name, or a path, with #anchor for one heading's section. --fields keeps
      only those fields; with --aliases FILE a field may be a question the file
      maps to each kind's own fields (size, usage, danger), tab-separated rows of
      question, folder, fields. --settled keeps only the text under a settled
      mark, and text under no status mark. --strip cuts annotations from what
      is kept: links keep their words and lose their targets, marks are dropped,
      ruling IDs are dropped. Each card prints under "## Name (path)"; the first
      line says what was cut, so a reader knows a missing citation is cut, not absent.

Integrity. One command checks every card for what an agent must be able to trust:

  python3 tools/cards.py integrity [--forms FILE] [--ledger DIR] [--prose DIR]
                                   [--finished RX] [--only FOLDER] [--shared N]
      For every card, problems: the head out of form; a field missing or out of
      order (with --forms); a link to no file, or to a heading the file lacks; a
      ruling ID the ledger does not hold (with --ledger, the IDs that open its
      table rows); a link into a task file. On a finished card, also: a proposal
      left, and a field with no status mark (Name, Appears in and Open excepted).
      To check, listed but not failing: the chapters Appears in lists whose prose
      never names the card, and the chapters whose prose names it that Appears
      in does not list (with --prose); a run of --shared words (default 12)
      found on two cards, which may be one fact held in two places.
      A card is finished when its head lines match --finished (default
      "Distilled from|Finished"); with --clean, only once it also holds no
      proposal mark and no Open field (other than "None"), so a card becomes
      finished as its last proposal is ruled. Exit 1 on a problem on a finished card.

Marks. A mark is "*(Word ...)*" in the text. Its first words set the status of
the text after it, up to the next status mark: --settled-marks (default
Settled, Resolved, Confirmed, Drafted, Source) and --proposal-marks (default Proposal,
Proposals, Proposed, My reading, My readings, Open). Any other mark (Distilled
from, Moved, ...) is an annotation: it sets no status, and --strip marks drops it.
"""
import argparse, glob, os, re, sys

BEGIN = '<!-- cards: built by tools/cards.py; do not edit -->'
BEGIN_RX = re.compile(r'<!-- cards:.*?-->')
END = '<!-- /cards -->'
MARKS = []
TOOL = os.path.relpath(sys.argv[0]) if sys.argv[0].endswith('.py') else 'tools/cards.py'
TITLE = re.compile(r'^# (.+?): (.+)$')


def folders(root):
    out = set()
    for p in glob.glob(os.path.join(root, '**', '*.md'), recursive=True):
        d = os.path.dirname(p)
        if os.path.basename(p) != 'README.md' and os.path.abspath(d) != os.path.abspath(root):
            out.add(d)
    return sorted(out)


def cards(d):
    return sorted(p for p in glob.glob(os.path.join(d, '*.md')) if os.path.basename(p) != 'README.md')


def head(p):
    """(name, what, summary, keywords, errors) for the card at p."""
    lines = open(p, encoding='utf-8').read().split('\n') + [''] * 5
    err = []
    m = TITLE.match(lines[0])
    if not m:
        err.append('line 1 is not "# <Name>: <what it is>"')
    if lines[1].strip() or lines[3].strip():
        err.append('lines 2 and 4 must be blank')
    if not re.match(r'^\*[^*].*[^*]\*$', lines[2].strip()):
        err.append('line 3 is not one italic summary line')
    if not lines[4].startswith('Keywords: ') or not lines[4][10:].strip():
        err.append('line 5 is not "Keywords: ..."')
    name, what = (m.group(1), m.group(2)) if m else (lines[0].lstrip('# '), '')
    if MARKS:
        name = re.sub(r' \((?:' + '|'.join(map(re.escape, MARKS)) + r')\)$', '', name, flags=re.I)
    kw = [k.strip() for k in lines[4][10:].split(',') if k.strip()] if lines[4].startswith('Keywords: ') else []
    return name, what, lines[2].strip().strip('*'), kw, err


def table(d):
    rows = sorted(((head(p)[:2], os.path.basename(p)) for p in cards(d)),
                  key=lambda r: re.sub(r'^the ', '', r[0][0].lower()))
    return '\n'.join(['| Card | What it is |', '|---|---|'] +
                     [f'| [{n}]({f}) | {w} |' for (n, w), f in rows])


def readme(d):
    p = os.path.join(d, 'README.md')
    t = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    m = BEGIN_RX.search(t)
    b = t.find(END)
    return (t, m.end(), b) if m and m.end() <= b else None


def check(root, verbose):
    bad = 0
    for d in folders(root):
        for p in cards(d):
            name, what, summary, kw, err = head(p)
            for e in err:
                print(f'{p}: {e}')
                bad += 1
            if verbose:
                body = open(p, encoding='utf-8').read().split('\n', 5)[-1].lower()
                for k in kw:
                    if re.search(r'\b' + re.escape(k.lower()) + r'\b', body):
                        print(f'{p}: keyword already in the text: {k}')
        r = readme(d)
        if not r:
            print(f'{d}/README.md: no table markers')
            bad += 1
        elif r[0][r[1]:r[2]].strip() != table(d):
            print(f'{d}/README.md: table is stale; run build')
            bad += 1
    print(bad, 'card problems')
    return bad


def build(root):
    for d in folders(root):
        r = readme(d)
        if not r:
            print(f'{d}/README.md: no table markers, skipped')
            continue
        t, a, b = r
        new = t[:a] + '\n' + table(d) + '\n' + t[b:]
        if new != t:
            open(os.path.join(d, 'README.md'), 'w', encoding='utf-8').write(new)
            print('rebuilt', d)


def find(root, words):
    words = [w.lower() for w in words]
    hits, body = [], []
    for d in folders(root):
        for p in cards(d):
            name, what, summary, kw, _ = head(p)
            h = ' '.join([name, what, summary] + kw).lower()
            if all(w in h for w in words):
                hits.append(f'{p}: {name}: {what}')
            elif all(w in open(p, encoding='utf-8').read().lower() for w in words):
                body.append(f'{p}: {name}: {what} (in the text)')
    print('\n'.join(hits + body) or 'no card')


def index(root, sheets):
    ent = {}

    def add(term, label, path):
        t = term.strip().strip('.').strip()
        if len(t) >= 3:
            ent.setdefault(t[0].upper() + t[1:], set()).add((label, path))

    for d in folders(root):
        for p in cards(d):
            name, what, summary, kw, _ = head(p)
            label = f'{name}: {what}' if what else name
            add(name, label, p)
            for k in kw:
                add(k, label, p)
            for part in re.split(r',|;| and | or ', what):
                part = re.sub(r'^\s*(the|a|an|its|their|his|her)\s+', '', part.strip())
                if 3 <= len(part) <= 40 and len(part.split()) <= 4:
                    add(part, label, p)
        r = os.path.join(d, 'README.md')
        if os.path.exists(r):
            t = open(r, encoding='utf-8').readline().lstrip('# ').strip()
            add(t.split(':')[0], t, r)
    for p in sorted(glob.glob(os.path.join(root, '*.md'))):
        if os.path.basename(p) not in ('README.md', 'INDEX.md'):
            t = open(p, encoding='utf-8').readline().lstrip('# ').strip()
            add(t.split(':')[0], t, p)
    if sheets and os.path.isdir(sheets):
        for p in sorted(glob.glob(os.path.join(sheets, '**', '*.md'), recursive=True)):
            if os.path.basename(p) != 'README.md':
                t = open(p, encoding='utf-8').readline().lstrip('# ').strip()
                add(t.split('(')[0].split(':')[0], t, p)
    key = lambda s: re.sub(r'^(the|a|an) ', '', s.lower())
    out = os.path.join(root, 'INDEX.md')
    lines = ['# Subject index', '',
             '*Every card by its name and its search words, every folder and every character sheet, A to Z. '
             f'Built by `{TOOL} index` from the card heads; never edit by hand (fix the card\'s head). '
             f'For a subject not here, `python3 {TOOL} find WORDS` searches the text.*']
    letter = None
    for term in sorted(ent, key=key):
        L = key(term)[:1].upper()
        if L != letter:
            letter = L
            lines += ['', f'## {L}', '']
        refs = '; '.join(f'[{lab}]({os.path.relpath(p, root)})' for lab, p in sorted(ent[term]))
        lines.append(f'- **{term}**: {refs}')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'{out}: {len(ent)} entries')


LABEL = re.compile(r'^- \*\*([^*]{1,60}?)\.\*\*')
MARK = re.compile(r'\*\((?P<w>[A-Za-z][A-Za-z ]*?)\b[^\n]*?\)\*')
SETTLED = ['Settled', 'Resolved', 'Confirmed', 'Drafted', 'Source']
PROPOSAL = ['Proposal', 'Proposals', 'Proposed', 'My reading', 'My readings', 'Open']
ID = re.compile(r',?\s*\b[A-Z]\d{4}-\d+(?:-\d+)?(?:\s*(?:to|and|,)\s*\d+)*\b')


def fields(p):
    """[(label, first line, last line, text)] for each top-level field of the file at p, up to its second ## heading."""
    out, cur, heads = [], None, 0
    for i, line in enumerate(open(p, encoding='utf-8').read().split('\n'), 1):
        if line.startswith('## '):
            heads += 1
            if heads > 1:  # fields live in the head and first section; bold items further on are content
                break
        m = LABEL.match(line)
        if m:
            cur = [m.group(1).strip(), i, i, [line]]
            out.append(cur)
        elif cur and line.strip() and line[:1].isspace():
            cur[2] = i
            cur[3].append(line)
        else:
            cur = None
    return [(l, a, b, '\n'.join(t)) for l, a, b, t in out]


def load_forms(path):
    forms = {}
    for line in open(path, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        d, _, fs = line.rstrip('\n').partition('\t')
        forms[os.path.normpath(d.strip())] = [(f.strip().rstrip('?'), f.strip().endswith('?')) for f in fs.split(';') if f.strip()]
    return forms


def load_mapped(path):
    """{card: {field: [sources]}} from a sections file: card<TAB>field<TAB>sources, ';'-separated.
    A source is a heading of the card (its section holds the field), **Label** (a field of the card's
    own under another name), or '-' (the field does not apply to this card)."""
    m = {}
    if not path:
        return m
    for line in open(path, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        c, f, s = (line.rstrip('\n').split('\t') + ['', ''])[:3]
        m.setdefault(os.path.normpath(c.strip()), {})[f.strip()] = [x.strip() for x in s.split(';') if x.strip()]
    return m


def mapped_text(p, sources):
    """The text a sections file maps a field to on card p: each section, or each field under its own label."""
    out = []
    for s in sources:
        if s == '-':
            continue
        lab = re.fullmatch(r'\*\*(.+?)\.?\*\*', s)
        if lab:
            out += [t for l, _, _, t in fields(p) if l.lower() == lab.group(1).lower()]
        else:
            out.append('\n' + (section_text(p, re.sub(r'[^\w\- ]', '', s.strip().lower()).replace(' ', '-')) or f'(no section "{s}")') + '\n')
    return out


def check_fields(forms_path, only=None, mapped_path=None):
    forms, bad, extra = load_forms(forms_path), 0, 0
    mapped = load_mapped(mapped_path)
    for d, form in forms.items():
        if only and os.path.normpath(only) != d:
            continue
        names = [f for f, _ in form]
        for p in cards(d):
            mine = mapped.get(os.path.normpath(p), {})
            own = {s[2:-2].rstrip('.') for v in mine.values() for s in v if s.startswith('**')}
            got = [l for l, *_ in fields(p) if l not in own]
            for f, opt in form:
                if f in mine:
                    for s, t in zip([s for s in mine[f] if s != '-'], mapped_text(p, [s for s in mine[f] if s != '-'])):
                        if t.strip().startswith('(no section'):
                            print(f'{p}: {f} is mapped to a section the card lacks: {s}')
                            bad += 1
                    continue
                if not opt and f not in got:
                    print(f'{p}: missing field: {f}')
                    bad += 1
            for l in got:
                if l not in names:
                    print(f'{p}: (info) a field of its own: {l}')
                    extra += 1
            known = [names.index(l) for l in dict.fromkeys(got) if l in names]
            if known != sorted(known):
                print(f'{p}: fields out of order: ' + ', '.join(names[k] for k in known))
                bad += 1
    print(f'{bad} field problems; {extra} fields of their own (info: content the form does not name, kept; '
          'add one to the form when several cards share it)')
    return bad


def status_of(word, settled, proposal):
    w = word.strip().lower()
    if any(w == s.lower() or w.startswith(s.lower() + ' ') for s in settled):
        return 'settled'
    if any(w == s.lower() or w.startswith(s.lower() + ' ') for s in proposal):
        return 'proposal'
    return None


def settled_only(text, settled, proposal):
    """The text under a settled mark or under no status mark; a field reduced to its label is dropped."""
    out, pos, state = [], 0, None
    for m in MARK.finditer(text):
        if state != 'proposal':
            out.append(text[pos:m.start()])
        s = status_of(m.group('w'), settled, proposal)
        if s:
            state = s
            if s == 'settled':
                out.append(m.group(0))
        elif state != 'proposal':
            out.append(m.group(0))
        pos = m.end()
    if state != 'proposal':
        out.append(text[pos:])
    return re.sub(r'[ \t]{2,}', ' ', ''.join(out)).rstrip()


def strip(text, what):
    if 'marks' in what:
        text = MARK.sub('', text)
    if 'links' in what:
        text = re.sub(r'\[([^\]]*)\]\([^)\s]*\)', r'\1', text)
    if 'ids' in what:
        text = ID.sub('', text)
    text = re.sub(r'\(\s*[,.]?\s*\)', '', text)
    text = re.sub(r'\s*[;,:]\s*([.)])', r'\1', text)   # "(Settled by the author;.)" once its ID is cut
    return re.sub(r'[ \t]{2,}', ' ', re.sub(r' +([.,;:])', r'\1', text)).rstrip()


def resolve(root, sheets, want):
    """The file a CARD argument names: a path, a file name without .md, or a card's name."""
    name, _, anchor = want.partition('#')
    if os.path.exists(name):
        return name, anchor
    pool = [p for d in folders(root) for p in cards(d)] + (cards(sheets) if os.path.isdir(sheets) else [])
    for p in pool:
        if os.path.basename(p)[:-3] == name:
            return p, anchor
    for p in pool:
        if head(p)[0].lower() == name.lower():
            return p, anchor
    return None, anchor


def section_text(p, anchor):
    lines = open(p, encoding='utf-8').read().split('\n')
    slug = lambda h: re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-')
    for i, l in enumerate(lines):
        m = re.match(r'(#+) (.*)', l)
        if m and slug(m.group(2)) == anchor:
            lv, j = len(m.group(1)), i + 1
            while j < len(lines) and not (re.match(r'#+ ', lines[j]) and len(re.match(r'(#+)', lines[j]).group(1)) <= lv):
                j += 1
            return '\n'.join(lines[i:j]).strip()
    return None


def load_aliases(path):
    al = {}
    for line in open(path, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        q, d, fs = (line.rstrip('\n').split('\t') + ['', ''])[:3]
        al.setdefault(q.strip().lower(), {})[os.path.normpath(d.strip())] = [f.strip() for f in fs.split(';') if f.strip()]
    return al


def get(a):
    settled = a.settled_marks or SETTLED
    proposal = a.proposal_marks or PROPOSAL
    cuts = [w for w in (a.strip or '').split(',') if w]
    wanted = [f.strip() for f in a.fields.split(',')] if a.fields else None
    aliases = load_aliases(a.aliases) if a.aliases else {}
    mapped = load_mapped(a.sections)
    picks = []
    for w in a.words:
        p, anchor = resolve(a.root, a.sheets, w)
        if not p:
            print(f'no card: {w}', file=sys.stderr)
            continue
        picks.append((p, anchor))
    if a.keyword:
        k = a.keyword.lower()
        for d in folders(a.root):
            for p in cards(d):
                n, _, _, kw, _ = head(p)
                if k in [x.lower() for x in kw] or re.search(r'\b' + re.escape(k) + r'\b', n.lower()):
                    picks.append((p, ''))
    said = []
    if a.settled:
        said.append('only settled text')
    if cuts:
        said.append('cut: ' + ', '.join({'links': 'link targets', 'marks': 'marks', 'ids': 'ruling IDs'}.get(c, c) for c in cuts))
    if a.table:
        return get_table(a, picks, wanted, aliases, settled, proposal, cuts, mapped)
    print('*' + ('; '.join(said) if said else 'Whole') + '. The full card is at its path.*' if said else '*The lines asked for; the full card is at its path.*')
    seen = set()
    for p, anchor in picks:
        if (p, anchor) in seen:
            continue
        seen.add((p, anchor))
        kind = os.path.normpath(os.path.dirname(p))
        if anchor:
            body = [section_text(p, anchor) or f'(no section #{anchor})']
        else:
            fs = fields(p)
            if wanted:
                want = []
                for f in wanted:
                    want += aliases.get(f.lower(), {}).get(kind, [f])
                lower = [x.lower() for x in want]
                fs = sorted((x for x in fs if x[0].lower() in lower), key=lambda x: lower.index(x[0].lower()))
                got = {x[0].lower() for x in fs}
                for f, srcs in mapped.get(os.path.normpath(p), {}).items():
                    if f.lower() in lower and f.lower() not in got:
                        fs += [(f, 0, 0, t) for t in mapped_text(p, srcs)]
            body = [t for *_, t in fs] if fs or wanted else [open(p, encoding='utf-8').read().split('\n', 5)[-1].strip()]
        out = []
        for t in body:
            if a.settled:
                t = settled_only(t, settled, proposal)
                if re.fullmatch(r'- \*\*[^*]+\.\*\*\s*', t):
                    continue
            if cuts:
                t = strip(t, cuts)
            out.append(t)
        print(f'\n## {head(p)[0]} ({p}' + (f'#{anchor}' if anchor else '') + ')\n')
        print('\n'.join(out) if out else '(nothing asked for is on this card)')


def cell(text, words):
    """A field's text as one table cell: the label cut, lines joined, pipes escaped, at most `words` words."""
    t = LABEL.sub('', text.split('\n', 1)[0], count=1) + ' ' + ' '.join(l.strip() for l in text.split('\n')[1:])
    t = t.strip()
    w = t.split()
    t = ' '.join(w[:words]) + (' …' if len(w) > words else '')
    return t.replace('|', '\\|')


def get_table(a, picks, wanted, aliases, settled, proposal, cuts, mapped=None):
    """One row per card, one column per field or question asked; with no fields, a brief index:
    each card's name and its first field. Sections (card#anchor) are skipped: a table holds fields."""
    cols = wanted or ['First field']
    print('| Card | ' + ' | '.join(cols) + ' |')
    print('|---|' + '---|' * len(cols))
    seen = set()
    for p, anchor in picks:
        if p in seen or anchor:
            continue
        seen.add(p)
        kind = os.path.normpath(os.path.dirname(p))
        fs = {l.lower(): t for l, _, _, t in fields(p)}
        row = []
        for c in cols:
            if not wanted:
                first = fields(p)
                texts = [first[0][3]] if first else []
            else:
                names = aliases.get(c.lower(), {}).get(kind, [c])
                texts = [fs[x.lower()] for x in names if x.lower() in fs]
                mine = (mapped or {}).get(os.path.normpath(p), {})
                for x in names:
                    if x.lower() not in fs and x in mine:
                        texts += mapped_text(p, mine[x])
            out = []
            for t in texts:
                if a.settled:
                    t = settled_only(t, settled, proposal)
                if cuts:
                    t = strip(t, cuts)
                out.append(cell(t, a.cell))
            row.append('; '.join(x for x in out if x) or '—')
        print(f'| [{head(p)[0]}]({p}) | ' + ' | '.join(row) + ' |')


def slug(h):
    return re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-')


def anchors(path, _c={}):
    if path not in _c:
        seen, out = {}, set()
        for l in open(path, encoding='utf-8'):
            m = re.match(r'#+ (.*)', l)
            if m:
                s = slug(m.group(1))
                n = seen.get(s, 0)
                seen[s] = n + 1
                out.add(s if n == 0 else f'{s}-{n}')
        _c[path] = out
    return _c[path]


def ledger_ids(d):
    ids = set()
    for p in glob.glob(os.path.join(d, '**', '*.md'), recursive=True):
        for l in open(p, encoding='utf-8'):
            m = re.match(r'\|\s*([A-Z]\d{4}-\d+(?:-\d+)?)\s*\|', l)
            if m:
                ids.add(m.group(1))
    return ids


def page_name(p, name):
    """The word the pages use for a card: its Name field's first name (before a comma, a stop or
    "from"), else the card's title without an article."""
    t = next((t for l, *_, t in fields(p) if l == 'Name'), '')
    t = MARK.sub('', re.sub(r'^- \*\*Name\.\*\*', '', t.split('\n')[0]))
    t = re.split(r'[,.;(]| from | for | means ', re.sub(r'[*_]', '', t).strip(), maxsplit=1)[0].strip()
    t = t if 2 < len(t) <= 40 else name
    return re.sub(r'^(the|a|an) ', '', t.lower())


def integrity(a):
    settled, proposal = a.settled_marks or SETTLED, a.proposal_marks or PROPOSAL
    forms = load_forms(a.forms) if a.forms else {}
    mapped = load_mapped(a.sections)
    ids = ledger_ids(a.ledger) if a.ledger else None
    fin_rx = re.compile(a.finished)
    prose = sorted(glob.glob(os.path.join(a.prose, '*.md'))) if a.prose else []
    ptext = {os.path.basename(p)[:5]: open(p, encoding='utf-8').read() for p in prose}
    every = [p for d in folders(a.root) for p in cards(d) if not a.only or os.path.normpath(d) == os.path.normpath(a.only)]
    probs = {p: [] for p in every}
    checks = {p: [] for p in every}
    fin, waiting = {}, {}
    for p in every:
        text = open(p, encoding='utf-8').read()
        fin[p] = bool(fin_rx.search('\n'.join(text.split('\n')[:8])))
        if fin[p] and a.clean:
            left = [m for m in MARK.finditer(text) if status_of(m.group('w'), settled, proposal) == 'proposal']
            left += [None for l, *_, ft in fields(p) if l == 'Open' and not re.search(r'\*\*Open\.\*\*\s*(None|Nothing)\b', ft)]
            if left:
                fin[p] = False
                waiting[p] = len(left)
        name, _, _, _, err = head(p)
        probs[p] += err
        d = os.path.normpath(os.path.dirname(p))
        if d in forms:
            got = [l for l, *_ in fields(p)]
            names = [f for f, _ in forms[d]]
            mine = mapped.get(os.path.normpath(p), {})
            probs[p] += [f'missing field: {f}' for f, opt in forms[d] if not opt and f not in got and f not in mine]
            known = [names.index(l) for l in dict.fromkeys(got) if l in names]
            if known != sorted(known):
                probs[p].append('fields out of order')
        for m in re.finditer(r'\]\(([^)\s]+)\)', text):
            f, _, an = m.group(1).partition('#')
            if re.match(r'^[a-z]+:', f):
                continue
            t = os.path.normpath(os.path.join(os.path.dirname(p), f)) if f else p
            if not os.path.exists(t):
                probs[p].append(f'link to no file: {m.group(1)}')
            elif an and t.endswith('.md') and an not in anchors(t):
                probs[p].append(f'link to no heading: {m.group(1)}')
            if re.search(r'(^|/)tasks?/', f) or re.search(r'(^|/)task-\d', f):
                probs[p].append(f'a task cited: {m.group(1)}')
        if ids is not None:
            for i in sorted(set(re.findall(r'\b[A-Z]\d{4}-\d+(?:-\d+)?\b', text))):
                if i not in ids:
                    probs[p].append(f'ruling not in the ledger: {i}')
        if fin[p]:
            for m in MARK.finditer(text):
                if status_of(m.group('w'), settled, proposal) == 'proposal':
                    probs[p].append(f'proposal left on a finished card: {m.group(0)[:60]}')
            for l, ln, _, t in fields(p):
                if l not in ('Name', 'Appears in', 'Open') and not any(status_of(m.group('w'), settled, proposal) for m in MARK.finditer(t)):
                    probs[p].append(f'field with no status mark: {l} (line {ln})')
        if prose:
            appears = next((t for l, *_, t in fields(p) if l == 'Appears in'), '')
            listed = set(re.findall(r'\b\d{5}\b', appears))
            term = page_name(p, name)
            named = {n for n, t in ptext.items() if len(term) > 3 and re.search(r'\b' + re.escape(term) + r'\b', t.lower())}
            if appears:
                for n in sorted(listed - named):
                    if n in ptext:
                        checks[p].append(f'Appears in lists {n}, whose prose never names "{term}"')
                for n in sorted(named - listed):
                    checks[p].append(f'{n} names "{term}" but Appears in does not list it')
    if a.shared:
        runs = {}
        for p in every:
            w = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', MARK.sub(' ', open(p, encoding='utf-8').read().split('\n', 5)[-1])).lower().split()
            for i in range(len(w) - a.shared + 1):
                runs.setdefault(' '.join(w[i:i + a.shared]), set()).add(p)
        pairs = {}
        for r, ps in runs.items():
            if 1 < len(ps) <= 3:
                for x in ps:
                    for y in ps:
                        if x < y:
                            pairs.setdefault((x, y), r)
        for (x, y), r in sorted(pairs.items()):
            checks[x].append(f'shares "{r}" with {y}')
    bad = 0
    for p in every:
        for e in probs[p]:
            print(f'{p}: {"PROBLEM" if fin[p] else "problem"}: {e}')
        for c in checks[p]:
            print(f'{p}: check: {c}')
        if fin[p]:
            bad += len(probs[p])
    nf = sum(fin.values())
    if a.clean:
        print(f'{len(waiting)} distilled cards wait on proposals or open questions ({sum(waiting.values())} in all)')
    print(f'{len(every)} cards, {nf} finished; problems: {sum(len(v) for v in probs.values())} '
          f'({bad} on finished cards); checks: {sum(len(v) for v in checks.values())}')
    return bad


def main():
    ap = argparse.ArgumentParser(description='Card heads, folder indexes and search.',
                                 epilog='See the top of this file for the card head form.')
    ap.add_argument('command', choices=['check', 'build', 'find', 'index', 'fields', 'get', 'integrity'],
                    help='check the card heads and indexes; build the indexes; find cards by word; write the subject index; '
                         'check cards against their kinds\' fields; get fields from cards')
    ap.add_argument('words', nargs='*', help='for find: the words to look for; for fields: the forms file; for get: the cards')
    ap.add_argument('--only', help='for fields: check only this folder')
    ap.add_argument('--keyword', help='for get: also every card whose name or Keywords hold this word')
    ap.add_argument('--fields', help='for get: the fields to keep, comma-separated (or questions, with --aliases)')
    ap.add_argument('--aliases', help='for get: a file mapping questions to each kind\'s fields')
    ap.add_argument('--settled', action='store_true', help='for get: keep only settled and unmarked text')
    ap.add_argument('--strip', help='for get: cut links, marks and/or ids, comma-separated')
    ap.add_argument('--sections', help='for fields and get: a file mapping a card\'s field to its sections or to a field of its own name (card, field, sources)')
    ap.add_argument('--table', action='store_true', help='for get: one row per card, a column per field asked (with no fields, each card\'s first field: a brief index)')
    ap.add_argument('--cell', type=int, default=30, help='for get --table: the most words in a cell (default 30)')
    ap.add_argument('--forms', help='for integrity: the forms file (as for fields)')
    ap.add_argument('--ledger', help='for integrity: the ledger folder; every ruling ID cited must open a row there')
    ap.add_argument('--prose', help='for integrity: the prose folder, to check Appears in both ways')
    ap.add_argument('--finished', default='Distilled from|Finished', help='for integrity: a pattern a finished card\'s head lines match')
    ap.add_argument('--clean', action='store_true', help='for integrity: a card matching --finished is finished only once no proposal mark and no Open field is left')
    ap.add_argument('--shared', type=int, default=12, help='for integrity: a run of this many words on two cards is listed (0: off)')
    ap.add_argument('--settled-marks', nargs='*', help='mark words that settle the text after them')
    ap.add_argument('--proposal-marks', nargs='*', help='mark words that propose the text after them')
    ap.add_argument('--root', default='world', help='the folder whose subfolders are card folders (default: world)')
    ap.add_argument('--sheets', default='story/notes/characters', help='for index: the character sheets folder (default: story/notes/characters)')
    ap.add_argument('-v', action='store_true', help='for check: also list keywords the card text already uses')
    ap.add_argument('--mark', action='append', default=[], help='a status mark a name may end with, "(WORD)", left out of tables and index (repeatable)')
    ap.add_argument('--index', action='store_true', help='for build: also write the subject index')
    a = ap.parse_args()
    MARKS.extend(a.mark)
    if not os.path.isdir(a.root):
        sys.exit(f'no folder {a.root}')
    if a.command == 'check':
        sys.exit(1 if check(a.root, a.v) else 0)
    elif a.command == 'build':
        build(a.root)
        if a.index:
            index(a.root, a.sheets)
    elif a.command == 'index':
        index(a.root, a.sheets)
    elif a.command == 'fields':
        if not a.words:
            sys.exit('fields needs the forms file')
        sys.exit(1 if check_fields(a.words[0], a.only, a.sections) else 0)
    elif a.command == 'get':
        get(a)
    elif a.command == 'integrity':
        sys.exit(1 if integrity(a) else 0)
    else:
        find(a.root, a.words)


if __name__ == '__main__':
    main()
