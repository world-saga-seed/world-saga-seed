#!/usr/bin/env python3
"""Build an EPUB from drafted chapters, so the writer can read a volume as a reader would.

Each chapter becomes its own page named for its file, and every paragraph
carries its source line number as an id (p87 is line 87), so a highlight made
on the ereader can be traced back to the exact line of the source file.

Two ways to name the chapters:

  1. List the files, in order:
       python3 tools/epub.py --title "Volume 1" --out build/volume-1.epub story/prose/00*.md

  2. Give a number range, and let outlined chapters with no prose yet show
     as "[Not yet drafted.]" pages, so the gaps are visible where they fall:
       python3 tools/epub.py --title "Volume 1" --out build/volume-1.epub \\
           --prose story/prose --outline story/outline --from 100 --to 2000

  Chapter files are named by number and slug: 00100-the-causeway.md.

Options:
  --title T        the book's title (required)
  --author A       the author line (default: "Unknown")
  --series S       a series name; with --index N, readers that group series will
  --index N        group the books (EPUB 3 and calibre metadata both)
  --front FILE     a front-matter page set before the first chapter; if the
                   file has a line "---", only what follows it is used; "[Title]"
                   in it becomes the series and title. Repeat for more pages
                   (a copyright page, then a "before you begin"), in order;
                   "TITLE=FILE" sets the page's title in place of its heading
  --rights TEXT    the rights line in the book's metadata
  --cover          a plain typeset cover (the series, the title split at ": ",
                   the author) as the first page, in place of the title page;
                   needs Pillow, and is left out with a note if it is missing
  --skip N,N       chapter numbers left out (with --from and --to)
  --merged-mark T  an outlined slot with no prose whose outline holds T (for
                   example "**Merged into") gets no placeholder page
  --uid-seed S     what the book's identifier is made from (default: the title);
                   keep it fixed so a rebuilt book is the same book to the reader
  --out FILE       where to write the .epub (folders are created)
  --no-kepub       build the plain EPUB only; by default kepubify (if installed)
                   also makes FILE.kepub.epub for Kobo readers (--kepub, the
                   old switch, is still taken and does nothing more)

What goes in: each file's text only. The first "# " line is the chapter title
(a trailing "(draft N)" is dropped); other headings become subheads; "---" is a
scene break; <!-- comments --> are dropped; *italic* and **bold** are kept.
Standard library only. Check the result with epubcheck if you have it.
"""
import argparse, glob, html, io, os, re, shutil, subprocess, sys, uuid, zipfile, datetime

CSS = """html { font-size: 100%; }
body { margin: 0 4%; font-size: 1em; line-height: 1.35; }
h1 { text-align: center; margin: 30% 0 0.5em; font-size: 1.8em; font-weight: normal; }
h2 { text-align: center; margin: 2em 0 1.5em; font-size: 1.4em; font-weight: normal; }
h3 { text-align: center; font-size: 1.1em; font-weight: normal; }
p { margin: 0; text-indent: 1.4em; text-align: justify; }
h2 + p, p.break + p { text-indent: 0; }
p.break { text-align: center; text-indent: 0; margin: 0.8em 0; }
p.placeholder, p.byline { text-indent: 0; text-align: center; }
body.front { font-family: sans-serif; font-size: 0.92em; }
body.front p { text-indent: 0; text-align: left; margin: 0 0 0.75em; }
body.front h3 { margin: 1.6em 0 0.6em; font-size: 1.05em; font-variant: small-caps; letter-spacing: 0.04em; }
body.front ul { margin: 0 0 0.75em 1.2em; padding: 0; }
body.front li { margin: 0 0 0.3em; }
body.copyright { font-size: 0.78em; line-height: 1.25; }
body.copyright h2 { margin: 0.5em 0 1em; }
body.copyright p { margin: 0 0 0.5em; }
p.placeholder { color: #666; }
"""
FONTS = ['/mnt/c/Windows/Fonts/georgia.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
         '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/Library/Fonts/Georgia.ttf', 'C:/Windows/Fonts/georgia.ttf']


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    return s


