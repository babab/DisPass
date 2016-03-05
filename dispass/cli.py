# Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2016  Benjamin Althues <benjamin@althu.es>
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

from algos import algoObject
from dispass import versionStr

try:
    import curses
    hasCurses = True
except ImportError:
    hasCurses = False


class CLI:
    '''Command Line Interface handling'''

    verifyPassword = False
    '''Boolean. Prompt for password twice and save label to labelfile'''

    scriptableIO = False
    '''Boolean. Optimize input/output for wrapping dispass'''

    passphrases = {}
    '''Dict of labels and generated passphrases'''

    def __init__(self, filehandler):
        '''Set `useCurses` to True or False.

        Depending on the availability of curses

        '''
        self.filehandler = filehandler
        self.useCurses = hasCurses

    def setCurses(self, useCurses):
        '''Optionally override `self.useCurses`

        Instead of setting the instance variable `self.useCurses` directly, a
        setter is used to ensure it can only be set to `True` if the curses
        library is supported.

        :Parameters:
            - `useCurses`: Boolean

        '''
        if useCurses and not hasCurses:
            self.useCurses = False
        else:
            self.useCurses = useCurses

    def passwordPrompt(self):
        '''Prompt for password

        Use the `getpass.getpass` function to ask the user for the password
        and ensure it is 8 characters. The password will be asked twice if
        `self.verifyPassword` == `True`.

        :Return: Password string.

        '''
        while True:
            inp = getpass.getpass()

            if len(inp) < 8:
                print('Password must contain at least 8 characters.'
                      'Please try again.')
                continue

            if self.verifyPassword:
                inp2 = getpass.getpass("Password (again): ")
                if inp == inp2:
                    break
                else:
                    print('Passwords do not match. Please try again.')
            else:
                break

        return inp

    def generate(self, password, labeltup):
        '''Generate passphrase and store result in `passphrases`

        :Parameters:
            - `password`: Password to use for passphrase generation
            - `labeltup`: A tuple `labeltup` with 5 values:
               * `label`: Label to use for passphrase generation
               * `length`: Length to use for passphrase generation
               * `algo`: Algorithm to use for passphrase generation
               * `seqno`: Sequence number to use for passphrase generation
               * `disabled`: Whether or not the label is disabled

        '''
        label = labeltup[0]
        length = labeltup[1]
        algo = labeltup[2]
        seqno = labeltup[3]

        hasher = algoObject(algo)
        if hasher:
            self.passphrases.update({label: hasher.digest(
                label, password, length, seqno
            )})

    def output(self):
        '''Output and flush passphrase(s)'''
        if not self.passphrases:
            return False

        divlen = len(max(self.passphrases.keys(), key=len)) + 2

        if self.useCurses:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            stdscr.addstr(0, 0, versionStr + " - press 'q' to quit",
                          curses.A_BOLD)
            stdscr.addstr(1, 0, "Your passphrase(s)", curses.A_BOLD)

            j = 3
            for label, passphrase in self.passphrases.iteritems():
                stdscr.addstr(j,  0, label, curses.A_BOLD)
                stdscr.addstr(j, divlen, passphrase)
                j += 1
            stdscr.refresh()
            curses.curs_set(0)

            while True:
                c = stdscr.getch()
                if c == ord('q'):
                    stdscr.erase()
                    break

            curses.nocbreak()
            curses.echo()
            curses.endwin()
        else:
            for label, passphrase in self.passphrases.iteritems():
                if self.scriptableIO:
                    print('{:50} {}'.format(label[:50], passphrase))
                else:
                    print('{:{fill}} {}'
                          .format(label, passphrase, fill=divlen))
        self.passphrases = {}
        return True
