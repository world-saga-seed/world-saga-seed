#!/usr/bin/env python3
"""The reading list for one chapter's agents, one hop from its outline and notes.

A drafter or critic told "read the cards it needs" opens whole files and reads
far more than it uses; one told "read the drafts before" reads the whole volume.
This builds the list instead: every link in the chapter's outline and notes,
resolved to its file and, where the link names a heading in a large file, to
that section's line range; the cards the outline or notes name without a link (by the card's name or a
person's first name), listed apart as not to read unless --named read; the sheets
of the people the chapter names (a sheet's own subfolder only when linked); the
chapter before; and the volume digest in place of the rest of the volume.
A linked card that is a stub (a line starting "Stub:") is named on stderr and
listed first, to be built before the chapter is drafted.

Usage:
  python3 tools/reading.py N [--step STEP] [--digest FILE] [--rules FILE ...]
                          [--sheets DIR] [--large WORDS]

  N              the chapter number, as it starts the file names (e.g. 00400)
  --step STEP    narrow the list for one role: drafter (default, everything),
                 facts (cards, sections and sheet heads), setup (cards, and
                 the sheet sections a drafter reads), procedures (cards and
                 sections), habits (sheets' Habits sections only), continuity
                 (digest and prose). A drafter or setup critic reads a short
                 sheet whole and of a long one --sheet-sections, up to
                 --sheet-budget words.
  --digest FILE  the volume digest, read in place of the earlier chapters
  --rules FILE   files every drafter reads (default: story/voice/voice.md,
                 plan/workflows/drafting/rulings.md)
  --sheets DIR   the character sheets' folder (default story/notes/characters)
  --large WORDS  a file over this many words is listed by section (default 1500)

Reads story/outline/N-*.md and story/notes/N-*.md and story/prose/. Prints the
list as markdown; write it to the task's folder and give it to the agent with
"read these and nothing else, unless a fact you need is missing; then follow
one link and say so in your report". Run from the book's top folder.
"""
import argparse, collections, glob, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cards as cardtool  # noqa: E402  (fields, marks and annotation cuts, for --bundle)

# For --bundle: what each role reads of a card and a sheet, unless --recipes names a file.
# role: (card fields: * for all, "*,-Field" for all but those, else fields or questions; sheets:
#        sections, habits, head, size, none; settled only; what to cut)
BOOKKEEPING = '-Appears in,-Origin and lineage,-History,-Open'
RECIPES = {
    'drafter':    ('*,' + BOOKKEEPING, 'sections', False, 'links,ids'),
    'facts':      ('*,' + BOOKKEEPING, 'head', True, 'links,marks,ids'),
    'setup':      ('*,' + BOOKKEEPING, 'sections', False, 'links,ids'),
    'procedures': ('*,' + BOOKKEEPING, 'none', True, 'links,marks,ids'),
    'habits':     ('', 'habits', False, 'links,marks,ids'),
    'continuity': ('', 'none', False, 'links,marks,ids'),
    'scale':      ('size', 'size', True, 'links,marks,ids'),
}
INCLUDE = re.compile(r'^\s*[-*] \[[^\]]*\]\(([^)\s]+)\):\s*(.+?)\s*$')


STUB = re.compile(r'^Stub:', re.M)


def is_stub(path):
    """A stub card carries a line starting "Stub:" (card-existing: build when a scene needs it)."""
    try:
        with open(path, encoding='utf-8') as f:
            return bool(STUB.search(f.read()))
    except OSError:
        return False


def slug(h):
    h = h.strip().lower()
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


_cache = {}


def sections(path):
    """anchor -> (title, level, first line, last line, words); '' is the whole file."""
    if path in _cache:
        return _cache[path]
    lines = open(path, encoding='utf-8').read().split('\n')
    heads, seen = [], collections.Counter()
    for i, line in enumerate(lines, 1):
        m = re.match(r'(#+) (.*)', line)
        if m:
            s = slug(m.group(2))
            k = seen[s]
            seen[s] += 1
            heads.append((s if k == 0 else f'{s}-{k}', m.group(2).strip(), len(m.group(1)), i))
    out = {'': ('(whole file)', 0, 1, len(lines), sum(len(l.split()) for l in lines))}
    for j, (an, t, lv, st) in enumerate(heads):
        end = len(lines)
        for _, _, lv2, st2 in heads[j + 1:]:
            if lv2 <= lv:
                end = st2 - 1
                break
        out[an] = (t, lv, st, end, sum(len(l.split()) for l in lines[st - 1:end]))
    _cache[path] = out
    return out


def fmt(path, anchors, large):
    S = sections(path)
    whole = S['']
    anchors = {a for a in anchors if a in S}
    if not anchors or '' in anchors or whole[4] <= large:
        return f'- `{path}` (whole, {whole[4]} words)'
    keep = []
    for an in sorted(anchors, key=lambda x: (S[x][2], -S[x][3])):
        if not any(S[k][2] <= S[an][2] and S[an][3] <= S[k][3] for k in keep):
            keep.append(an)
    if sum(S[an][4] for an in keep) >= 0.9 * whole[4]:  # the sections are nearly the whole file
        return f'- `{path}` (whole, {whole[4]} words)'
    rows = [f'- `{path}` ({whole[4]} words in all; read only these sections, by line):']
    for an in keep:
        t, _, st, en, w = S[an]
        rows.append(f'  - lines {st} to {en}: "{t}" ({w} words)')
    return '\n'.join(rows)


