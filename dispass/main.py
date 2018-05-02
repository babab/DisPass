'''Main functions / setup.py script entry points for console and GUI.'''

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

import sys

from dispass.dispass import (
    DispassCommand,
    settings,
)
from dispass.filehandler import Filehandler


def console():
    try:
        cmd = DispassCommand(sys.argv[1:])
        if cmd.error:
            print('error: {0}'.format(cmd.error))
            return 1
        else:
            return cmd.run()
    except KeyboardInterrupt:
        print('\nOk, bye')
        return 0


def gui():
    try:
        from dispass.gui import GUI

        gui = GUI(settings, Filehandler(settings))
        gui.mainloop()
    except ImportError:
        print(
            'Could not find Tkinter, this is a package needed for using\n'
            'the graphical version of dispass.\n\n'
            'For installation instructions, please see the\n'
            '"Using gdispass" chapter of the documentation.'
        )
        return 1
    except KeyboardInterrupt:
        print('\nOk, bye')
        return 0
