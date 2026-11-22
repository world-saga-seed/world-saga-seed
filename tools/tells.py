#!/usr/bin/env python3
"""Texture numbers for drafted chapters, and a scan for banned words.

Model-written prose gives itself away by rhythm more than by vocabulary: the
same simile frame, long "and" chains, paragraphs that end on a short kicker,
too many negations. This tool measures those on the narration (text outside
double quotes), so a chapter can be set beside the writer's own samples.

Usage:
  python3 tools/tells.py FILE [FILE ...] [--banned LIST] [--stop REGEX] [--all-text]
                         [--sample FILE ...]

  FILE          markdown chapters; headings (# lines) are ignored
  --banned LIST a word list: one word or phrase per line, matched as whole
                words, case ignored; a line starting "re:" is a regular
                expression; lines starting "#" are comments
  --stop REGEX  ignore everything from the first line matching REGEX
                (default "^## Notes", so notes kept under a draft are skipped)
  --all-text    scan dialogue too when looking for banned words
                (by default only narration is scanned)
  --sample FILE the voice sample (one or more files, pooled): under each
                chapter, an "over the sample" line where short/k, run or
                trip/k runs well past the sample's own, and a "spelling" line
                for each word the sample prints another way (colour/color,
                -ise/-ize, centre/center, travelled/traveled, grey/gray)

Per file it prints one line of numbers:
  w            narration words
  way/k        "the way you / the way a ..." similes per 1,000 words
  asif/k       "as if / as though" per 1,000 words
  and/s        "and" per sentence
  neg/k        negations (not, no, nothing, never, nobody, none) per 1,000 words
  med, sd      median and spread of sentence length in words
  short%       sentences of 6 words or fewer;  long%  sentences of 25 or more
  button%      paragraphs of two sentences or more that end on one of 5 words or fewer
  short/k      short narration sentences (under 8 words) per 1,000 words of
               narration sentences; a sentence holding dialogue is skipped
  run          the longest run of short narration sentences in a row: a
               chapter can match the averages and still read clipped in a cluster
  trip/k       rhythm triplets ("dry, warm, and snug") per 1,000 words; a list
               of things counts too, so read it against the sample's own rate
Under it, a "knot" line for each narration sentence of 35 words or more that
holds a semicolon: two main clauses run through one read as a tangle (a list
held by semicolons is fine; the reviser splits the rest).
Then any banned-word hits as  file:line  word  | the line.
Read the numbers against the same numbers for the writer's own pages; there is
no universal good value.
"""
import argparse, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import context  # noqa: E402  (the shared pattern matcher, for the banned-word scan)


QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')


def load_banned(path):
    rx = []
    for line in open(path, encoding='utf-8'):
        t = line.strip()
        if not t or t.startswith('#'):
            continue
        if t.startswith('re:'):
            rx.append((t, re.compile(t[3:].strip(), re.I)))
        else:
            rx.append((t, re.compile(r'\b' + re.escape(t) + r'\b', re.I)))
    return rx


def body_lines(path, stop):
    out = []
    for line in open(path, encoding='utf-8').read().split('\n'):
        if stop and re.search(stop, line):
            break
        out.append(line)
    return out


SPLIT = re.compile(r'(?<=[.!?])["”’)]*\s+(?=["“‘(]?[A-Z])')
TRIPLET = re.compile(r"\b[\w'’-]+(?: [\w'’-]+){0,2}, [\w'’-]+(?: [\w'’-]+){0,2},? (?:and|or) [\w'’-]+(?: [\w'’-]+){0,2}\b")


def shape(text):
    """Short narration sentences, the words they are counted over, and the longest run."""
    short = words = longest = 0
    for p in text.split('\n\n'):
        cur = 0
        for s in SPLIT.split(p.strip()):
            if re.search(r'["“”]', s):      # a sentence holding dialogue: skipped, and it ends a run
                cur = 0
                continue
            n = len(s.split())
            words += n
            if 0 < n < 8:
                short += 1
                cur += 1
                longest = max(longest, cur)
            else:
                cur = 0
    return short, words, longest


PAIRS = {'grey': 'gray', 'plough': 'plow', 'mould': 'mold', 'sceptic': 'skeptic', 'whilst': 'while'}


def variants(w):
    """The other spellings of a word: -our/-or, -ise/-ize, -re/-er, -ll-/-l-, and a few pairs."""
    out = set()
    for a, b in PAIRS.items():
        if w == a: out.add(b)
        if w == b and b != 'while': out.add(a)
    m = re.match(r"^(\w{3,}?)(our|or)(s|ed|ing|ite|ites|able|ful)?$", w)
    if m and not m.group(1).endswith('o'):   # floor is not flour
        out.add(m.group(1) + ('or' if m.group(2) == 'our' else 'our') + (m.group(3) or ''))
    m = re.match(r'^(\w{3,}?)(is|iz)(e|es|ed|ing|ation|ations)$', w)
    if m:
        out.add(m.group(1) + ('iz' if m.group(2) == 'is' else 'is') + m.group(3))
    m = re.match(r'^(\w{3,}?)(re|er)(s)?$', w)
    if m:
        out.add(m.group(1) + ('er' if m.group(2) == 're' else 're') + (m.group(3) or ''))
    m = re.match(r'^(\w{4,}?)(ll|l)(ed|ing|er|ers|ous)$', w)
    if m and m.group(1)[-1] in 'aeiou':   # travel-led, never fill-ed for filed
        out.add(m.group(1) + ('l' if m.group(2) == 'll' else 'll') + m.group(3))
    out.discard(w)
    return out


def spellings(text, sample_words):
    words = set(re.findall(r"[a-z]+", text.lower()))
    found = []
    for w in sorted(words):
        if w in sample_words:
            continue
        other = sorted(v for v in variants(w) if v in sample_words)
        if other:
            found.append(f'{w} (sample: {other[0]})')
    return found