def chapter(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    title, body, comment = None, [], False
    for n, line in enumerate(lines, 1):
        t = line.strip()
        if comment or t.startswith('<!--'):
            comment = '-->' not in t
            continue
        if not t:
            continue
        if t.startswith('# ') and title is None:
            title = re.sub(r'\s*\(draft \d+\)\s*$', '', t[2:]).strip()
            continue
        if t.startswith('#'):
            body.append(f'<h3 id="p{n}">{inline(t.lstrip("#").strip())}</h3>')
        elif t in ('---', '* * *', '***'):
            body.append(f'<p id="p{n}" class="break">*</p>')
        else:
            body.append(f'<p id="p{n}">{inline(t)}</p>')
    return title or os.path.splitext(os.path.basename(path))[0], body


def front(path, full_title=''):
    text = open(path, encoding='utf-8').read()
    title = 'Before you begin'
    first = text.split('\n', 1)[0]
    if first.startswith('# '):
        title = first[2:].strip()
    if '\n---\n' in text:
        text = text.split('\n---\n', 1)[1]
    elif first.startswith('# '):
        text = text.split('\n', 1)[1] if '\n' in text else ''
    body, in_list = [], False
    for t in (l.strip() for l in text.split('\n')):
        if t.startswith('- '):
            if not in_list:
                body.append('<ul>')
                in_list = True
            body.append(f'<li>{inline(t[2:])}</li>')
            continue
        if in_list:
            body.append('</ul>')
            in_list = False
        if not t or t == '---':
            continue
        if t.startswith('# '):
            title = t[2:].strip()
        elif t.startswith('#'):
            body.append(f'<h3>{inline(t.lstrip("#").strip())}</h3>')
        else:
            body.append(f'<p>{inline(t)}</p>')
    if in_list:
        body.append('</ul>')
    if full_title:
        body = [b.replace('[Title]', html.escape(full_title, quote=False)) for b in body]
    return title, body


def cover(series, title, author):
    """A plain typeset cover, JPEG at 1072x1448, or None without Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    W, H = 1072, 1448
    img = Image.new('L', (W, H), 245)
    d = ImageDraw.Draw(img)

    def font(size):
        for f in FONTS:
            if os.path.exists(f):
                return ImageFont.truetype(f, size)
        return ImageFont.load_default()

    def centered(text, y, size, fill=20):
        f = font(size)
        w = d.textbbox((0, 0), text, font=f)[2]
        d.text(((W - w) / 2, y), text, font=f, fill=fill)
    number, _, rest = title.partition(': ')
    d.rectangle((60, 60, W - 60, H - 60), outline=60, width=4)
    if series:
        centered(series.upper(), 310, 54)
        d.line((W / 2 - 140, 430, W / 2 + 140, 430), fill=60, width=3)
    if rest:
        centered(number, 560, 72, 60)
        centered(rest, 680, 96)
    else:
        centered(number, 620, 96)
    centered(author, H - 260, 56, 60)
    buf = io.BytesIO()
    img.convert('RGB').save(buf, 'JPEG', quality=90)
    return buf.getvalue()


def page(title, body, cls='', heading=True):
    h = f'<h2>{html.escape(title, quote=False)}</h2>\n' if heading else ''
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
            f'<head><title>{html.escape(title, quote=False)}</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            f'<body class="{cls}">{h}' + '\n'.join(body) + '\n</body></html>\n')


def numbered(folder):
    out = {}
    for p in glob.glob(os.path.join(folder, '[0-9][0-9][0-9][0-9][0-9]*.md')):
        out[int(os.path.basename(p)[:5])] = p
    return out


def main():
    ap = argparse.ArgumentParser(description='Build an EPUB from drafted chapters.')
    ap.add_argument('files', nargs='*', help='prose files in reading order (or use --prose with --from and --to)')
    ap.add_argument('--title', required=True, help='the book title')
    ap.add_argument('--author', default='Unknown', help='the author name (default: Unknown)')
    ap.add_argument('--series', help='series name, for series metadata')
    ap.add_argument('--index', type=int, default=1, help='the book number in the series (default: 1)')
    ap.add_argument('--front', action='append', default=[], help="front-matter file; only what follows its first '---' is used (repeatable, in order)")
    ap.add_argument('--rights', help='the rights line in the metadata')
    ap.add_argument('--cover', action='store_true', help='a plain typeset cover in place of the title page (needs Pillow)')
    ap.add_argument('--skip', default='', help='chapter numbers left out, comma-separated')
    ap.add_argument('--merged-mark', help='an outline-only slot whose outline holds this text gets no placeholder')
    ap.add_argument('--uid-seed', help='what the identifier is made from (default: the title)')
    ap.add_argument('--out', required=True, help='the EPUB file to write')
    ap.add_argument('--prose', help='folder of numbered prose files (00100-slug.md), taken by --from and --to')
    ap.add_argument('--outline', help='folder of numbered outlines; an outlined chapter with no prose gets a "[Not yet drafted.]" page')
    ap.add_argument('--from', dest='lo', type=int, help='first chapter number, e.g. 100')
    ap.add_argument('--to', dest='hi', type=int, help='last chapter number, e.g. 2000')
    ap.add_argument('--kepub', action='store_true', help=argparse.SUPPRESS)  # the default now; kept so old commands run
    ap.add_argument('--no-kepub', action='store_true', help='build the plain EPUB only, without the .kepub.epub')
    a = ap.parse_args()

    entries = []   # (id, href, title, xhtml)
    full_title = f'{a.series}, {a.title}' if a.series else a.title
    for k, f in enumerate(a.front):
        forced = None
        if '=' in f and not os.path.exists(f):
            forced, f = f.split('=', 1)
        t, b = front(f, full_title)
        t = forced or t
        name = 'front' if k == 0 else f'front{k + 1}'
        cls = 'front copyright' if t.strip().lower() == 'copyright' else 'front'   # a page titled Copyright is set small, to fit one screen
        entries.append((name, f'{name}.xhtml', t, page(t, b, cls)))
    skip = {int(x) for x in a.skip.split(',') if x.strip()}
    if a.files:
        for p in a.files:
            t, b = chapter(p)
            stem = re.sub(r'[^A-Za-z0-9_-]', '-', os.path.splitext(os.path.basename(p))[0])
            entries.append((f'c-{stem}', f'c-{stem}.xhtml', t, page(t, b)))
    elif a.prose and a.lo is not None and a.hi is not None:
        prose = numbered(a.prose)
        outline = numbered(a.outline) if a.outline else {}
        for n in sorted(k for k in set(prose) | set(outline) if a.lo <= k <= a.hi and k not in skip):
            if n in prose:
                t, b = chapter(prose[n])
                cls = 'fragment' if t.lower().startswith('fragment') else ''
            else:
                cls = 'fragment'
                text = open(outline[n], encoding='utf-8').read()
                if a.merged_mark and a.merged_mark in text:
                    continue
                t = re.sub(r'^#\s*', '', text.split('\n', 1)[0]).strip()
                t = re.sub(r'\s*\((fragment )?outline\)\s*$', '', t)
                if re.match(r'\d{5}-F\d', os.path.basename(outline[n])) and not t.lower().startswith('fragment'):
                    t = 'Fragment: ' + t
                b = ['<p class="placeholder">[Not yet drafted.]</p>']
            entries.append((f'c{n:05d}', f'c{n:05d}.xhtml', t, page(t, b, cls)))
    else:
        ap.error('give chapter files, or --prose with --from and --to')
    if not [e for e in entries if not e[0].startswith('front')]:
        sys.exit('no chapters found')

    titlepage = page(a.title, [f'<h1>{html.escape(a.title, quote=False)}</h1>',
                               f'<p class="byline">{html.escape(a.author, quote=False)}</p>'], heading=False)
    uid = f'urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, a.uid_seed or "story-kit/" + a.title)}'
    jpeg = cover(a.series, a.title, a.author) if a.cover else None
    if a.cover and jpeg is None:
        print('Pillow not found; built with a title page, no cover')
    rights = f'<dc:rights>{html.escape(a.rights, quote=False)}</dc:rights>\n' if a.rights else ''
    if jpeg:
        first_item = ('<item id="cover-image" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>\n'
                      '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
        first_ref, cover_meta = '<itemref idref="cover"/>', '<meta name="cover" content="cover-image"/>\n'
    else:
        first_item = '<item id="titlepage" href="title.xhtml" media-type="application/xhtml+xml"/>'
        first_ref, cover_meta = '<itemref idref="titlepage"/>', ''
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    series = ''
    if a.series:
        s = html.escape(a.series, quote=False)
        series = (f'<meta property="belongs-to-collection" id="series">{s}</meta>\n'
                  '<meta refines="#series" property="collection-type">series</meta>\n'
                  f'<meta refines="#series" property="group-position">{a.index}</meta>\n'
                  f'<meta name="calibre:series" content="{html.escape(a.series)}"/>\n'
                  f'<meta name="calibre:series_index" content="{a.index}"/>\n')
    manifest = '\n'.join(f'<item id="{i}" href="{h}" media-type="application/xhtml+xml"/>' for i, h, _, _ in entries)
    spine = '\n'.join(f'<itemref idref="{i}"/>' for i, _, _, _ in entries)
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{uid}</dc:identifier>
<dc:title>{html.escape(a.title, quote=False)}</dc:title>
<dc:creator>{html.escape(a.author, quote=False)}</dc:creator>
{rights}<dc:language>en</dc:language>
{series}{cover_meta}<meta property="dcterms:modified">{stamp}</meta>
</metadata>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
<item id="css" href="style.css" media-type="text/css"/>
{first_item}
{manifest}
</manifest>
<spine toc="ncx">
{first_ref}
{spine}
</spine>
</package>'''
    nav = page('Contents', ['<nav epub:type="toc"><ol>'] +
               [f'<li><a href="{h}">{html.escape(t, quote=False)}</a></li>' for _, h, t, _ in entries] +
               ['</ol></nav>'])
    ncx = ('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
           f'<head><meta name="dtb:uid" content="{uid}"/></head>'
           f'<docTitle><text>{html.escape(a.title, quote=False)}</text></docTitle><navMap>' +
           ''.join(f'<navPoint id="n{k}" playOrder="{k}"><navLabel><text>{html.escape(t, quote=False)}</text>'
                   f'</navLabel><content src="{h}"/></navPoint>' for k, (_, h, t, _) in enumerate(entries, 1)) +
           '</navMap></ncx>')
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    D = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(a.out, 'w') as z:
        z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml',
                   '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                   '</rootfiles></container>', compress_type=D)
        z.writestr('OEBPS/content.opf', opf, compress_type=D)
        z.writestr('OEBPS/nav.xhtml', nav, compress_type=D)
        z.writestr('OEBPS/toc.ncx', ncx, compress_type=D)
        z.writestr('OEBPS/style.css', CSS, compress_type=D)
        if jpeg:
            z.writestr('OEBPS/cover.jpg', jpeg, compress_type=zipfile.ZIP_STORED)
            z.writestr('OEBPS/cover.xhtml', '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
                       '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Cover</title>'
                       '<style>body{margin:0;padding:0;text-align:center}img{height:100%;max-width:100%}</style></head>'
                       f'<body><img src="cover.jpg" alt="{html.escape(a.title)}"/></body></html>\n', compress_type=D)
        else:
            z.writestr('OEBPS/title.xhtml', titlepage, compress_type=D)
        for _, href, _, text in entries:
            z.writestr('OEBPS/' + href, text, compress_type=D)
    words = sum(len(re.sub('<[^>]+>', ' ', e[3]).split()) for e in entries)
    print(f'{a.out}: {len(entries)} pages, about {words} words')
    if not a.no_kepub:
        if shutil.which('kepubify'):
            kepub = re.sub(r'\.epub$', '', a.out) + '.kepub.epub'
            if os.path.exists(kepub):
                os.remove(kepub)
            subprocess.run(['kepubify', '--output', kepub, a.out], check=True, stdout=subprocess.DEVNULL)
            print(kepub)
        else:
            print('kepubify not found; built the plain EPUB only')


if __name__ == '__main__':
    main()
