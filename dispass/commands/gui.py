'''Subcommand module `gui`; contains only a single class `Command`'''

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
    '''Start the graphical version of DisPass'''

    usagestr = 'usage: dispass gui [-h]'
    description = 'Start the graphical version of DisPass.'
    optionList = (('help', ('h', False, 'show this help information')),)

    def run(self):
        '''Entry point and handler of command options and arguments'''

        if self.flags['help']:
            print(self.usage)
            return

        if self.parentFlags['file']:
            lf = Filehandler(settings,
                             file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        try:
            from dispass.gui import GUI
            g = GUI(settings, lf)
            g.mainloop()
        except ImportError:
            print('Could not find Tkinter, this is a package needed '
                  'for using\n' 'the graphical version of dispass.\n'
                  '\n'
                  'For installation instructions, please see the\n'
                  '"Using gdispass" chapter of the documentation.')
            return 2
