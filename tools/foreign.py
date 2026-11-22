#!/usr/bin/env python3
"""Source-language spans left in the narration of a book written from a source in another language.

A run that works from a French (or German, Spanish, Italian) source drifts: a
clause of the source slips into the English narration, or into a note. Quoting
the source is fine; leaving it unquoted is not. This finds the unquoted spans:
any four words in a row of which three are markers of the source language
(its function words, or a word with a letter English does not use, such as é
or ß), outside quotes. A single loanword ("café") or a fixed phrase of two
markers ("a la carte") is too short to count. Common English words at a span's
ends are trimmed off.

Usage:
  python3 tools/foreign.py FILE|FOLDER [...] [--lang fr|de|es|it] [--words LIST] [--stop REGEX]

  --lang L      the source language's function words (fr, de, es, it); repeatable
  --words LIST  markers of your own, one per line, "#" a comment (for another
                language, or a source's own names and terms)
  --stop REGEX  ignore everything from the first line matching REGEX (default "^## Notes")

Prints each span as  file:line  span | the line, then a count. Text inside
straight, curly or guillemet quotes is set aside, and so is a
line in the kit's quote form, "- quote: the exact words". Sort the finds by hand or
with a cheap finder: a span may be a quotation that lost its marks (restore
them), a name (keep it), or drift (put it in the working language).
"""
import argparse, os, re

# Function words, minus any that are also common English words (on, son, pour, par, plus, ...).
LANGS = {
    'fr': 'le la les un une des du de et est à au aux en dans sur avec que qui ne pas il elle ils elles nous vous '
          'je sa ses leur leurs ce cette ces été était étaient sont avait avaient mais où donc ni car lui leur dont '
          'très bien aussi comme être avoir fait cela ceci ici',
    'de': 'der die das und ist nicht ein eine einen einem dem des mit von zu auf für sich auch als wie aber nach bei '
          'aus wenn noch nur ich du er sie wir ihr es sind haben wird wurde mehr sehr schon keine kein',
    'es': 'el los las un una unos unas y es en de del al que por para se su sus le les pero como más muy ya está '
          'están fue era sido hay entre sin sobre también',
    'it': 'il lo la gli le un una uno e è di da su che non si ma più anche del della dei delle nel nella al alla '
          'sono era stato questo questa quello quella',
}
ENGLISH = set('the a an and or but of to in at on by for with as from that this these those he she it they we you i '
              'was were is are be been his her its their our then there so not no all said had has have'.split())
FOREIGN_LETTERS = re.compile(r'[àâäçéèêëîïôöùûüÿñßœæåøąćęłńśźżčřšžőű]', re.I)
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”|«[^»\n]*»')
QUOTE_LINE = re.compile(r'^\s*[-*]\s+quote:', re.I)
WORD = re.compile(r"[^\W\d_][\w'’-]*", re.U)


def load_words(path):
    out = set()
    for line in open(path, encoding='utf-8'):
        t = line.strip().lower()
        if t and not t.startswith('#'):
            out.add(t)
    return out


def spans(line, markers):
    blank = QUOTED.sub(lambda m: ' ' * len(m.group(0)), line)
    q = QUOTE_LINE.match(blank)
    if q:  # the kit's quote form, "- quote: the exact words": a quotation
        blank = blank[:q.end()] + ' ' * (len(blank) - q.end())
    toks = [(m.start(), m.end(), m.group(0)) for m in WORD.finditer(blank)]
    low = [t[2].lower().strip("'’-") for t in toks]
    mark = [w not in ENGLISH and (w in markers or bool(FOREIGN_LETTERS.search(w))) for w in low]
    hit = [False] * len(toks)
    for i in range(len(toks) - 3):
        if sum(mark[i:i + 4]) >= 3:
            for j in range(i, i + 4):
                hit[j] = True
    out, i = [], 0
    while i < len(toks):
        if not hit[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(toks) and hit[j + 1]:
            j += 1
        a, b = i, j
        while a < b and low[a] in ENGLISH:
            a += 1
        while b > a and low[b] in ENGLISH:
            b -= 1
        out.append(line[toks[a][0]:toks[b][1]])
        i = j + 1
    return out


def main():
    ap = argparse.ArgumentParser(description='Find source-language spans outside quotes.')
    ap.add_argument('files', nargs='+')
    ap.add_argument('--lang', action='append', default=[], choices=sorted(LANGS), help='the source language (repeatable)')
    ap.add_argument('--words', action='append', default=[], help='a file of markers of your own, one per line')
    ap.add_argument('--stop', default=r'^## Notes', help='stop reading a file at a line matching this regex')
    a = ap.parse_args()
    if not a.lang and not a.words:
        ap.error('name the source language with --lang, or give markers with --words')
    markers = set()
    for l in a.lang:
        markers |= set(LANGS[l].split())
    for w in a.words:
        markers |= load_words(w)
    files = []
    for f in a.files:  # a folder: every .md file under it
        if os.path.isdir(f):
            files += sorted(os.path.join(d, x) for d, _, fs in os.walk(f) for x in fs if x.endswith('.md'))
        else:
            files.append(f)
    n = 0
    for f in files:
        for k, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            if a.stop and re.search(a.stop, line):
                break
            if line.startswith('#'):
                continue
            for s in spans(line, markers):
                n += 1
                print(f'{f}:{k}  {s}  | {line.strip()[:100]}')
    print(f'{n} spans')


if __name__ == '__main__':
    main()
