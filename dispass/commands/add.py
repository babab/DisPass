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

from dispass import algos
from dispass.common import CommandBase
from dispass.dispass import settings
from dispass.filehandler import Filehandler


class Command(CommandBase):
    usagestr = 'usage: dispass add [options] <labelspec>'
    description = (
        'Add a new label to the labelfile and generate passphrase.\n'
        'The labelspec looks like this:\n\n'
        '    label[:size[:algorithm[:sequence_number]]]'
    )
    optionList = (
        ('help',        ('h', 'show this help information')),
        #('interactive', ('i', 'add a new label interactively')),
        #('generate',    ('g', 'generate and output passphrase for label')),
        ('dry-run',     ('n', 'do not actually add label to labelfile')),
        ('silent',      ('s','do not print success message')),
    )

    def run(self):
        if not self.args or self.flags['help']:
            print self.usage
            return

        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            if not lf.promptForCreation():
                return 1

        labelspec = self.args[0].split(':')
        params = len(labelspec)

        length = 0
        try:
            length = params >= 2 and int(labelspec[1])
        except ValueError:
            pass

        if not length:
            length = settings.passphrase_length

        algo = params >= 3 and labelspec[2] or settings.algorithm
        if not algo in algos.algorithms:
            algo = settings.algorithm

        seqno = 0
        if algo != 'dispass1':
            try:
                seqno = params >= 4 and int(labelspec[3])
            except ValueError:
                pass

        if not seqno:
            seqno = settings.sequence_number

        if lf.add(labelname=labelspec[0], length=length, algo=algo,
                  seqno=seqno):
            if not self.flags['dry-run']:
                lf.save()
            if not self.flags['silent']:
                print('Label saved')
        else:
            print('Label already exists in labelfile')
            return 1
