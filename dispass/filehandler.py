'''Dispass labelfile handler'''

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
    '''List of [(labelname, length, algorithm, seqno, disabled), ... ]'''

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
        '''Create dictionary {algorithm: (label, (length, seqno, disabled))}'''

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
            disabled = self.settings.disabled

            for arg in line:
                if 'length=' in arg:
                    try:
                        length = int(arg.strip('length='))
                    except ValueError:
                        print("Warning: Invalid length in: '{}'".format(line))
                elif 'algo=' in arg:
                    algo = arg.strip('algo=')
                elif 'seqno=' in arg:
                    seqno = arg.strip('seqno=')
                elif 'disabled=' in arg:
                    disabled = arg.lstrip('disabled=') == 'True'

            self.labelfile.append((labelname, length, algo, seqno, disabled))

        return self

    def find(self, labelname):
        for label in self.labelfile:
            if labelname == label[0]:
                return label

    def add(self, labelname, length=None, algo=None, seqno=None,
            disabled=False):
        '''Add label to `labelfile`'''

        length = length if length else self.settings.passphrase_length
        algo = algo if algo else self.settings.algorithm
        seqno = seqno if seqno else self.settings.sequence_number
        disabled = disabled if disabled else self.settings.disabled

        if self.find(labelname):
            return False

        self.labelfile.append((labelname, length, algo, seqno, disabled))
        return True

    def update(self, labelname, length=None, algo=None, seqno=None,
               disabled=None):
        '''Update label in `labelfile`'''

        label = self.find(labelname)

        if not label:
            return False

        params = {'length': length if length else label[1],
                  'algo': algo if algo else label[2],
                  'seqno': seqno if seqno else label[3],
                  'disabled': disabled if disabled is not None else label[4]}

        return self.remove(labelname) and self.add(labelname, **params)

    def increment(self, labelname):
        '''Increment sequence number of `labelfile`'''

        label = self.find(labelname)

        if not label or label[2] == 'dispass1':
            return False

        return self.update(labelname, seqno=int(label[3]) + 1)

    def disable(self, labelname, disabled=True):
        '''Disable or enable a label'''

        label = self.find(labelname)

        if not label:
            return False

        return self.update(labelname, disabled=disabled)

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
            if label[2] == 'dispass1':
                options = ('length={length}  algo={algo} disabled={disabled}'
                           .format(length=label[1], algo=label[2],
                                   disabled=label[4]))
            else:
                options = (('length={length}  algo={algo}  seqno={seqno} '
                            'disabled={disabled}')
                           .format(length=label[1], algo=label[2],
                                   seqno=label[3], disabled=label[4]))
            labelfile += ('{label:{divlen}}  {options}\n'
                          .format(label=label[0], options=options,
                                  divlen=self.longest_label))
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
            - A tuple with 5 values ``(label, length, algo, seqno, disabled))``
                - `label`: Label to use for passphrase generation
                - `length`: Length to use for passphrase generation
                - `algo`: Algorithm to use for passphrase generation
                - `seqno`: Sequence number to use for passphrase generation
                - `disabled`: Whether or not the passphrase is disabled

        '''

        for labeltup in self.labelfile:
            if label == labeltup[0]:
                return labeltup
        return False

    def printLabels(self, fixed_columns=False, labels_only=False, all_=False):
        '''Print a formatted table of labelfile contents

        :Parameters:
            - `fixed_columns`: Boolean.
            - `labels_only`: Boolean.

        If `labels_only` is True, only the labelnames will be printed.

        If `fixed_columns` is true the output will be optimized for easy
        parsing by other programs and scripts by not printing the header
        and always printing one entry on a single line using the
        following positions:

        * Column 1-50: labelname (50 chars)
        * Column 52-54: length (3 chars wide)
        * Column 56-70: hash algo (15 chars wide)
        * Column 72-74: sequence number (3 chars wide)
        * Column 76-77: disabled (1 char wide)

        If fixed columns is false an ascii table is printed with a variable
        width depending on the length of the longest label.
        '''

        self.refresh()
        if labels_only:
            for label in self.labelfile:
                if all_ or not label[4]:
                    print(label[0])
            return

        if fixed_columns:
            for label in self.labelfile:
                if all_ or not label[4]:
                    print('{:50} {:3} {:15} {:3} {}'
                          .format(label[0][:50], str(label[1])[:3],
                                  label[2][:15], str(label[3]),
                                  'y' if label[4] else 'n'))
        else:
            divlen = self.longest_label

            if not divlen:
                return

            divtitle = 'Label'
            divlen = max(divlen, len(divtitle))

            print('+-{spacer:{fill}}-+--------+----------+--------+---+\n'
                  '| {title:{fill}} | Length | Algo     | Number | X |\n'
                  '+-{spacer:{fill}}-+--------+----------+--------+---+'
                  .format(spacer='-' * divlen, title=divtitle, fill=divlen))

            for label in self.labelfile:
                if all_ or not label[4]:
                    print('| {:{fill}} |    {:3} | {:8} |      {:3>} | {} |'
                          .format(label[0], label[1], label[2], int(label[3]),
                                  'y' if label[4] else 'n', fill=divlen))
            print('+-{:{fill}}-+--------+----------+--------+---+'
                  .format('-' * divlen, fill=divlen))

    def promptForCreation(self, silent=False):
        '''Create the labelfile, optionally warning the user beforehand

        :Parameters:
            - `silent`: When True, the user will not be warned.

        :Returns: Boolean. Indicating if the labelfile was created succesfully.
        '''
        if silent:
            if self.save():
                return True
            else:
                return False

        print('error: could not load labelfile at "{loc}"'
              .format(loc=self.file_location))
        inp = raw_input('Do you want to create it? Y/n ')

        if inp == '' or inp[0].lower() == 'y':
            # create directories for file_location if they don't exist
            dir = os.path.abspath(os.path.dirname(self.file_location))
            if not os.path.exists(dir):
                os.makedirs(dir)
            # save file
            if not self.save():
                print('error: could not save to "{loc}"\n'
                      .format(loc=self.file_location))
                return False
        else:
            return False
        return True
