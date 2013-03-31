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

from dispass.common import CommandBase


class Command(CommandBase):
    usagestr = ('usage: dispass add [-no] <labelspec>\n'
                '       dispass add [-hio]')
    description = (
        'Add a new label to the labelfile and generate passphrase.\n'
        'The labelspec looks like this:\n\n'
        '    label[:size[:algorithm[:sequence_number]]]'
    )
    optionList = (
        ('help',        ('h', 'show this help information')),
        ('interactive', ('i', 'add a new label interactively')),
        ('dry-run',     ('n', 'do not actually add label to labelfile')),
        ('output',      ('o', 'generate and output passphrase for label')),
    )

    def run(self):
        if self.flags['help']:
            print self.usage
            return

        if not self.args:
            if not self.flags['interactive']:
                print self.usage
                return
        else:
            labelspec = self.args[0]
            print labelspec
            return