def habits_of(sh, large):
    S = sections(sh)
    hs = [x for x in S if x and 'habit' in x]
    if hs:
        return fmt(sh, {hs[0]}, 0)
    for i, line in enumerate(open(sh, encoding='utf-8'), 1):
        if re.match(r'-\s+\*\*Habits', line):
            return f'- `{sh}`: line {i}, the **Habits** item'
    return f'- `{sh}`: no Habits section; read the head only'


def drafter_sheet(sh, a):
    """A drafter reads a short sheet whole, and of a long one the sections that carry how the person
    looks, talks and acts (--sheet-sections), up to --sheet-budget words."""
    S = sections(sh)
    if S[''][4] <= a.large:
        return fmt(sh, {''}, a.large)
    pick, used = set(), 0
    for pat in a.sheet_sections:
        for an in S:
            if an and re.search(pat, an) and an not in pick and used + S[an][4] <= a.sheet_budget:
                pick.add(an)
                used += S[an][4]
                break
    if pick:
        return fmt(sh, pick, 0)
    lines = open(sh, encoding='utf-8').read().splitlines()
    head = next((i for i, l in enumerate(lines, 1) if l.startswith('## ')), len(lines))
    return f'- `{sh}`: lines 1 to {head} (the head) and the **Habits.** item'


def load_recipes(path):
    r = dict(RECIPES)
    if path:
        for line in open(path, encoding='utf-8'):
            if not line.strip() or line.startswith('#'):
                continue
            c = (line.rstrip('\n').split('\t') + [''] * 5)[:5]
            r[c[0].strip()] = (c[1].strip(), c[2].strip() or 'none', c[3].strip().lower() in ('yes', 'y', 'true'), c[4].strip())
    return r


def lines_of(path, st, en):
    return '\n'.join(open(path, encoding='utf-8').read().split('\n')[st - 1:en]).strip()


def cut(text, settled, cuts):
    if settled:
        text = cardtool.settled_only(text, cardtool.SETTLED, cardtool.PROPOSAL)
    return cardtool.strip(text, cuts) if cuts else text


def card_text(path, anchors, want, settled, cuts, aliases):
    """A card's lines for one role: the linked sections of a card without fields, else its fields,
    narrowed by the include's fields and the role's (questions through the aliases)."""
    fs = cardtool.fields(path)
    S = sections(path)
    secs = [an for an in anchors if an and an in S]
    drop = [w[1:].strip().lower() for w in (want or []) if w.startswith('-')]
    want = [w for w in want if not w.startswith('-')] if want is not None else None
    if want == ['*']:
        want = None
    if want is not None:  # a role asking only some fields reads only fields, never a card's sections
        if not fs:
            return ''
        secs = []
    if secs or not fs:
        if secs:
            body = '\n\n'.join(lines_of(path, S[an][2], S[an][3]) for an in sorted(secs, key=lambda x: S[x][2]))
        else:
            body = open(path, encoding='utf-8').read().split('\n', 5)[-1].strip()
        return cut(body, settled, cuts)
    kind = os.path.normpath(os.path.dirname(path))
    if want is not None:
        names = []
        for w in want:
            names += aliases.get(w.lower(), {}).get(kind, [w])
        lower = [n.lower() for n in names]
        fs = sorted((f for f in fs if f[0].lower() in lower), key=lambda f: lower.index(f[0].lower()))
    kept = []
    for f in (f for f in fs if f[0].lower() not in drop):
        t = cut(f[3], settled, cuts)
        if not re.fullmatch(r'- \*\*[^*]+\.\*\*\s*', t):
            kept.append(t)
    return '\n'.join(kept)


def sheet_text(sh, mode, a, settled, cuts, aliases):
    S = sections(sh)
    if mode == 'habits':
        hs = [x for x in S if x and 'habit' in x]
        if hs:
            return cut(lines_of(sh, S[hs[0]][2], S[hs[0]][3]), settled, cuts)
        return cut('\n'.join(f[3] for f in cardtool.fields(sh) if f[0].lower().startswith('habits')), settled, cuts)
    if mode == 'size':
        return card_text(sh, set(), ['size'], settled, cuts, aliases)
    if mode == 'head':
        gl = [x for x in S if x and S[x][1] <= 2 and 'glance' in x]
        lines = open(sh, encoding='utf-8').read().split('\n')
        first = next((i for i, l in enumerate(lines, 1) if l.startswith('## ')), len(lines) + 1)
        parts = ['\n'.join(lines[5:first - 1]).strip()] + [lines_of(sh, S[x][2], S[x][3]) for x in gl[:1]]
        return cut('\n\n'.join(p for p in parts if p), settled, cuts)
    if S[''][4] <= a.large:
        return cut(open(sh, encoding='utf-8').read().split('\n', 5)[-1].strip(), settled, cuts)
    pick, used = [], 0
    inside = lambda x, y: S[y][2] <= S[x][2] and S[x][3] <= S[y][3]
    for pat in a.sheet_sections:
        for an in S:
            if an and re.search(pat, an) and an not in pick and not any(inside(an, k) for k in pick) \
                    and used + S[an][4] <= a.sheet_budget:
                pick = [k for k in pick if not inside(k, an)] + [an]
                used = sum(S[k][4] for k in pick)
                break
    if not pick:  # a long sheet with no sections: its head (the lines before any field) and its Habits
        fs = cardtool.fields(sh)
        lines = open(sh, encoding='utf-8').read().split('\n')
        first = fs[0][1] if fs else len(lines) + 1
        keep = [f[3] for f in fs if f[0].lower() in ('who', 'look and voice', 'habits') or f[0].lower().startswith('habits')]
        return cut('\n'.join(lines[5:first - 1]).strip() + '\n' + '\n'.join(keep), settled, cuts)
    return cut('\n\n'.join(lines_of(sh, S[an][2], S[an][3]) for an in sorted(pick, key=lambda x: S[x][2])), settled, cuts)


