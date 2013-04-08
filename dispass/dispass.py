'''Password manager for GNU/Linux, *BSD, MacOS X and Windows.'''

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

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2011, 2012, 2013  Benjamin Althues"
__version_info__ = (0, 3, 0, 'alpha', 0)
__version__ = '0.3.0-dev'
versionStr = 'DisPass ' + __version__

import exceptions
import importlib
import os
import sys

from common import CommandBase


def verboseVersionInfo():
    return('{dispass} {fullversion}\n\n'
           'Python {python}\nPlatform is {os}'
           .format(dispass=versionStr, fullversion=__version_info__,
                   python=sys.version.replace('\n', ''), os=os.name))


class Settings(object):
    '''Global settings'''

    passphrase_length = 30
    '''Int. Default passphrase length'''

    algorithm = 'dispass1'
    '''String. The algorithm to use, default is dispass1'''

    sequence_number = 1
    '''Int. Default sequence number'''

settings = Settings()


class DispassCommand(CommandBase):
    usagestr = 'usage: dispass [options] <command> [<args>]'
    description = (
        'Commands:\n'
        '   add          add a new label to labelfile\n'
        '   gui          start the graphical version of DisPass\n'
        '   help         show this help information\n'
        '   list         print a formatted table of labelfile contents\n'
        '   rm           remove label from labelfile\n'
        #'   settings     show default values for length, algo etc.\n'
        '   version      show full version information'
    )
    optionList = (
        ('file',        ('f', '<labelfile>', 'override labelfile')),
        ('help',        ('h', False, 'show this help information')),
        ('version',     ('V', False, 'show full version information')),
    )
    usageTextExtra = (
        "See 'dispass help <command>' for more information on a "
        "specific command."
    )

    def run(self):
        import commands.add
        import commands.gui
        import commands.help
        import commands.list
        import commands.rm
        import commands.version

        if self.flags['help']:
            print(self.usage)
            return
        elif self.flags['version']:
            print(verboseVersionInfo())
            return

        if not self.args:
            print(self.usage)
            return 2
        elif self.args[0][0] == 'a':
            cmd = commands.add.Command(settings=settings, argv=self.args[1:])
        elif self.args[0][0] == 'g':
            cmd = commands.gui.Command(settings=settings, argv=self.args[1:])
        elif self.args[0][0] == 'h':
            cmd = commands.help.Command(settings=settings, argv=self.args[1:])
        elif self.args[0][0] == 'l':
            cmd = commands.list.Command(settings=settings, argv=self.args[1:])
        elif self.args[0][0] == 'r':
            cmd = commands.rm.Command(settings=settings, argv=self.args[1:])
        elif self.args[0][0] == 'v':
            cmd = commands.version.Command(settings=settings,
                                           argv=self.args[1:])
        else:
            try:
                mod = importlib.import_module('dispass.commands.'
                                              + self.args[0])
                cmd = mod.Command(settings=settings, argv=self.args[1:])
            except ImportError:
                print('error: command {cmd} does not exist'
                      .format(cmd=self.args[0]))
                return 1
            except exceptions.KeyboardInterrupt:
                print('\nOk, bye')
                return

        cmd.registerParentFlag('file', self.flags['file'])

        if cmd.error:
            print('dispass {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()
