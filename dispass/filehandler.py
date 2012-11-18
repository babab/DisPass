'''Dispass labelfile handler'''

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

    algodict = {}
    '''Dictionary of {algorithm: (labelname, (length, seqno))}'''

    labelfile = []
    '''List of [(labelname, length, algorithm, seqno), ... ]'''

    longest_labelname = None
    '''String. The longest labelname of `labelfile`. Set on refresh()'''

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
        labels_dispass1 = []
        labels_dispass2 = []

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

            if algo == 'dispass1':
                labels_dispass1.append((labelname, (length, None)))
            elif algo == 'dispass2':
                labels_dispass2.append((labelname, (length, seqno)))

            self.labelfile.append((labelname, length, algo, seqno))

        self.algodict = {'dispass1': dict(labels_dispass1),
                         'dispass2': dict(labels_dispass2)}
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

    def refresh(self, sort=True):
        '''Sort `labelfile` on labelname and get longest label'''

        if sort:
            self.labelfile.sort()
        labelnames = []
        for label in self.labelfile:
            labelnames.append(label[0])
        if labelnames:
            self.longest_labelname = max(labelnames, key=len)

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
                                  divlen=len(self.longest_labelname)))
        try:
            self.filehandle = open(self.file_location, 'w')
            self.filehandle.write(labelfile)
            self.filehandle.close()
        except IOError:
            return False

        return True

    def search(self, search_string):
        '''Search for substring in labelfile

        :Parameters:
            - `search_string`: String to search for

        :Returns: Boolean False, Integer or Dict

        Searches all labels to find ``search_string`` as a substring of each
        label.

        If no matches are found, return False.
        If multiple matches are found, return Integer of number of matches
        If a unique match is found a dict of
        ``{algo: {label, (passphrase_length, sequence_number)}}`` is returned.
        '''
        count = 0
        found = []
        found_algo = None
        length = None
        seqno = None

        for algo, labels in self.algodict.iteritems():
            for label, params in labels.iteritems():
                if search_string in label:
                    found_algo = algo
                    length = params[0]
                    seqno = params[1]
                    found.append(label)
                    count += 1

        if not found:
            return False

        if count > 1:
            return count

        return {found_algo: {found.pop(): (length, seqno)}}

    def getLongestLabel(self):
        '''Return length of longest label name'''
        labelnames = []
        for algo, labels in self.algodict.iteritems():
            for label, params in labels.iteritems():
                labelnames.append(label)
        if labelnames:
            return len(max(labelnames, key=len))
        else:
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
        if fixed_columns:
            for label in self.labelfile:
                print('{:50} {:3} {:15} {:3}'
                      .format(label[0][:50], str(label[1])[:3],
                              label[2][:15], str(label[3])))
        else:
            divlen = self.getLongestLabel()
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