def demote(body):
    """A card's own headings sit under the bundle's block heading: two levels down, at least #### ."""
    return re.sub(r'^(#{1,6}) ', lambda m: '#' * min(6, max(4, len(m.group(1)) + 2)) + ' ', body, flags=re.M)


ASIDE_FREE = {'drafter'}   # roles that never see author-side text: what the page must not hold
CHAPTER = re.compile(r'(?<![\w-])(\d{5})(?::\d+(?:-\d+)?)?(?![\w-])')
MARKSPAN = re.compile(r'\*\([^\n]*?\)\*')
SENTENCE = re.compile(r'(?:(?<=[.!?;])|(?<=[.!?]["”])|(?<=\d\))|(?<=\x00))\s+(?=[*(\"“A-Z\x00])')


def so_far(text, n):
    """The cards and sheets without what the page shows from chapter n on, and without citations.
    A chapter number on a trait says where it is shown, not when it became true, so traits stay. What goes is
    the page itself from chapter n on (later chapters have not happened; chapter n's old draft is not read):
    a sentence quoting the page there ("...", 06000:101), a line marked from that draft ("from the draft,
    06000"), and in an On the page field or a list of instances (indented items), any sentence or item that
    cites only chapter n or later. A mark stays whole with its sentence. Then the citations go: short
    parentheticals that cite a chapter, runs of bare chapter numbers, habit tags like (M22), file names.
    The critics keep it all."""
    n = int(n)
    refs = lambda s: [int(m.group(1)) for m in CHAPTER.finditer(s)]
    late = lambda s: bool(refs(s)) and min(refs(s)) >= n
    page = lambda s: bool(re.search(r'["“][^"”]{6,}["”][^"“]{0,12}?\(?\[?(\d{5})', s)) and \
        max(int(m.group(1)) for m in re.finditer(r'["“][^"”]{6,}["”][^"“]{0,12}?\(?\[?(\d{5})', s)) >= n
    drafted = lambda s: any(int(m.group(1)) >= n for m in re.finditer(r'from the (?:\w+ )?draft,?\s*\[?(\d{5})', s, re.I))
    out, field = [], ''
    for line in text.split('\n'):
        lead = re.match(r'(\s*(?:[-*]|\d+\.)\s+(?:\*\*[^*]+\*\*\s*)?)?', line).group(0)
        sub = bool(re.match(r'\s+\S', lead))
        top = re.match(r'[-*]\s+\*\*([^*]+?)\.\*\*', line)
        if top:
            field = top.group(1).lower()
        elif not sub and line.strip() and not line.lstrip().startswith(('-', '*')):
            field = ''
        instances = sub or field in ('on the page', 'appears in')
        if (sub or (instances and not top)) and late(line) or drafted(line[:120]) and sub:
            continue
        body = line[len(lead):]
        marks = []
        body = MARKSPAN.sub(lambda m: marks.append(m.group(0)) or f'\x00{len(marks) - 1}\x00', body)
        parts, held = [], ''
        for s in SENTENCE.split(body):
            if re.fullmatch(r'(?:\s*\x00\d+\x00)+\s*', s):
                held += s + ' '               # a mark governs the text after it
            elif parts and not re.sub(r'[\s\d:,;.()-]|M\d+', '', s):
                parts[-1] += ' ' + s          # a citation alone belongs to the sentence before
            else:
                parts.append(held + s)
                held = ''
        if held:
            parts.append(held.rstrip())
        unmark = lambda s: re.sub(r'\x00(\d+)\x00', lambda m: marks[int(m.group(1))], s)
        keep = [s for s in parts if not (page(unmark(s)) or drafted(unmark(s)) or (instances and late(unmark(s))))]
        body = unmark(' '.join(keep))
        for _ in range(2):  # a citation that holds a citation: (03000 (retired draft))
            body = re.sub(r'\s*(?<!\*)\((?:[^()]|\([^()]*\))*?\d{5}(?:[^()]|\([^()]*\))*?\)(?!\*)',
                          lambda m: '' if len(m.group(0).split()) <= 9 else m.group(0), body)
        body = re.sub(r'(\*\([^()\n]*?),?\s*\d{5}(?::\d+)?(?:\s*(?:outline|draft))?(?:\s*beat\s*\d+)?([.;)])', r'\1\2', body)   # a mark's own citation
        body = re.sub(r'(?:\s*\b\d{5}(?::\d+(?:-\d+)?)?\b[,;]?)+(?=\s*(?:\(M\d+\))?\s*$)', '', body)
        body = re.sub(r'\s*\(M\d+\)', '', body)
        body = re.sub(r'\s*\(\s*[\w./#-]+\.md(?:#[\w-]+)?\s*\)|`?\b[\w./-]+\.md(?:#[\w-]+)?\b`?', '', body)   # file names
        body = re.sub(r'\s+([.,;:])', r'\1', body).rstrip()
        if lead.strip() and not re.sub(r'[\s.,;:*()-]', '', body):
            continue
        out.append(lead + body)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip()


def as_fields(text):
    """A card's fields as the drafter reads them: "Field: text", marks plain, the list markup gone."""
    text = re.sub(r'^- \*\*([^*]+?)\.\*\*\s*', r'\1: ', text, flags=re.M)
    return re.sub(r'\*\(([^\n]*?)\)\*', r'(\1)', text)


