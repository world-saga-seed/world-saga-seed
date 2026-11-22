#!/usr/bin/env python3
"""Refuse a commit that stages a recording, anything under tmp/, or a very large file.

A book's history is hard to clean once a private file is in it: a recording of
the writer's voice, a raw transcript in tmp/, a 40 MB scan. .gitignore keeps
most of them out; this catches the one staged by hand or by a careless
"git add -A". Run it as the pre-commit hook (setup installs it):

  printf '#!/bin/sh\\nexec python3 tools/check_commit.py\\n' > .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit

Usage:
  python3 tools/check_commit.py [PATH ...] [--max-mb N]

  PATH        the files to check (default: the names staged in git, added or changed)
  --max-mb N  refuse a file larger than N megabytes (default 10)

Prints one line per refused file and a count, and exits 1 if any was refused.
"""
import argparse, os, re, subprocess, sys

AUDIO = {'.m4a', '.mp3', '.wav', '.ogg', '.flac', '.opus', '.aac', '.wma', '.aiff', '.amr'}


def staged():
    p = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z'],
                       capture_output=True, text=True)
    if p.returncode:
        sys.exit('check_commit.py: not in a git repository; name the files instead')
    return [n for n in p.stdout.split('\0') if n]


def why(name, max_mb):
    n = name.replace('\\', '/')
    if n == 'tmp' or n.startswith('tmp/'):
        return 'under tmp/, which is never committed'
    if n.endswith(':Zone.Identifier'):
        return 'a Windows download marker (Zone.Identifier); delete it'
    ext = os.path.splitext(n)[1].lower()
    if ext in AUDIO:
        return f'a recording ({ext}); keep it in tmp/ or outside the repository'
    if os.path.isfile(name):
        mb = os.path.getsize(name) / 1e6
        if mb > max_mb:
            return f'{mb:.1f} MB, over {max_mb:g} MB; keep large sources out of git with a SOURCE.md and checksums'
    return None


def main():
    ap = argparse.ArgumentParser(description='Refuse recordings, tmp/ and very large files in a commit.')
    ap.add_argument('paths', nargs='*', help='files to check (default: the staged names)')
    ap.add_argument('--max-mb', type=float, default=10, help='largest file allowed, in MB (default 10)')
    a = ap.parse_args()
    names = a.paths or staged()
    bad = [(n, w) for n in names for w in [why(n, a.max_mb)] if w]
    for n, w in bad:
        print(f'{n}: {w}')
    print(f'{len(bad)} files refused')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
