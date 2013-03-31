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
    usagestr = 'usage: dispass gui [-h]'
    description = 'Start the graphical version of DisPass.'
    optionList = {'help': ('h', 'show this help information')}

    def run(self):
        '''Entry point and handler of command options and arguments'''

        if self.flags['help']:
            print self.usage
            return

        try:
            from dispass.gui import GUI
            g = GUI(self.settings)
            g.mainloop()
        except ImportError:
            print ('Could not find Tkinter, this is a package needed '
                   'for using\n' 'the graphical version of dispass.\n'
                   'To install, search for a python-tk package for'
                   ' your OS.\n'
                   'Arch Linux     \t\t# pacman -S python-tk\n'
                   'Debian / Ubuntu\t\t$ sudo apt-get install '
                   'python-tk\n'
                   'OpenBSD        \t\t# pkg_add -i python-tk')
            return 2
