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
import getopt
import importlib
import os
import sys

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


class Dispass(object):
    '''Command handler for ``dispass``'''

    def usage(self):
        '''Print help / usage information'''
        print('usage: dispass [--file=<labelfile>] <command> [<args>]')
        print
        print('Commands:')
        print('   add          add a new label and generate passphrase')
        print('   gui          start the graphical version of DisPass')
        print('   help         show this help information')
        print('   list         list all labels in labelfile')
        print('   settings     show default values for length, algo etc.')
        print('   version      show full version information')
        print
        print("See 'dispass help <command>' for more information on a "
              "specific command.")

    def main(self, argv):
        '''Entry point and handler of command options and arguments

        :Parameters:
            - `argv`: List of command arguments
        '''

        try:
            opts, arguments = getopt.getopt(argv[1:], "f:hV?",
                                            ['file', "help", "version"])
        except getopt.GetoptError, err:
            print('dispass: {error}' .format(error=str(err)))
            return 1

        if arguments:
            args = arguments
        else:
            args = False

        for o, a in opts:
            if o in ("-h", "-?", "--help"):
                return self.usage()
            elif o in ("-f", "--file"):
                pass
            elif o in ("-V", "--version"):
                print(verboseVersionInfo())
                return

        if not args:
            self.usage()
            return 2
        else:
            try:
                mod = importlib.import_module('dispass.commands.' + args[0])
                cmd = mod.Command(settings=settings, argv=args[1:])
            except ImportError:
                print('error: command {cmd} does not exist'
                      .format(cmd=args[0]))
                return 1
            except exceptions.KeyboardInterrupt:
                print('\nOk, bye')
                return

            if cmd.error:
                print('dispass {cmd}: {error}'
                      .format(cmd=args[0], error=cmd.error))
                return 1
            else:
                return cmd.run()
