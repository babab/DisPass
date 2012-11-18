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
import algos

from dispass import versionStr
from filehandler import Filehandler

try:
    import curses
    hasCurses = True
except ImportError:
    hasCurses = False


class CLI:
    '''Command Line Interface handling'''

    createLabel = False
    '''Boolean. Prompt for password twice and save label to labelfile'''

    scriptableIO = None
    '''Boolean. Optimize input/output for wrapping dispass'''

    passphrases = []
    '''List of 2-tuples of labels and generated passphrases'''

    def __init__(self, settings):
        '''Set `useCurses` to True or False.

        Depending on the availability of curses
        '''
        self.algorithm = settings.algorithm
        self.passphraseLength = settings.passphrase_length
        self.seqno = settings.sequence_number
        self.settings = settings
        self.useCurses = hasCurses

    def setAlgo(self, algo):
        '''Optionally override the algorithm to use for generating passphrases

        :Parameters:
            - `algo`: String. Name of the algorithm
        '''

        self.algorithm = algo

    def setSeqNo(self, seqno):
        '''Optionally override the sequence number to use

        :Parameters:
            - `algo`: String. Name of the algorithm
        '''

        self.seqno = seqno

    def setCurses(self, useCurses):
        '''Optionally override `self.useCurses`

        :Parameters:
            - `useCurses`: Boolean
        '''

        if useCurses and not hasCurses:
            self.useCurses = False
        else:
            self.useCurses = useCurses

    def setScriptableIO(self, scriptableIO=True):
        '''Optimize input/output for wrapping dispass in a script or program

        :Parameters:
            - `sriptableIO`: Boolean
        '''

        self.scriptableIO = scriptableIO

    def setLength(self, length):
        '''Optionally override length of output passphrase

        :Parameters:
            - `length`: Integer. Length of output passphrase
        '''

        self.passphraseLength = length

    def passwordPrompt(self):
        '''Prompt for password.

        :Return: Password string.
        '''

        while True:
            inp = getpass.getpass()

            if len(inp) < 8:
                print 'Password must contain at least 8 characters.',
                print 'Please try again.'
                continue

            if self.createLabel:
                inp2 = getpass.getpass("Password (again): ")
                if inp == inp2:
                    break
                else:
                    print "Passwords do not match. Please try again."
            else:
                break

        return inp

    def interactive(self, labels, filehandler):
        '''Start interactive prompt, generating and showing the passprase(s)

        :Parameters:
            - `labels`: List or dict of labels to use for passprase generation
        '''

        password = self.passwordPrompt()
        algo_dispass1 = algos.Dispass1()
        algo_dispass2 = algos.Dispass2()
        fh = filehandler
        added = False
        saved = False

        if isinstance(labels, list):
            labelmap = []
            for i in labels:
                labelmap.append((i, (self.passphraseLength, self.algorithm)))
                if (self.createLabel and
                    fh.add(labelname=i, length=self.passphraseLength,
                           algo=self.algorithm, seqno=self.seqno)):
                    added = True
            if added and fh.save():
                saved = True

            if self.algorithm == 'dispass1':
                self.passphrases = algo_dispass1.digestPasswordDict(
                    dict(labelmap), password
                )
            elif self.algorithm == 'dispass2':
                self.passphrases = algo_dispass2.digestPasswordDict(
                    dict(labelmap), password
                )

            divlen = len(max(labels, key=len)) + 2
            self.passphrases = dict(self.passphrases)

        elif isinstance(labels, dict):
            for algo, labels in labels.iteritems():
                if algo == 'dispass1':
                    self.passphrases += algo_dispass1.digestPasswordDict(
                        labels, password
                    )
                elif algo == 'dispass2':
                    self.passphrases += algo_dispass2.digestPasswordDict(
                        labels, password
                    )

            label_list = []
            self.passphrases = dict(self.passphrases)
            for label, length in self.passphrases.iteritems():
                label_list.append(label)
            if label_list:
                divlen = len(max(label_list, key=len)) + 2
            else:
                print('Nothing to generate, you need to add some labels')
                return

        del password

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
                    print '{:50} {}'.format(label[:50], passphrase)
                else:
                    print "{:{fill}} {}".format(label, passphrase, fill=divlen)
        self.passphrases = {}

        if saved:
            print('Succesfully added label(s) to {loc}'
                  .format(loc=fh.file_location))
        if self.createLabel and not saved:
            print('error: could not save to "{loc}"\n'
                  .format(loc=fh.file_location))
