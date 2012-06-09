# Copyright (c) 2011-2012 Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import getpass

import digest
from dispass import versionStr

try:
    import curses
    hasCurses = True
except ImportError:
    hasCurses = False

class CLI:
    def __init__(self):
        self.useCurses = hasCurses

    def setCurses(self, useCurses):
        if useCurses and not hasCurses:
            self.useCurses = False
        else:
            self.useCurses = useCurses

    def interactive(self, labels, pwTypoCheck=False):
        while True:
            inp = getpass.getpass()
            if pwTypoCheck:
                inp2 = getpass.getpass("Again:")
                if inp == inp2:
                    break;
                else:
                    print "Passwords do not match. Please try again."
            else:
                break

        if self.useCurses:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            stdscr.addstr(0, 0, versionStr + " - press 'q' to quit",
                    curses.A_BOLD)
            stdscr.addstr(1, 0, "Your passphrase(s)", curses.A_BOLD)
            divlen = len(max(labels, key=len)) + 2
            j = 3
            for i in labels:
                stdscr.addstr(j,  0, i, curses.A_BOLD)
                stdscr.addstr(j, divlen, digest.digest(i + inp),
                        curses.A_REVERSE)
                j += 1
            del inp
            stdscr.refresh()

            while True:
                c = stdscr.getch()
                if c == ord('q'):
                    break

            curses.nocbreak()
            curses.echo()
            curses.endwin()
        else:
            for i in labels:
                print "%25s %s" % (i, digest.digest(i + inp))
