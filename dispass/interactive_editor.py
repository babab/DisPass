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

import sys

import algos


class InteractiveEditor:
    '''User interface for altering labelfiles'''

    filehandler = None
    '''Filehandler object'''

    def __init__(self, settings, filehandler, interactive=False):
        self.settings = settings
        self.filehandler = filehandler

        if interactive:
            print('Using {loc} as labelfile\n'
                  .format(loc=self.filehandler.file_location))
            self.menu()

    def menu(self):
        print('add     Add label\n'
              'remove  Remove label\n'
              'ls      List all labels\n'
              'help    Show this help information\n'
              'quit    Quit')
        self.prompt()

    def prompt(self):
        try:
            inp = raw_input('\n> ').split()
            if not inp:
                print('No menu option given')
                self.prompt()

            command = inp[0].lower()
            command_char = command[0].lower()

            if command_char == 'l':
                self.filehandler.printLabels()
                self.prompt()
            elif command_char == 'a':
                self.add()
                self.prompt()
            elif command_char == 'r':
                self.remove()
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
        except KeyboardInterrupt:
            self.prompt()

    def read_label(self):
        '''Keep bugging the user for a label until they crack and give us
        one.

        '''
        while True:
            try:
                return raw_input('Label: ').split()[0]
            except IndexError:
                print('label cannot be empty - please try again')
                continue

    def add(self):
        label = self.read_label()

        while True:
            try:
                length = (
                    raw_input('Length [press enter for default "{len}"]: '
                              .format(len=self.settings.passphrase_length))
                    .split()[0])
            except IndexError:
                length = self.settings.passphrase_length
                break

            try:
                length = int(length)
            except ValueError:
                print('length must be a number in range 9 -> 171')
                continue

            if length < 9 or length > 171:
                print('length must be a number in range 9 -> 171')
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
                    if algoname == self.settings.algorithm:
                        choices += ' [default]'
                    print(choices)
                    i += 1
                choice = (raw_input('Algorithm [press enter for default]: ')
                          .split()[0])
            except IndexError:
                algo = self.settings.algorithm
                break

            if not algo:
                try:
                    choice = int(choice)
                except ValueError:
                    print('Invalid choice')
                    continue

                if choice < 1:
                    print('Invalid choice')
                    continue

                try:
                    algo = algos.algorithms[choice - 1]
                except IndexError:
                    print('Invalid choice')
                    continue
            print(algo)
            break

        if algo != 'dispass1':
            default_seqno = self.settings.sequence_number
            while True:
                try:
                    seqno = (
                        raw_input(
                            'Sequence number [press enter for default'
                            ' "{seqno}"]: '.format(seqno=default_seqno))
                        .split()[0])
                except IndexError:
                    seqno = self.settings.sequence_number
                    break

                try:
                    seqno = int(seqno)
                except ValueError:
                    print('Sequence number must be a number > 1')
                    continue

                if seqno < 1:
                    print('Sequence number must be a number > 1')
                    continue
                else:
                    break
        else:
            seqno = self.settings.sequence_number

        if self.filehandler.add(labelname=label, length=length,
                                algo=algo, seqno=seqno):
            self.filehandler.save()
            print('Label saved')
            self.filehandler.parse()
            return label
        else:
            print('Label already exists in labelfile')
            return False

    def remove(self):
        label = self.read_label()

        if self.filehandler.remove(label):
            self.filehandler.save()
            print('Label removed')
        else:
            print("Label doesn't exist in labelfile")