CALLED = {}
DRAFT_CUT = {'appears in', 'open', 'origin and lineage', 'history'}
AHEAD = re.compile(r'^(in volume|in the .* arc|ahead|later|after\b|the war arc|forward|elsewhere)', re.I)


def all_fields(path):
    """Every top-level field on a card, in any section: {label lower: (label, text, section title)}. cards.fields
    reads a card's first section only, which is its form; an include may name a field further down."""
    out, sec, cur = {}, '', None
    lines = open(path, encoding='utf-8').read().split('\n')
    for line in lines:
        h = re.match(r'#+ (.*)', line)
        m = re.match(r'- \*\*([^*]+?)\.\*\*', line)
        if h:
            sec, cur = h.group(1).strip(), None
        elif m:
            cur = m.group(1).strip().lower()
            out.setdefault(cur, [m.group(1).strip(), [line], sec])
        elif cur and (line.startswith(' ') or line.startswith('\t')) and line.strip():
            out[cur][1].append(line)
        elif not line.strip():
            continue
        else:
            cur = None
    return {k: (v[0], '\n'.join(v[1]), v[2]) for k, v in out.items()}


MISSING = []


def rejoin(asked, order):
    """An include's fields split on commas; a label with a comma in it ("It pools by depth, above the water")
    comes back whole when its pieces, in the order written, make one of the card's labels."""
    out, i, asked = [], 0, list(asked)
    while i < len(asked):
        for j in range(len(asked), i, -1):
            joined = ', '.join(asked[i:j])
            if joined.lower() in order:
                out.append(joined)
                i = j
                break
        else:
            out.append(asked[i])
            i += 1
    return out


def drafter_fields(body):
    """A card or sheet as the drafter's bundle gives it: no bookkeeping field (Appears in, Open, Origin, History;
    Name stays, since it holds what the page calls a thing) and no field that looks ahead ("In volume 3", "Ahead", "Later")."""
    out, skip = [], False
    for line in body.split('\n'):
        m = re.match(r'- \*\*([^*]+?)\.\*\*', line)
        if m:
            lab = m.group(1).strip()
            skip = lab.lower() in DRAFT_CUT or bool(AHEAD.match(lab))
        elif skip and (not line.strip() or not line[:1].isspace()):
            skip = False
        if not skip:
            out.append(line)
    return '\n'.join(out)


def page_name(path, title, a):
    """How the drafter's bundle heads a card: what the page calls it (--called), else the card's title. A title is
    our label and can leak: "the man from the fork" before the fork is on the page."""
    if a.called and not CALLED:
        for line in open(a.called, encoding='utf-8'):
            if line.strip() and not line.startswith('#') and '\t' in line:
                k, v = line.rstrip('\n').split('\t', 1)
                CALLED[os.path.normpath(k.strip())] = [x.strip() for x in v.split(';') if x.strip()]
    names = CALLED.get(os.path.normpath(path))
    return ', '.join(names) if names else title


def kind_of(path, sheets):
    if path.startswith(sheets.rstrip('/') + '/'):
        return 'person'
    return os.path.basename(os.path.dirname(path)).replace('-', ' ')
DROP = ['author-side', 'reference', 'notes for markup', 'note changes implied', 'cards']
CITE = re.compile(r'\s*\((?:see\s+)?\[[^\]]*\]\([^)\s]*\)(?:[,;]?\s*(?:§\s*)?[\w.\- ]{0,30})?\)')


ASIDE = re.compile(r'\*\((?:author-side\b[^\n]*?|[^\n]*?(?:^|[;,:]\s*|\s)author-side(?:[,:.;]|\s+commentary|\s+only)[^\n]*?)\)\*', re.I)
QUALIFIED = re.compile(r'\b(?:count|counts|lengths?|numbers?|figures?|units?)\b[^;)]*author-side', re.I)
ANYMARK = re.compile(r'\*\([A-Z][^\n]*?\)\*')


def drop_asides(text):
    """Text marked author-side cut, from its mark to the next mark or the end of its paragraph or item: the
    drafter is never told what the page must not hold. A mark that makes only a figure author-side ("the count
    author-side") keeps its text, since the fact is on the page and only the number is not. A mark whose text
    says the line is author-side commentary is cut too."""
    out = []
    for para in re.split(r'(\n(?=\s*(?:[-*]|\d+\.)\s|#)|\n\n)', text):
        before = para
        while True:
            m = next((m for m in ANYMARK.finditer(para) if ASIDE.fullmatch(m.group(0)) and not QUALIFIED.search(m.group(0))
                      or re.search(r'author-side commentary|never reaches (?:her|his|their) mouth', m.group(0), re.I)), None)
            if not m:
                break
            nxt = next((n for n in ANYMARK.finditer(para, m.end())), None)
            para = para[:m.start()].rstrip() + (' ' + para[nxt.start():] if nxt else '')
        if para != before and re.fullmatch(r'\s*(?:[-*]|\d+\.)?\s*(?:\*\*[^*]+\*\*)?\s*', para) and para.strip():
            para = ''
        out.append(para)
    return re.sub(r'\n{3,}', '\n\n', ''.join(out))


