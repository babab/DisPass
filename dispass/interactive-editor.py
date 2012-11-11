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

import sys

import algos
from labelfile import FileHandler


class InteractiveEditor:

    filehandler = None
    '''FileHandler object, set on init if labelfile is found'''

    def __init__(self, file_location=None):
        if file_location:
            self.filehandler = FileHandler(file_location=file_location)
        else:
            self.filehandler = FileHandler()
        print('Using {loc} as labelfile\n'
              .format(loc=self.filehandler.file_location))

    def menu(self):
        print('a[ad]             Add label\n'
              'l[s]              List all labels\n'
              'h[elp]            Show this help information\n'
              'q[uit]            Quit')
        self.prompt()

    def prompt(self):
        inp = raw_input('\n> ').split()
        if not inp:
            print 'No menu option given'
            self.prompt()

        command = inp[0].lower()
        command_char = command[0].lower()

        if command_char == 'l':
            self.filehandler.printLabels()
            self.prompt()
        elif command_char == 'a':
            self.add()
            self.prompt()
        elif command_char == 'q':
            print('Bye')
            sys.exit()
        elif command_char == 'h':
            self.menu()
            self.prompt()
        else:
            print("Invalid option '{command}'".format(command=command))
            self.menu()

    def add(self):
        while True:
            try:
                label = raw_input('Label: ').split()[0]
                break
            except IndexError:
                print 'label cannot be empty - please try again'
                continue

        while True:
            try:
                length = (
                    raw_input('Length [press enter for default "{len}"]: '
                              .format(len=self.filehandler.default_length))
                    .split()[0])
            except IndexError:
                length = self.filehandler.default_length
                break

            try:
                length = int(length)
            except ValueError:
                print 'length must be a number in range 9 -> 171'
                continue

            if length < 9 or length > 171:
                print 'length must be a number in range 9 -> 171'
                continue
            else:
                break

        algo = None
        while True:
            try:
                i = 1
                for algoname in algos.algorithms:
                    choices = ('[{num}] {algoname}'
                               .format(num=i, algoname=algoname))
                    if algoname == self.filehandler.algorithm:
                        choices += ' [default]'
                    print choices
                    i += 1
                choice = (raw_input('Algorithm [press enter for default]: ')
                          .split()[0])
            except IndexError:
                algo = self.filehandler.algorithm
                break

            if not algo:
                try:
                    choice = int(choice)
                except ValueError:
                    print 'Invalid choice'
                    continue

                if choice < 1:
                    print 'Invalid choice'
                    continue

                try:
                    algo = algos.algorithms[choice - 1]
                except IndexError:
                    print 'Invalid choice'
                    continue
            print algo
            break

        if algo != 'dispass1':
            default_seqno = self.filehandler.default_sequence_number
            while True:
                try:
                    seqno = (
                        raw_input(
                            'Sequence number [press enter for default'
                            ' "{seqno}"]: '.format(seqno=default_seqno))
                        .split()[0])
                except IndexError:
                    seqno = self.filehandler.default_sequence_number
                    break

                try:
                    seqno = int(seqno)
                except ValueError:
                    print 'Sequence number must be a number > 1'
                    continue

                if seqno < 1:
                    print 'Sequence number must be a number > 1'
                    continue
                else:
                    break
        else:
            seqno = self.filehandler.default_sequence_number

        if self.filehandler.add(labelname=label, length=length,
                                algo=algo, seqno=seqno):
            self.filehandler.save()
            print 'Label saved '
        else:
            print 'Label already exists in labelfile'

if __name__ == '__main__':
    ie = InteractiveEditor()
    ie.menu()
