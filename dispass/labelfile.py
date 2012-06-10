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

from os.path import expanduser

class Parse:
    '''Labelfile parser'''

    file_stripped = []
    '''Labelfile stripped for parsing'''

    labels = []
    '''List of labels (+options)'''

    def __init__(self, file_location='~/.dispass'):
        '''Open file and strip empty lines and comments'''

        try:
            filehandle = open(expanduser(file_location), 'r')
        except IOError:
            print 'error: could not load labelfile'
            return

        for i in filehandle:
            if i[0] != '\n' and i[0] != '#':
                self.file_stripped.append(i)

    def parse(self):
        '''Strip spaces and create lists of labels with their options'''

        for i in self.file_stripped:
            wordlist = []
            line = i.rsplit(' ')
            for word in line:
                if word != '':
                    wordlist.append(word.strip('\n'))
            self.labels.append(wordlist)

class Write:
    '''Labelfile editor'''
    pass

if __name__ == '__main__':
    p = Parse()
    p.parse()
    for i in p.labels:
        print i
