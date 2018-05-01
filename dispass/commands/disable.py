'''Subcommand module 'disable'; contains only a single class `Command`'''

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

from dispass.commands.decorators import write_labels


@write_labels
class Command(CommandBase):
    '''Disable a label without throwing it away'''

    usagestr = (
        'usage: dispass disable <label>'
    )

    description = (
        'Disable a label without throwing it away'
    )

    optionList = (
        ('help',    ('h', False, 'show this help information')),
        ('silent',  ('s', False, 'do not print success message')),
    )

    def run(self, lf):
        '''Parse the arguments and disable using `Filehandler.disable`.'''

        if not len(self.args) == 1 or self.flags['help']:
            print(self.usage)
            return

        labelname = self.args[0]

        if lf.disable(labelname):
            if not self.flags['silent']:
                print("Label '{name}' disabled".format(name=labelname))
        else:
            if not self.flags['silent']:
                print("Label '{name}' could not be disabled"
                      .format(name=labelname))
