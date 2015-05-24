#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, print_function

import argparse
import os
import sys
import re
import logging

DEFAULT_INCLUDE_PATH = ['.']
PRAGMA_INCLUDE_RE = re.compile(r'INCLUDE\s+"([^"\']*)"')

logging.basicConfig(format="%(asctime)-15s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser('C-style pre-processing include for F2J')

    parser.add_argument('target', metavar='file', type=str, nargs='?',
                        help='The target .sf file')
    parser.add_argument('--include', '-s', type=str, nargs='+', default=[],
                        help='Add folder into the search path')
    parser.add_argument('--output', '-o', type=str, nargs=1,
                        help='Output file')

    args = parser.parse_args()

    additional_include_path = args.include + os.environ.get('F2J_INCLUDE_PATH', [])

    return {
        'target': args.target,
        'output': args.output,
        'additional_include_path': additional_include_path,
    }


def process_file(f, search_path, visited_files):
    logger.debug('Processing %s' % f.name)
    lines = []

    line = f.readline()
    while line != '':
        trimed = line.strip()

        if trimed.startswith('{-#'):
            pragma = []
            while not line.strip().endswith('#-}'):
                if line == '':
                    break
                pragma.append(line)
                line = f.readline()
            else:
                pragma.append(line)

            pragmas = ''.join(pragma)
            includes = PRAGMA_INCLUDE_RE.findall(pragmas)
            pragma = []

            current_visited = []

            for inc in includes:
                logger.debug('Found include %s in %s' % (inc, f.name))
                for sp in search_path:
                    full = os.path.join(sp, inc)
                    logger.debug('Trying %s' % full)
                    if not os.path.exists(full):
                        continue

                    if full in visited_files:
                        logger.debug('Already included %s' % inc)
                        break
                    else:
                        visited_files.add(full)

                    includef = open(full, 'r')

                    procceed, _ = process_file(includef, search_path, visited_files)

                    if not procceed.rstrip().endswith(';'):
                        raise RuntimeError('Included file should not have the last expression, %s', includef.name)

                    current_visited.append(procceed)
                    break
                else:
                    raise RuntimeError('Unable to include %s, %s' % (inc, repr(inc)))

            lines += current_visited
        else:
            if not trimed.startswith('--'):
                lines.append(line)
        line = f.readline()

    return ''.join(lines), visited_files


def main():
    args = parse_arguments()

    include_path = args['additional_include_path'] + DEFAULT_INCLUDE_PATH
    include_path = [os.path.abspath(p) for p in include_path]
    target = open(args['target'], 'r') if args['target'] is not None else sys.stdin
    output = open(args['output'][0], 'w+') if args['output'] is not None else sys.stdout

    visited_files = {os.path.abspath(args['target'])} if args['target'] is not None else set()

    if args['output'] is None:
        logger.setLevel(logging.NOTSET)

    logger.info('Target: %s' % target.name)
    logger.info('Include Path: %s' % include_path)
    logger.info('Output: %s' % output.name)

    processed, _ = process_file(target, include_path, visited_files)
    output.write(processed)


if __name__ == '__main__':
    main()
