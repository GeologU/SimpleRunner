#!/usr/bin/env python3

import enum
from typing import Tuple, List

from with_html_stack import HTMLDocument

FILENAME = "gtype-instantiable-classed.html"


def line_and_sym(lines: List[str], pos: int) -> str:
    offset = 0
    for k, item in enumerate(lines, 1):
        new_offset = offset + len(item)
        if pos < new_offset:
            return f'line {k}, symbol {pos - offset + 1}'
        offset = new_offset
    raise RuntimeError('position is outside lines')


def find_bracket(content: str, offset: int) -> Tuple[int, str]:  # index, bracket
    for k in range(offset, len(content)):
        if content[k] in {'<', '>'}:
            return k, content[k]
    raise StopIteration


def load(content: str) -> Tuple[HTMLDocument, List[str]]:
    doc = HTMLDocument(doctype=False)
    lines = content.splitlines(keepends=True)
    offset = 0
    errors = []

    while True:
        try:
            pos, bracket = find_bracket(content, offset)
        except StopIteration:
            if offset < len(content):
                doc.raw(content[offset:])
            break

        if bracket == '>':
            errors.append(f"unpared '>' at {line_and_sym(lines, pos)}")
            doc.raw(content[offset:pos + 1])
            offset = pos + 1
            continue

        if offset != pos:
            doc.raw(content[offset:pos])
        offset = pos + 1

        try:
            pos2, bracket2 = find_bracket(content, offset)
        except StopIteration:
            errors.append(f"unpared '<' at {line_and_sym(lines, pos)}")
            doc.raw(content[offset - 1:])
            break

        if bracket2 == '<':
            errors.append(f"unexpected '<' at {line_and_sym(lines, pos2)}")
            doc.raw(content[offset:pos2])
            offset = pos2
            continue

        tag_data = content[offset:pos2]
        offset = pos2 + 1

        if tag_data.startswith('/'):
            chunks = tag_data[1:].split(maxsplit=1)
            if not chunks:
                errors.append(f"tag without name at {line_and_sym(lines, pos)}")
                continue
            if len(chunks) > 1:
                errors.append(f"closing tag has attributes at {line_and_sym(lines, pos)}")

            tag_name = chunks[0]
        #if tag_data.endswith('/'):

    return doc, errors


def main():
    with open(FILENAME) as fin:
        #print(load(fin.read(), 0).as_code())
        doc, errors = load(fin.read())
        for item in errors:
            print('error:', item)


if __name__ == '__main__':
    main()