def numbers(lines, counts=()):
    text = '\n'.join('' if l.startswith('#') else l for l in lines)
    narr = QUOTED.sub('', text)
    words = narr.split()
    w = max(1, len(words))
    sents = [s for s in re.split(r'[.!?]+(?:\s|$)', narr) if s.strip()]
    lens = sorted(len(s.split()) for s in sents) or [0]
    mean = sum(lens) / len(lens)
    sd = (sum((x - mean) ** 2 for x in lens) / len(lens)) ** .5
    paras = [QUOTED.sub('', p) for p in text.split('\n\n') if p.strip() and not p.lstrip().startswith(('"', '“'))]
    multi = [[s for s in re.split(r'(?<=[.!?])\s+', p.strip()) if s.split()] for p in paras]
    multi = [s for s in multi if len(s) >= 2]
    c = lambda rx: len(re.findall(rx, narr, re.I))
    return {
        'w': len(words),
        'way/k': 1000 * c(r'\bthe way (you|a|an|he|she|they|it|people|somebody|someone|anybody|anyone)\b') / w,
        'asif/k': 1000 * c(r'\bas (if|though)\b') / w,
        'and/s': c(r'\band\b') / max(1, len(sents)),
        'neg/k': 1000 * c(r'\b(not|no|nothing|never|nobody|none)\b') / w,
        'med': lens[len(lens) // 2],
        'sd': sd,
        'short%': 100 * sum(x <= 6 for x in lens) / len(lens),
        'long%': 100 * sum(x >= 25 for x in lens) / len(lens),
        'button%': 100 * sum(len(s[-1].split()) <= 5 for s in multi) / max(1, len(multi)),
        'knots': [s.strip() for s in sents if ';' in s and len(s.split()) >= 35],
        'short/k': 1000 * shape(text)[0] / max(1, shape(text)[1]),
        'run': shape(text)[2],
        'trip/k': 1000 * len(TRIPLET.findall(narr)) / w,
        'text': text,
        'counts': [(name, 1e4 * c(rx) / w) for name, rx in counts],
    }


def main():
    ap = argparse.ArgumentParser(description='Texture numbers and banned-word scan for chapters.')
    ap.add_argument('files', nargs='+', help='chapter files to measure')
    ap.add_argument('--banned', help='banned list: one word or phrase per line; re: starts a regex; # a comment')
    ap.add_argument('--stop', default=r'^## Notes', help='stop reading a file at a line matching this regex (default: ^## Notes)')
    ap.add_argument('--all-text', action='store_true', help='scan dialogue for banned words too')
    ap.add_argument('--count', action='append', default=[], metavar='NAME=REGEX',
                    help='also count a pattern in narration, per 10,000 words (repeatable), for a habit of your own narrator')
    ap.add_argument('--sample', nargs='+', metavar='FILE', help='the voice sample: flag measures well past it, and spellings it prints another way')
    a = ap.parse_args()
    banned = load_banned(a.banned) if a.banned else []
    base = None
    if a.sample:
        st = '\n\n'.join('\n'.join(body_lines(f, a.stop)) for f in a.sample)
        base = numbers(st.split('\n'))
        base_words = set(re.findall(r'[a-z]+', QUOTED.sub('', base['text']).lower()))
    hits = []
    for f in a.files:
        lines = body_lines(f, a.stop)
        n = numbers(lines, [tuple(x.split('=', 1)) for x in a.count])
        name = f.replace('\\', '/').split('/')[-1][:30]
        print(f"{name:30} w={n['w']:5} way/k={n['way/k']:4.1f} asif/k={n['asif/k']:4.1f} "
              f"and/s={n['and/s']:.2f} neg/k={n['neg/k']:4.1f} med={n['med']:2} sd={n['sd']:4.1f} "
              f"short%={n['short%']:3.0f} long%={n['long%']:3.0f} button%={n['button%']:3.0f}"
              f" short/k={n['short/k']:4.1f} run={n['run']} trip/k={n['trip/k']:4.1f}"
              + ''.join(f" {k}/10k={v:4.1f}" for k, v in n['counts']))
        for k in n['knots']:
            print(f"    knot ({len(k.split())} words): {' '.join(k.split())[:160]}")
        if base is not None:
            over = []
            if n['short/k'] > 1.5 * base['short/k'] and n['short/k'] - base['short/k'] > 2:
                over.append(f"short/k {n['short/k']:.1f} (sample {base['short/k']:.1f})")
            if n['run'] >= 3 and n['run'] > base['run'] + 1:
                over.append(f"run {n['run']} (sample {base['run']})")
            if n['trip/k'] > 1.5 * base['trip/k'] and n['trip/k'] - base['trip/k'] > 1:
                over.append(f"trip/k {n['trip/k']:.1f} (sample {base['trip/k']:.1f})")
            if over:
                print('    over the sample: ' + '; '.join(over))
            sp = spellings(QUOTED.sub('', n['text']), base_words)
            if sp:
                print('    spelling: ' + ', '.join(sp))
        if banned:
            pats = [{'label': j, 're': rx, 'near_re': None, 'unless_re': None, 'within': 0,
                     'narration': not a.all_text} for j, (label, rx) in enumerate(banned)]
            found = context.find(f, pats, a.stop, merge_sentences=False)[2]
            for h in sorted(found, key=lambda h: (h['line'], h['label'], h['col'])):
                hits.append(f'{f}:{h["line"]}  {h["match"]}  | {lines[h["line"] - 1].strip()[:100]}')
    if banned:
        print(f'\n{len(hits)} banned-word hits' + (':' if hits else ''))
        for h in hits:
            print(h)


if __name__ == '__main__':
    main()