def chapter_text(p, drop, cuts):
    """An outline or notes file as a drafter needs it: the navigation line and struck text gone, every section whose
    heading matches a --drop pattern left out (author-side, reference, the include list), parentheticals
    that only cite a source dropped, and the rest cut by the role's recipe (link targets, ruling IDs)."""
    out, skip = [], None
    for line in open(p, encoding='utf-8').read().split('\n'):
        h = re.match(r'(#+)\s+(.*)', line)
        if h:
            lv = len(h.group(1))
            if skip is not None and lv > skip:
                continue
            skip = lv if any(re.search(d, h.group(2), re.I) for d in drop) else None
            if skip is not None:
                continue
            out.append('#' + line)        # under the bundle's own headings
            continue
        if skip is not None:
            continue
        if re.fullmatch(r'\s*\[[^\]]*\]\([^)]*\)(\s*·\s*\[[^\]]*\]\([^)]*\))+\s*', line):
            continue                      # arc · previous · next
        if re.match(r'\s*-\s*\*\((author-side|reference)\b', line, re.I):
            continue
        line = CITE.sub('', re.sub(r'~~.*?~~\s*', '', line))   # struck text is withdrawn
        line = re.sub(r'\s*\(?`[^`\s]*\.md(?::[\d-]+)?`\)?', '', line)    # a file path: an invitation to open it
        if not line.strip(' -0-9.') and out and not out[-1].strip():
            continue
        line = cardtool.strip(line, cuts) if cuts else line
        out.append(line)
    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip()
    return re.sub(r'\*\((\w+(?: \w+)?)[,;:]?\s*\)\*', r'*(\1.)*', text).replace('.)*.)*', '.)*')


MANIFEST = []   # (path, what the bundle gave of it), for --manifest


def given(body):
    """What a block gave: its field labels, or its section headings, or 'whole'."""
    fs = re.findall(r'^- \*\*([^*]+?)\.\*\*', body, re.M)
    if fs:
        return 'fields: ' + '; '.join(dict.fromkeys(fs))
    hs = re.findall(r'^#+\s+(.+)$', body, re.M)
    return ('sections: ' + '; '.join(dict.fromkeys(hs))) if hs else 'whole'


