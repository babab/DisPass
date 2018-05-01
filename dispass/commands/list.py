'''Subcommand module `list`; contains only a single class `Command`'''

# Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2018  Benjamin Althues <benjamin@babab.nl>
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

from dispass.commands.decorators import read_labels


@read_labels()
class Command(CommandBase):
    '''Print a formatted table of labelfile contents'''

    usagestr = 'usage: dispass list [-h] [-n] [--script]'
    description = (
        'Print a formatted table of labelfile contents\n\n'

        'If --script is passed the output will be optimized for easy\n'
        'parsing by other programs and scripts by not printing the header\n'
        'and always printing one entry on a single line using the\n'
        'following positions:\n\n'

        'Column  1-50: labelname        50 chars wide\n'
        'Column 52-54: length            3 chars wide\n'
        'Column 56-70: hash algo        15 chars wide\n'
        'Column 72-74: sequence number   3 chars wide\n'
        'Column 76-77: disabled          1 char wide'
    )
    optionList = (
        ('all',         ('a', False, 'include disabled labels')),
        ('help',        ('h', False, 'show this help information')),
        ('names-only',  ('n', False, 'only print names of the labels')),
        ('script',      ('', False, 'output in fixed columns')),
    )

    def run(self, lf):
        if self.flags['help']:
            print(self.usage)
            return

        lf.printLabels(fixed_columns=self.flags['script'],
                       labels_only=self.flags['names-only'],
                       all_=self.flags['all'])
