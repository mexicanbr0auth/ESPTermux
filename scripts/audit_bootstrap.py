#!/usr/bin/env python3
"""Inventory hardcoded upstream prefixes in bundled Termux bootstraps.

This is an audit, not a claim that rewriting binary strings makes packages relocatable.
"""
import argparse
import collections
import pathlib
import sys
import zipfile

OLD = b'/data/data/com.termux/files/usr'
NEW = b'/data/data/dev.mexicanbr.esptermux/files/usr'

def audit(path):
    kinds = collections.Counter()
    examples = collections.defaultdict(list)
    with zipfile.ZipFile(path) as archive:
        for item in archive.infolist():
            if item.is_dir():
                continue
            data = archive.read(item)
            if OLD not in data:
                continue
            if data.startswith(b'\x7fELF'):
                kind = 'ELF binaries (require rebuild)'
            elif data.startswith(b'#!'):
                kind = 'scripts (interpreter or body)'
            elif item.filename == 'SYMLINKS.txt':
                kind = 'symlink manifest'
            elif b'\x00' in data[:4096]:
                kind = 'other binary data'
            else:
                kind = 'other text/configuration'
            kinds[kind] += 1
            if len(examples[kind]) < 12:
                examples[kind].append(item.filename)
    print(f'Bootstrap: {path}')
    print(f'Original prefix: {OLD.decode()}')
    print(f'Fork prefix: {NEW.decode()}')
    print('This audit does not alter the bootstrap.')
    for kind, count in kinds.most_common():
        print(f'\n{kind}: {count}')
        for example in examples[kind]:
            print(f'  {example}')
    if not kinds:
        print('No literal original-prefix matches found (does not prove relocatability).')
    return kinds

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('archives', nargs='+', type=pathlib.Path)
    parser.add_argument('--require-relocatable', action='store_true', help='Fail if any original prefix is embedded')
    args = parser.parse_args()
    has_old_prefix = False
    for archive in args.archives:
        counts = audit(archive)
        has_old_prefix = has_old_prefix or bool(counts)
    if args.require_relocatable and has_old_prefix:
        print("ERROR: Upstream prefix remains in bootstrap; do not publish as working ESPTermux.", file=sys.stderr)
        sys.exit(1)
