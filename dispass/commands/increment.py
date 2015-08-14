'''Subcommand module `increment`; contains only a single class `Command`'''

# Copyright (c) 2012-2015  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2015  Benjamin Althues <benjamin@babab.nl>
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

from dispass.common import CommandBase
from dispass.dispass import settings
from dispass.filehandler import Filehandler


class Command(CommandBase):
    '''Increment the sequence number of a label'''

    usagestr = (
        'usage: dispass increment [-n] [-s] <label>\n'
        '       dispass increment [-h]'
    )

    description = (
        'Increment the sequence number of a label'
    )

    optionList = (
        ('help',    ('h', False, 'show this help information')),
        ('dry-run', ('n', False, 'do not actually update label in labelfile')),
        ('silent',  ('s', False, 'do not print success message')),
    )

    def run(self):
        '''Parse the arguments and increment using `FileHandler.increment`.'''

        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not len(self.args) == 1 or self.flags['help']:
            print self.usage
            return

        if not lf.file_found:
            # File not found? No possible label to increment.
            return 1

        labelname = self.args[0]

        if lf.increment(labelname):
            if not self.flags['silent']:
                print("Label '{name}' incremented".format(name=labelname))
        else:
            if not self.flags['silent']:
                print("Label '{name}' could not be incremented"
                      .format(name=labelname))

        if not self.flags['dry-run']:
            lf.save()
