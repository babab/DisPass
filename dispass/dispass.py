'''Password manager for GNU/Linux, \*BSD, MacOS X and Windows.'''

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

import os
import sys

import pycommand

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2011-2016  Benjamin Althues & Tom Willemse"
__version_info__ = (0, 3, 0, 'final', 0)
__version__ = '0.3.0'
versionStr = 'DisPass ' + __version__


def verboseVersionInfo():
    '''Returns a string with verbose version information

    The string shows the version of DisPass and that of Python.
    It also displays the name of the operating system/platform name.

    '''
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

    disabled = False
    '''Bool. Default disabled state'''

settings = Settings()


class DispassCommand(pycommand.CommandBase):
    '''Main shell command object'''

    usagestr = 'usage: dispass [options] <command> [<args>]'

    description = (
        'Commands:\n'
        '   add          add a new label to labelfile\n'
        '   disable      disable a label without throwing it away\n'
        '   enable       enable a label\n'
        '   generate     generate passphrases for one or more labels\n'
        '   gui          start the graphical version of DisPass\n'
        '   help         show this help information\n'
        '   increment    increment the sequence number of a label\n'
        '   list         print a formatted table of labelfile contents\n'
        '   remove       remove label from labelfile\n'
        '   update       update length, algo or seqno of a label\n'
        '   version      show full version information'
    )

    optionList = (
        ('file',        ('f', '<labelfile>', 'override labelfile')),
        ('help',        ('h', False, 'show this help information')),
        ('version',     ('V', False, 'show full version information')),
    )

    usageTextExtra = (
        "See 'dispass help <command>' for more information on a "
        "specific command.\nFor full documentation, see 'man dispass' "
        "or visit https://dispass.org/"
    )

    def run(self):
        '''The `run` method of the main command

        This is the first point of entry that will parse the command and
        arguments given in the shell by the user, directing arguments to
        subcommands if applicable.

        The subcommands are imported in this method, since doing it in the
        module itself causes circular import problems. There is support for
        dynamically loading the modules, so you can define custom commands. The
        (main) subcommands get imported explicitly so that 'freezing' apps like
        PyInstaller will correctly include the modules.

        '''

        import commands.add
        import commands.disable
        import commands.enable
        import commands.generate
        import commands.gui
        import commands.help
        import commands.increment
        import commands.list
        import commands.remove
        import commands.update
        import commands.version

        self.commands = {
            'add': commands.add.Command,
            'disable': commands.disable.Command,
            'enable': commands.enable.Command,
            'generate': commands.generate.Command,
            'gui': commands.gui.Command,
            'help': commands.help.Command,
            'increment': commands.increment.Command,
            'list': commands.list.Command,
            'remove': commands.remove.Command,
            'update': commands.update.Command,
            'version': commands.version.Command,
        }

        if self.flags['help']:
            print(self.usage)
            return
        elif self.flags['version']:
            print(verboseVersionInfo())
            return

        if not self.args:
            print(self.usage)
            return 2

        try:
            cmd = super(DispassCommand, self).run()
        except pycommand.CommandExit as e:
            return e.err

        cmd.registerParentFlag('file', self.flags['file'])

        if cmd.error:
            print('dispass {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()
