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
import os
import sys

import algos
# from cli import CLI
from filehandler import Filehandler
from gui import GUI
from interactive_editor import InteractiveEditor


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

    def usage(self, command=None):
        '''Print help / usage information'''

        if not command or command == 'help':
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
        elif command == 'add':
            print('usage: dispass add [-i] [-n] [-v] [<labelspec>]')
            print
            print('Add a new label to the labelfile and generate passphrase.')
            print('The labelspec looks like this:')
            print
            print('    label[:size[:algorithm[:sequence_number]]]')
            print
            print('Options:')
            print '-i, --interactive    add a new label interactively'
            print '-n, --dry-run        do not actually add label to labelfile'
            print '-v, --verbose        verbose output'
        elif command == 'gui':
            print('usage: dispass gui')
            print
            print('Start the graphical version of DisPass.')
        elif command == 'list':
            print('usage: dispass list')
            print
            print('List all labels in labelfile.')
        else:
            print('command {command} does not exist'.format(command=command))
            return 1
        return 0

        '''
        print 'Options (general):'
        print '-c, --create    use if this passphrase is new (check input PW)'
        print '-g, --gui       start guided graphical version of DisPass'
        print '-h, -?, --help  show this help and exit'
        print '-o, --output    output passphrases to stdout (instead of the '
        print '                more secure way of displaying via curses)'
        print '-V, --version   show full version information and exit'
        print "--script        optimize input/output for 'wrapping' dispass"
        print
        print 'Options (when using labelfile):'
        print '-s <string>, --search=<string>'
        print ' ' * 15, 'dispass label from file that matches <string>'
        print '-f <labelfile>, --file=<labelfile>'
        print '                set location of labelfile'
        print
        print 'Options (when passing labels as arguments):'
        print '-l <length>, --length=<length>'
        print ' ' * 14, 'set length of passphrase (default: 30, max: 171)'
        print '-a <algorithm>, --algo=<algorithm>'
        print '                override algorithm for generating passphrase(s)'
        print '-n <number>, --number=<number>'
        print '                override sequence number (default = 1)'
        '''

    def versionString(self):
        return('{dispass} - {version} running on {os}'
               .format(dispass=versionStr, version=__version_info__,
                       os=os.name))

    def startGUI(self):
        try:
            g = GUI(settings)
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
        except exceptions.KeyboardInterrupt:
            print '\nOk, bye'

    def main(self, argv):
        '''Entry point and handler of command options and arguments

        :Parameters:
            - `argv`: List of command arguments
        '''

        # execname = argv[0].split('/').pop()
        # console = CLI(settings)
        # a_flag = None
        # f_flag = None

        try:
            opts, arguments = getopt.getopt(argv[1:],
                                            "hV?", ["help", "version"])
        except getopt.GetoptError, err:
            print str(err)
            return 1

        if arguments:
            args = arguments
        else:
            args = False

        for o, a in opts:
            if o in ("-h", "-?", "--help"):
                if args:
                    return self.usage(args[0])
                return self.usage()
            elif o in ("-V", "--version"):
                print(self.versionString())
                return

        if not args:
            self.usage()
            return 2
        elif args[0] == 'add':
            return self.usage(args[0])
        elif args[0] == 'gui':
            self.startGUI()
            return
        elif args[0] == 'help':
            if len(args) > 1:
                self.usage(args[1])
            else:
                self.usage()
            return
        elif args[0] == 'list':
            print 'command n/a yet'
            return
        elif args[0] == 'settings':
            print 'command n/a yet'
            return
        elif args[0] == 'version':
            print(self.versionString())
            return


class DispassLabel(object):
    '''Command handler for ``dispass-label``'''

    def usage(self):
        '''Print help / usage information'''

        print('USAGE: dispass-label [-hlV] [-f <labelfile>] \n'
              '                     [-a|--add <labelspec>] [--script]\n\n'
              'Options:\n'
              '-h, --help      show this help and exit\n'
              '-l, --list      print all labels and options found '
              'in labelfile\n'
              '-V, --version   show full version information and exit\n'
              '-f <labelfile>, --file=<labelfile>\n'
              '                set location of labelfile\n'
              '-a, --add <labelspec>\n'
              '                add a new label to the labelfile, the\n'
              '                labelspec looks like this:\n'
              '                label[:size[:algorithm[:sequence_number]]]\n'
              '-r, --remove <labelname>\n'
              '                remove a label from the labelfile\n'
              "--script        optimize input/output for 'wrapping' "
              'dispass-label')

    def main(self, argv):
        '''Entry point and handler of command options and arguments

        :Parameters:
            - `argv`: List of command arguments
        '''

        f_flag = None
        l_flag = None
        script_flag = None
        a_flag = None
        r_flag = None

        try:
            opts, args = getopt.getopt(argv[1:], "a:f:hlr:V",
                                       ["add=", "file=", "help", "list",
                                        "remove=", "script", "version"])
        except getopt.GetoptError, err:
            print str(err), "\n"
            self.usage()
            return 2

        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
                return
            elif o in ("-V", "--version"):
                print versionStr, '-', __version_info__, 'running on', os.name
                return
            elif o in ("-f", "--file"):
                f_flag = a
            elif o in ("-l", "--list"):
                l_flag = True
            elif o in "--script":
                script_flag = True
            elif o in ("-a", "--add"):
                a_flag = a.split(':')
            elif o in ("-r", "--remove"):
                r_flag = a
            else:
                assert False, "unhandled option"

        if f_flag:
            lf = Filehandler(settings, file_location=f_flag)
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            print ('error: could not load labelfile at "{loc}"'
                   .format(loc=lf.file_location))
            inp = raw_input('Do you want to create it? Y/n ')

            if inp == '' or inp[0].lower() == 'y':
                if not lf.save():
                    print ('error: could not save to "{loc}"\n'
                           .format(loc=lf.file_location))
                    return 1
            else:
                return 1

        if l_flag:
            lf.printLabels(script_flag)
            return
        elif a_flag:
            params = len(a_flag)

            length = 0
            try:
                length = params >= 2 and int(a_flag[1])
            except ValueError:
                pass

            if not length:
                length = settings.passphrase_length

            algo = params >= 3 and a_flag[2] or settings.algorithm
            if not algo in algos.algorithms:
                algo = settings.algorithm

            seqno = 0
            if algo != 'dispass1':
                try:
                    seqno = params >= 4 and int(a_flag[3])
                except ValueError:
                    pass

            if not seqno:
                seqno = settings.sequence_number

            if lf.add(labelname=a_flag[0], length=length, algo=algo,
                      seqno=seqno):
                lf.save()
                print('Label saved')
                lf.parse()
                return 0
            else:
                print('Label already exists in labelfile')
                return 1
        elif r_flag:
            if lf.remove(r_flag):
                lf.save()
                print('Label removed')
                return 0
            else:
                print("Label doesn't exist in labelfile")
                return 1

        InteractiveEditor(settings, lf, interactive=True)

if __name__ == '__main__':
    sys.exit(Dispass().main(sys.argv))