def bundle(a, step, srcs, cards, links, incl, sheets, prev, between, named, other):
    want, smode, settled, cuts = load_recipes(a.recipes).get(step, RECIPES['drafter'])
    MANIFEST.extend((p, 'the chapter, inline' if a.inline else 'the chapter, by path') for p in srcs)
    cuts = [c for c in cuts.split(',') if c]
    aliases = cardtool.load_aliases(a.aliases) if a.aliases else {}
    role = [w.strip() for w in want.split(',') if w.strip()]
    role = None if role == ['*'] else role  # ['*', '-Field', ...]: every field but those
    said = (['only settled text'] if settled else []) + \
        (['cut: ' + ', '.join({'links': 'link targets', 'marks': 'marks', 'ids': 'ruling IDs'}.get(c, c) for c in cuts)] if cuts else [])
    out = [f'# Reading for {a.n} ({step})', '',
           'Built by `tools/reading.py --bundle`: the facts this role needs, from each card and sheet the chapter '
           'links. ' + (('; '.join(said))[:1].upper() + ('; '.join(said))[1:] + '. ' if said else '') +
           ('Everything this chapter needs from the cards and sheets is here, as the book stands before this chapter. '
            'Read only the files named below; search for nothing else. If a fact you need is missing, '
            'write it as a question in your report and go on.' if step in ASIDE_FREE else
            'Each block names its file: open it only if a fact you need is missing, and say so in your report.'), '']
    if step == 'drafter':
        out += ['## Rules (read these files)', '', *[f'- `{p}`' for p in a.rules if os.path.exists(p)],
                f'- two or three of `{a.samples}`', '']
    if a.inline:
        drop = a.drop if a.drop is not None else (DROP if step in ASIDE_FREE else [d for d in DROP if d != 'author-side'])  # critics check the page against the author-side text
        for p in srcs:
            what = "Outline" if "/outline/" in p else "Notes"
            out += [(f'## {what}' if step in ASIDE_FREE else
                     f'## {what} (`{p}`, cut: navigation, source citations, ' + ', '.join(drop) + ' sections'
                     + (', link targets, ruling IDs' if cuts else '') + ')'), '',
                    drop_asides(chapter_text(p, drop, [c for c in cuts if c != 'marks'])), '']
    else:
        out += ['## The chapter (read these files)', '', *[f'- `{p}` (whole)' for p in srcs], '']
    if role is None or role != []:
        blocks = []
        for t in cards:
            if incl.get(t) == ['cited']:
                MANIFEST.append((t, 'cited: not given'))
                continue  # a source the outline already quotes: the link stays, the card is not read
            # a role that reads everything reads the fields the chapter's include names; a role with
            # fields of its own (a critic's question) reads those
            every = role is None or role[0] == '*'
            if t in incl and every:  # an include's fields, in the card's own order (the form's)
                order = [f[0].lower() for f in cardtool.fields(t)]
                known = order + list(all_fields(t)) + [sections(t)[x][0].lower() for x in sections(t) if x]
                w = sorted(rejoin(incl[t], known), key=lambda x: order.index(x.lower()) if x.lower() in order else len(order))
            else:
                w = role
            S = sections(t)
            heads = {S[x][0].lower(): x for x in S if x}
            named_secs = [heads[x.lower()] for x in (w or []) if t in incl and x.lower() not in order and x.lower() in heads] \
                if t in incl and every else []   # an include may name a section of a card by its heading
            if named_secs:
                w = [x for x in w if x.lower() not in heads or x.lower() in order]
            later = []
            if t in incl and every:   # fields further down the card (past its first section), and names found nowhere
                af = all_fields(t)
                for x in list(w or []):
                    k = x.lower()
                    if k in order or k in heads:
                        continue
                    if k in af and not (step in ASIDE_FREE and 'author-side' in af[k][2].lower()):
                        later.append(af[k][1])
                    elif k != 'cited':
                        MISSING.append((t, x))
                w = [x for x in w if x.lower() in order or x.lower() in heads]
            body = card_text(t, links[t], w, settled, cuts, aliases) if (w or not (named_secs or later)) else ''
            if later:
                body = (body + '\n' + cut('\n'.join(later), settled, cuts)).strip()
            if named_secs:
                body = (body + '\n\n' + cut('\n\n'.join(lines_of(t, S[x][2], S[x][3]) for x in sorted(named_secs, key=lambda x: S[x][2])),
                                             settled, cuts)).strip()
            MANIFEST.append((t, given(body) if body.strip() else 'nothing asked for'))
            if body.strip():
                name = cardtool.head(t)[0]
                if step in ASIDE_FREE:
                    blocks += [f'### {page_name(t, name, a)} ({kind_of(t, a.sheets)})', '', demote(as_fields(so_far(drop_asides(drafter_fields(body)), a.n))), '']
                else:
                    blocks += [f'### {name} (`{t}`)', '', demote(body), '']
        if blocks:
            out += ['## Cards', ''] + blocks
    if smode != 'none' and sheets:
        out += ['## People', '']
        every = role is None or bool(role) and role[0] == '*'
        for sh in sorted(sheets):
            if incl.get(sh) == ['cited']:
                MANIFEST.append((sh, 'cited: not given'))
                continue
            if sh in incl and every and smode not in ('habits', 'size'):  # the include names the sheet's fields
                order = [f[0].lower() for f in cardtool.fields(sh)]
                known = order + list(all_fields(sh)) + [sections(sh)[x][0].lower() for x in sections(sh) if x]
                want = sorted(rejoin(incl[sh], known), key=lambda x: order.index(x.lower()) if x.lower() in order else len(order))
                body = card_text(sh, set(), [w for w in want if w.lower() in order], settled, cuts, aliases)
                if any(w.lower().startswith('habit') for w in want) and not any(o.startswith('habit') for o in order):
                    body = (body + '\n' + sheet_text(sh, 'habits', a, settled, cuts, aliases)).strip()  # Habits as a section
                af, S = all_fields(sh), sections(sh)
                heads = {S[x][0].lower(): x for x in S if x}
                later = []
                for x in want:
                    k = x.lower()
                    if k in order or k.startswith('habit'):
                        continue
                    if k in heads:
                        later.append(lines_of(sh, S[heads[k]][2], S[heads[k]][3]))
                    elif k in af and not (step in ASIDE_FREE and 'author-side' in af[k][2].lower()):
                        later.append(af[k][1])
                    else:
                        MISSING.append((sh, x))
                if later:
                    body = (body + '\n' + cut('\n'.join(later), settled, cuts)).strip()
            else:
                body = sheet_text(sh, smode, a, settled, cuts, aliases)
            MANIFEST.append((sh, given(body) if body.strip() else 'nothing'))
            if body.strip():
                if step in ASIDE_FREE:
                    out += [f'### {page_name(sh, cardtool.head(sh)[0], a)} (person)', '', demote(as_fields(so_far(drop_asides(drafter_fields(body)), a.n))), '']
                else:
                    out += [f'### {cardtool.head(sh)[0]} (`{sh}`)', '', demote(body), '']
    if named and step not in ASIDE_FREE:
        out += ['## Named but not linked', '', 'Not given here; open one only if a fact you need is missing.', '',
                ', '.join(f'`{t}`' for t in sorted(named)), '']
    if step in ('drafter', 'facts', 'setup', 'procedures', 'continuity'):
        out += ['## Prose (read these files)', '']
        if a.digest and os.path.exists(a.digest):
            out.append(f"- `{a.digest}`: what the volume's pages have already set; read whole, in place of the earlier chapters")
        if prev:
            out.append(f'- `{prev}`: the chapter before; read closely')
        for p in between:
            out.append(f'- `{p}`: kept between the chapter before and this one; skim')
        out.append('')
    return out


