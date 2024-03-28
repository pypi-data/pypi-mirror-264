#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Standard python module
import argparse
import sys

from glxviewer.viewer import Viewer

parser_glxviewer = argparse.ArgumentParser(
    prog="glx-viewer",
    add_help=True,
)
parser_glxviewer.add_argument(
    "--status-text",
    nargs="?",
    help="The text to display ton the status part",
)
parser_glxviewer.add_argument(
    "--status-text-color",
    nargs="?",
    help="Allowed : BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE",
)
parser_glxviewer.add_argument(
    "--status-symbol",
    default=" ",
    nargs="?",
    help="A symbol of one letter. like ! > < / - | generally for show you application fo something.",
)
parser_glxviewer.add_argument(
    "--with-no-date",
    dest="with_no_date",
    action='store_true',
    default=False,
    help="Do not display the date on the output line",
)
parser_glxviewer.add_argument(
    "--column-1",
    nargs="?",
    default='',
    help="The thing to print in column 1",
)
parser_glxviewer.add_argument(
    "--column-2",
    nargs="?",
    default='',
    help="The thing to print in column 2",
)
parser_glxviewer.add_argument(
    "--column-3",
    nargs="?",
    default='',
    help="The thing to print in column 3",
)
parser_glxviewer.add_argument(
    "--with-no-prompt",
    action='store_true',
    default=False,
    help="Do not display the date on the output line",
)


def main():
    args = parser_glxviewer.parse_args(sys.argv[1:])
    with_date = isinstance(args.with_no_date, bool) and not args.with_no_date
    prompt = isinstance(args.with_no_prompt, bool) and args.with_no_prompt

    Viewer().write(
        with_date=with_date,
        status_text=args.status_text,
        status_text_color=args.status_text_color,
        status_symbol=args.status_symbol,
        column_1=args.column_1,
        column_2=args.column_2,
        column_3=args.column_3,
        prompt=prompt,
    )


if __name__ == "__main__":
    sys.exit(main())
