# Inspired from: https://github.com/gravmatt/py-term/blob/master/term.py
# Original source from: https://github.com/gravmatt/py-term
# That a frozen implementation of the py-term module with only functions needed by glxviewer.

import sys

OFF = '\033[0m\033[27m'
BOLD = '\033[1m'
DIM = '\033[2m'

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

BG_WHITE = '\033[47m'


def send(cmd):
    sys.stdout.write(cmd)
    sys.stdout.flush()


def pos(line, column):
    send('\033[%s;%sf' % (line, column))


def writeString(*style, text=''):
    send(format(text, *style))


def writeLine(*style, text=''):
    writeString(*style, text=str(text) + '\n')


def clearLineFromPos():
    send('\033[K')