def main():
    ap = argparse.ArgumentParser(description="The reading list for one chapter's agents.")
    ap.add_argument('n')
    ap.add_argument('--step', default='drafter',
                    choices=['drafter', 'facts', 'setup', 'procedures', 'habits', 'continuity', 'scale'])
    ap.add_argument('--digest')
    ap.add_argument('--rules', nargs='*', default=['story/voice/voice.md', 'plan/workflows/drafting/rulings.md'])
    ap.add_argument('--sheets', default='story/notes/characters')
    ap.add_argument('--large', type=int, default=1500)
    ap.add_argument('--sheet-sections', nargs='*', default=['^at-a-glance$', '^habits', 'talks', '^who-(he|she|they)-(is|are)', 'tells', 'voice'],
                    help="for the drafter, the sheet sections to read, by heading anchor pattern, first match of each in this order")
    ap.add_argument('--sheet-budget', type=int, default=2200, help="for the drafter, the most words read from one sheet")
    ap.add_argument('--not-before', help='a pattern for prose files never taken as "the chapter before" (e.g. fragments, '
                    '-F[0-9]); one that falls between the chapter before and this one is listed to skim')
    ap.add_argument('--bundle', action='store_true',
                    help='print the text the role reads (fields cut by its recipe, sheets by section), not a list of files')
    ap.add_argument('--recipes', help='for --bundle: a file of recipes, one role a row: role, card fields, sheets, settled (yes/no), cut')
    ap.add_argument('--aliases', help='for --bundle: the questions file cards.py get reads (size, usage, ...)')
    ap.add_argument('--called', help="for the drafter's bundle: a file of card<TAB>what the page calls it, to head each "
                    "card or sheet by its page name instead of its title (a title can name what the page has not shown yet)")
    ap.add_argument('--suggest', type=int, nargs='?', const=30, default=0,
                    help='print up to N candidate include lines (default 30): cards named or matched by a keyword but not linked')
    ap.add_argument('--manifest', help='for --bundle: also write what the bundle gave of each file (fields, sections, '
                    'cited, named) to this file, for gaps.py to trace a critic\'s finding to its source')
    ap.add_argument('--inline', action='store_true',
                    help='for --bundle: put the outline and notes in the bundle, cut for the role, in place of naming the files')
    ap.add_argument('--drop', nargs='*', help='for --inline: heading patterns whose sections are left out '
                    '(default: author-side, reference, notes for markup, note changes implied, cards)')
    ap.add_argument('--samples', default='story/voice/samples/', help="the drafter's style samples folder")
    ap.add_argument('--named', choices=['list', 'read', 'off'], default='list',
                    help='cards the outline or notes name without linking: list them apart, not to read '
                         '(default); read them with the linked cards (a book whose notes link little); or leave them out')
    a = ap.parse_args()
    N, step = a.n, a.step
    srcs = [p for p in (sorted(glob.glob(f'story/outline/{N}-*.md')) + sorted(glob.glob(f'story/notes/{N}-*.md')))]
    if not srcs:
        raise SystemExit(f'no outline or notes for {N}')

    links = collections.defaultdict(set)
    incl = {}
    for p in srcs:
        for m in re.finditer(r'\]\(([^)\s]+)\)', open(p, encoding='utf-8').read()):
            f, _, an = m.group(1).partition('#')
            if re.match(r'^[a-z]+:', f):
                continue
            t = os.path.normpath(os.path.join(os.path.dirname(p), f)) if f else p
            if t in srcs or not t.endswith('.md') or not os.path.exists(t):
                continue
            links[t].add(an)
        under = False
        for line in open(p, encoding='utf-8'):  # an include, under a Cards heading: "- [card](path): Body, Size"
            h = re.match(r'#+\s+(.*)', line)
            if h:
                under = bool(re.fullmatch(r'cards\b.*', h.group(1).strip(), re.I))
                continue
            m = INCLUDE.match(line) if under else None
            if m:
                f, _, an = m.group(1).partition('#')
                t = os.path.normpath(os.path.join(os.path.dirname(p), f))
                incl.setdefault(t, []).extend(x.strip() for x in m.group(2).rstrip('.').split(',') if x.strip())

    text = ' '.join(open(p, encoding='utf-8').read() for p in srcs).lower()
    sheets = {t for t in links if t.startswith(a.sheets.rstrip('/') + '/')}
    for sh in glob.glob(os.path.join(a.sheets, '*.md')):  # a sheet's own subfolder counts only when linked
        if os.path.basename(sh) == 'README.md':
            continue
        stem = os.path.basename(sh)[:-3].replace('-', ' ')
        first = open(sh, encoding='utf-8').readline().lstrip('# ').split(':')[0].split('(')[0].strip().lower()
        if any(len(nm) > 3 and re.search(r'\b' + re.escape(nm) + r'\b', text) for nm in {stem, first}):
            sheets.add(os.path.normpath(sh))

    # cards the outline or notes name without linking: by the card's name or a
    # person's first name (two capitalized words). Keywords are search words, not
    # names, and match far too much to read.
    raw = ' '.join(open(p, encoding='utf-8').read() for p in srcs)
    named = set()
    for c in glob.glob('world/**/*.md', recursive=True) if a.named != 'off' else []:
        c = os.path.normpath(c)
        if os.path.basename(c) in ('README.md', 'INDEX.md') or c in links:
            continue
        nm = open(c, encoding='utf-8').readline().lstrip('# ').split(':')[0].strip()
        term = re.sub(r'^(the|a|an) ', '', nm.lower())
        hit = len(term) > 3 and bool(re.search(r'\b' + re.escape(term) + r'\b', text))
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', nm):
            hit = hit or bool(re.search(r'\b' + nm.split()[0] + r'\b', raw))
        if hit:
            named.add(c)
    if a.named == 'read':
        for c in named:
            links[c].add('')
        named = set()

    if a.suggest:  # candidate includes for the author: named cards, and cards a Keywords word of theirs matches
        words = {re.sub(r'(?<=[a-z]{3})(es|s)$', '', w) for w in re.findall(r'[a-z][a-z-]{3,}', text)}
        score = {}
        for c in glob.glob('world/**/*.md', recursive=True) + glob.glob(os.path.join(a.sheets, '*.md')):
            c = os.path.normpath(c)
            if os.path.basename(c) in ('README.md', 'INDEX.md') or c in links:
                continue
            name, _, _, kw, _ = cardtool.head(c)
            hits = sorted({k for k in (x.lower() for x in kw)
                           if (' ' in k and re.search(r'\b' + re.escape(k) + r'\b', text))
                           or (' ' not in k and (re.sub(r'(?<=[a-z]{3})(es|s)$', '', k) in words
                                                 or any(len(w) >= 5 and k.endswith(w) and k != w for w in words)))})
            term = re.sub(r'^(the|a|an) ', '', name.lower())
            by_name = c in named and (' ' in term or bool(hits))   # a one-word name ("Open", "Land") alone matches far too much
            if by_name or len(hits) >= 2:   # one keyword alone ("village", "path") is a search word, not a mention
                score[c] = (2 if by_name else 0) + len(hits), name, hits, by_name
        for sh in glob.glob(os.path.join(a.sheets, '**', '*.md'), recursive=True):  # a sheet whose Appears in names the chapter
            sh = os.path.normpath(sh)
            if os.path.basename(sh) == 'README.md' or sh in links or sh in incl:
                continue
            ap = next((f[3] for f in cardtool.fields(sh) if f[0].lower() == 'appears in'), '')
            if re.search(r'\b' + re.escape(N) + r'\b', ap):
                s, name, hits, _ = score.get(sh, (0, cardtool.head(sh)[0], [], False))
                score[sh] = (s + 3, name, hits, 'appears')
        notes = next((p for p in srcs if '/notes/' in p), srcs[-1])
        print(f'# Includes to consider for {N}: cards the outline and notes name or match by a keyword, not linked')
        print('# Paste the right ones under the notes\' Cards heading, with the fields the chapter needs.\n')
        for c, (s, name, hits, by_name) in sorted(score.items(), key=lambda x: (-x[1][0], x[0]))[:a.suggest]:
            why = ('its Appears in lists ' + N if by_name == 'appears' else 'named' if by_name else '') + (('; ' if by_name and hits else '') + 'keywords: ' + ', '.join(hits) if hits else '')
            print(f'- [{name}]({os.path.relpath(c, os.path.dirname(notes))}):   <!-- {why} -->')
        return

    allp = sorted(p for p in glob.glob('story/prose/*.md') if os.path.basename(p) < N)
    side = lambda p: bool(a.not_before and re.search(a.not_before, os.path.basename(p)))
    prose = [p for p in allp if not side(p)]
    prev = prose[-1] if prose else None
    between = [p for p in allp if side(p) and prev and os.path.basename(p) > os.path.basename(prev)]
    cards = sorted(t for t in links if t not in sheets and t.startswith('world/'))
    other = sorted(t for t in links if t not in sheets and t not in cards and t.startswith(('story/outline/', 'story/notes/')))  # the voice rules, plans and prose are listed elsewhere or not at all

    out = [f'# Reading list for {N} ({step})', '',
           'Built by `tools/reading.py`. Read these and nothing else, unless a fact you need is missing; '
           'then follow one link and say so in your report.', '']
    if step == 'drafter':
        out += ['## Rules', '', *[f'- `{p}`' for p in a.rules if os.path.exists(p)],
                f'- two or three of `{a.samples}`', '']
    out += ['## The chapter', '', *[f'- `{p}` (whole)' for p in srcs], '']
    stubs = [t for t in cards if is_stub(t)]
    for t in stubs:  # a stub is a head and its cited lines: build it before an agent reads it as the card
        print(f'reading.py: {t} is a stub; build it from its cited lines before drafting', file=sys.stderr)
    if step in ('drafter', 'facts', 'setup', 'procedures'):
        if stubs:
            out += ['## Stubs to build first', '',
                    'These cards are stubs (a head and the lines that cite the thing). Build each from its cited '
                    'lines, by card-existing, before this chapter is drafted or checked.', '',
                    *[f'- `{t}`' for t in stubs], '']
        out += ['## Cards and sections', '', *[fmt(t, links[t], a.large) for t in cards], '']
        if named:
            out += ['## Named but not linked', '',
                    'The outline or notes name these cards without linking them. Do not read them; open one only '
                    'if a fact you need is missing, and say so in your report.', '',
                    ', '.join(f'`{t}`' for t in sorted(named)), '']
        if other:
            out += ['## Linked but not to read', '',
                    "Other chapters' outlines and method notes. The chapter's own outline and notes carry what "
                    'binds it; open one only if a settled line there is quoted to you as a conflict.', '',
                    ', '.join(f'`{t}`' for t in other), '']
    if step in ('drafter', 'facts', 'setup', 'habits'):
        out += ['## People', '']
        for sh in sorted(sheets):
            if step == 'habits':
                out.append(habits_of(sh, a.large))
            elif step == 'facts':
                S = sections(sh)
                out.append(fmt(sh, links.get(sh, set()) | {x for x in S if x and S[x][1] <= 2 and 'glance' in x}, a.large))
            else:  # drafter and setup: the sections that carry the person, not the whole sheet
                out.append(drafter_sheet(sh, a))
        out.append('')
    if step in ('drafter', 'facts', 'setup', 'procedures', 'continuity'):
        out += ['## Prose', '']
        if a.digest and os.path.exists(a.digest):
            out.append(f"- `{a.digest}`: what the volume's pages have already set; read whole, in place of the earlier chapters")
        if prev:
            out.append(f'- `{prev}`: the chapter before; read closely')
        for p in between:
            out.append(f'- `{p}`: kept between the chapter before and this one; skim')
        out.append('')
    if a.bundle:
        out = bundle(a, step, srcs, cards, links, incl, sheets, prev, between, named, other)
        for card, x in MISSING:  # an include named a field the card does not have: say so, never drop it silently
            print(f'reading.py: {card} has no field or section "{x}" (named in the Cards block)', file=sys.stderr)
            MANIFEST.append((card, f'not found: {x}'))
        MANIFEST.extend((t, 'named, not given') for t in sorted(named))
        if a.manifest:
            with open(a.manifest, 'w', encoding='utf-8') as f:
                import subprocess
                rev = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
                f.write(f'# What the {step} bundle for {a.n} gave, by file (reading.py --manifest): path<TAB>given\n')
                f.write(f'# commit {rev or "none"}\n')
                f.writelines(f'{p}\t{g}\n' for p, g in MANIFEST)
    print('\n'.join(out))


if __name__ == '__main__':
    main()
