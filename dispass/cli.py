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
    '''Command Line Interface handling'''

    passphraseLength = 30
    '''Length of output passphrase, default is 30'''

    promptDouble = False
    '''Boolean. Prompt for password twice'''

    def __init__(self):
        '''Set `useCurses` to True or False.

        Depending on the availability of curses
        '''

        self.useCurses = hasCurses

    def setCurses(self, useCurses):
        '''Optionally override `self.useCurses`

        :Parameters:
            - `useCurses`: Boolean
        '''

        if useCurses and not hasCurses:
            self.useCurses = False
        else:
            self.useCurses = useCurses

    def setLength(self, length):
        '''Optionally override length of output passphrase

        :Parameters:
            - `length`: Integer. Length of output passphrase
        '''

        self.passphraseLength = length

    def setPrompt(self, promptDouble=False):
        '''Set options for the passwordPrompt)

        :Parameters:
            - `promptDouble`: Boolean. Prompt 2x and compare passwords
        '''
        self.promptDouble = promptDouble

    def passwordPrompt(self):
        '''Prompt for password. Returns password'''

        while True:
            inp = getpass.getpass()
            if self.promptDouble:
                inp2 = getpass.getpass("Again:")
                if inp == inp2:
                    break;
                else:
                    print "Passwords do not match. Please try again."
            else:
                break

        return inp

    def interactive(self, labels):
        '''Start interactive prompt, generating and showing the passprase(s)

        :Parameters:
            - `labels`: List or dict of labels to use for passprase generation
        '''

        password = self.passwordPrompt()

        if isinstance(labels, list):
            labelmap = []
            for i in labels:
                labelmap.append((i, self.passphraseLength))

            hashedLabels = digest.digestPasswordDict(dict(labelmap), password)
            divlen = len(max(labels, key=len)) + 2
        elif isinstance(labels, dict):
            hashedLabels = digest.digestPasswordDict(labels, password)
            label_list = []
            for label, length in hashedLabels.iteritems():
                label_list.append(label)
            divlen = len(max(label_list, key=len)) + 2

        del password

        if self.useCurses:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            stdscr.addstr(0, 0, versionStr + " - press 'q' to quit",
                    curses.A_BOLD)
            stdscr.addstr(1, 0, "Your passphrase(s)", curses.A_BOLD)

            j = 3
            for label, passphrase in hashedLabels.iteritems():
                stdscr.addstr(j,  0, label, curses.A_BOLD)
                stdscr.addstr(j, divlen, passphrase, curses.A_REVERSE)
                j += 1
            stdscr.refresh()

            while True:
                c = stdscr.getch()
                if c == ord('q'):
                    break

            curses.nocbreak()
            curses.echo()
            curses.endwin()
        else:
            for label, passphrase in hashedLabels.iteritems():
                print "{:{fill}} {}".format(label, passphrase, fill=divlen)
