'''Dispass labelfile handler'''

# Copyright (c) 2011, 2012, 2013  Benjamin Althues <benjamin@babab.nl>
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

import datetime
import os
from os.path import expanduser, exists

from dispass import __version__


class Filehandler:
    '''Parsing of labelfiles and writing to labelfiles'''

    filehandle = None
    '''File object, set on init if labelfile is found'''

    file_found = None
    '''Boolean value set on init'''

    file_location = None
    '''String of labelfile location, set on init'''

    labelfile = []
    '''List of [(labelname, length, algorithm, seqno), ... ]'''

    longest_label = None
    '''Int. Length of the longest labelname of `labelfile`. Set on refresh()'''

    def __init__(self, settings, file_location=None):
        '''Open file; if file is found: strip comments and parse()'''

        self.settings = settings

        if file_location:
            self.file_location = expanduser(file_location)
        else:
            self.file_location = expanduser(self.getDefaultFileLocation())

        self.parse()

    def getDefaultFileLocation(self):
        """Scan default labelfile paths"""

        label_env = os.getenv('DISPASS_LABELFILE')
        std_env = os.getenv('XDG_DATA_HOME') or os.getenv('APPDATA')
        home_file = '~/.dispass/labels'

        if label_env:
            return label_env
        if not exists(home_file) and std_env:
            return std_env + '/dispass/labels'
        else:
            return home_file

    def parse(self):
        '''Create dictionary {algorithm: (label, (length, seqno))}'''

        file_stripped = []
        self.labelfile = []

        try:
            self.filehandle = open(self.file_location, 'r')
            self.file_found = True
        except IOError:
            self.file_found = False
            return

        # Strip comments and blank lines
        for i in self.filehandle:
            if i[0] != '\n' and i[0] != '#':
                file_stripped.append(i)

        if self.file_found:
            self.filehandle.close()
        else:
            return

        labels = []

        for i in file_stripped:
            wordlist = []
            line = i.rsplit(' ')
            for word in line:
                if word != '':
                    wordlist.append(word.strip('\n'))
            labels.append(wordlist)

        for line in labels:
            labelname = line.pop(0)
            length = self.settings.passphrase_length
            seqno = self.settings.sequence_number
            algo = self.settings.algorithm

            for arg in line:
                if 'length=' in arg:
                    try:
                        length = int(arg.strip('length='))
                    except ValueError:
                        print "Warning: Invalid length in: '%s'" % line
                elif 'algo=' in arg:
                    algo = arg.strip('algo=')
                elif 'seqno=' in arg:
                    seqno = arg.strip('seqno=')

            self.labelfile.append((labelname, length, algo, seqno))

        return self

    def add(self, labelname, length=None, algo=None, seqno=None):
        '''Add label to `labelfile`'''

        length = length if length else self.settings.passphrase_length
        algo = algo if algo else self.settings.algorithm
        seqno = seqno if seqno else self.settings.sequence_number

        for label in self.labelfile:
            if labelname == label[0]:
                return False

        self.labelfile.append((labelname, length, algo, seqno))
        return True

    def remove(self, labelname):
        '''Remove label from `labelfile`'''

        removed = False

        for i in range(len(self.labelfile)):
            if self.labelfile[i][0] == labelname:
                del self.labelfile[i]
                removed = True
                break

        return removed

    def refresh(self, sort=True):
        '''Sort `labelfile` on labelname and get longest label'''

        if sort:
            self.labelfile.sort()
        labelnames = []
        for label in self.labelfile:
            labelnames.append(label[0])
        if labelnames:
            self.longest_label = len(max(labelnames, key=len))

    def save(self):
        '''Save `labelfile` to file'''

        self.refresh()
        labelfile = ('# Generated by DisPass {version} on {datetime}\n\n'
                     .format(version=__version__,
                             datetime=datetime.datetime.now()))
        for label in self.labelfile:
            options = ''
            if label[1] != self.settings.passphrase_length:
                options += 'length={length}  '.format(length=label[1])
            if label[2] != self.settings.algorithm:
                options += 'algo={algo}  '.format(algo=label[2])
            if label[3] != self.settings.sequence_number:
                options += 'seqno={seqno}  '.format(seqno=label[3])

            labelfile += ('{label:{divlen}}  {options}\n'
                          .format(label=label[0], options=options,
                                  divlen=len(self.longest_label)))
        try:
            self.filehandle = open(self.file_location, 'w')
            self.filehandle.write(labelfile)
            self.filehandle.close()
        except IOError:
            return False

        return True

    def labeltup(self, label):
        '''Get labeltup for `label`

        :Parameters:
            - `label`: The labelname

        :Returns:
            A tuple `labeltup` with 4 values ``(label, length, algo, seqno))``:

            - `label`: Label to use for passprase generation
            - `length`: Length to use for passprase generation
            - `algo`: Algorithm to use for passprase generation
            - `seqno`: Sequence number to use for passprase generation

        '''

        for labeltup in self.labelfile:
            if label == labeltup[0]:
                return labeltup
        return False

    def printLabels(self, fixed_columns=False):
        '''Print a formatted table of labelfile contents

        :Parameters:
            - `fixed_columns`: Boolean.

        If fixed columns is true the output will be optimized for easy
        parsing by other programs and scripts by not printing the header
        and always printing one entry on a single line using the
        following positions:

        * Column 1-50: label (50 chars)
        * Column 52-54: length (3 chars wide)
        * Column 56-70: hash algo (15 chars wide)
        * Column 72-74: sequence number (3 chars wide)

        If fixed columns is false an ascii table is printed with a variable
        width depending on the length of the longest label.
        '''

        self.refresh()
        if fixed_columns:
            for label in self.labelfile:
                print('{:50} {:3} {:15} {:3}'
                      .format(label[0][:50], str(label[1])[:3],
                              label[2][:15], str(label[3])))
        else:
            divlen = self.longest_label
            if not divlen:
                return
            print('+-{spacer:{fill}}-+--------+----------+--------+\n'
                  '| {title:{fill}} | Length | Algo     | Number | \n'
                  '+-{spacer:{fill}}-+--------+----------+--------+'
                  .format(spacer='-' * divlen, title='Label', fill=divlen))

            for label in self.labelfile:
                print('| {:{fill}} |    {:3} | {:8} |      {:3>} |'
                      .format(label[0], label[1], label[2], int(label[3]),
                              fill=divlen))
            print('+-{:{fill}}-+--------+----------+--------+'
                  .format('-' * divlen, fill=divlen))

    def promptForCreation(self, silent=False):
        if silent:
            if self.save():
                return True
            else:
                return False

        print('error: could not load labelfile at "{loc}"'
              .format(loc=self.file_location))
        inp = raw_input('Do you want to create it? Y/n ')

        if inp == '' or inp[0].lower() == 'y':
            if not self.save():
                print('error: could not save to "{loc}"\n'
                      .format(loc=self.file_location))
                return False
        else:
            return False
        return True
