'''Subcommand module 'enable'; contains only a single class `Command`'''

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

from pycommand import CommandBase

from dispass.dispass import settings
from dispass.filehandler import Filehandler


class Command(CommandBase):
    '''Enable a label'''

    usagestr = (
        'usage: dispass enable <label>'
    )

    description = (
        'Enable a label'
    )

    optionList = (
        ('help',    ('h', False, 'show this help information')),
        ('dry-run', ('n', False, 'do not actually update label in labelfile')),
        ('silent',  ('s', False, 'do not print success message')),
    )

    def run(self):
        '''Parse the arguments and enable using `Filehandler.disable`.'''

        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not len(self.args) == 1 or self.flags['help']:
            print self.usage
            return

        if not lf.file_found:
            # File not found? No possible label to enable.
            return 1

        labelname = self.args[0]

        if lf.disable(labelname, False):
            if not self.flags['silent']:
                print("Label '{name}' enabled".format(name=labelname))
        else:
            if not self.flags['silent']:
                print("Label '{name}' could not be enabled"
                      .format(name=labelname))

        if not self.flags['dry-run']:
            lf.save()
