'''Subcommand module `remove`; contains only a single class `Command`'''

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
from dispass.interactive_editor import InteractiveEditor


class Command(CommandBase):
    '''Remove label from labelfile'''

    usagestr = (
        'usage: dispass remove [-n] [-s] <labelname> [<labelname2>] [...]\n'
        '       dispass remove [-i] [-h]'
    )
    description = 'Remove label from labelfile'
    optionList = (
        ('interactive', ('i', False, 'remove label in an interactive manner')),
        ('help',    ('h', False, 'show this help information')),
        ('dry-run', ('n', False,
                     'do not actually remove label from labelfile')),
        ('silent',  ('s', False, 'do not print success message')),
    )

    def run(self):
        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            if not lf.promptForCreation(silent=self.flags['silent']):
                return 1

        if self.flags['interactive']:
            InteractiveEditor(settings, lf, interactive=False).remove()
            return 0

        if not self.args or self.flags['help']:
            print(self.usage)
            return 0

        for arg in set(self.args):
            if lf.remove(arg):
                if not self.flags['silent']:
                    print("Label '{name}' removed".format(name=arg))
            else:
                if not self.flags['silent']:
                    print("Label '{name}' doesn't exist in labelfile"
                          .format(name=arg))

        if not self.flags['dry-run']:
            lf.save()
