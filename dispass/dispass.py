'''Multi-platform console/gui passphrase generator'''

# Copyright (c) 2011-2012 Benjamin Althues <benjamin@babab.nl>
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
__copyright__ = "Copyright (C) 2011-2012 Benjamin Althues"
__version_info__ = (0, 1, 0, 'alpha', 8)
__version__ = '0.1a8'
versionStr = 'DisPass ' + __version__

import exceptions
import getopt
import os
import sys

import algos
from cli import CLI
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

    def usage(self):
        '''Print help / usage information'''

        print "%s - http://dispass.babab.nl/" % (versionStr)
        print
        print 'USAGE: dispass [options]'
        print('       dispass [options] <label> [<label2>] [<label3>] [...]')
        print '       gdispass'
        print
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

    def main(self, argv):
        '''Entry point and handler of command options and arguments

        :Parameters:
            - `argv`: List of command arguments
        '''

        execname = argv[0].split('/').pop()
        console = CLI(settings)
        a_flag = None
        f_flag = None

        try:
            opts, args = getopt.getopt(
                argv[1:], "a:cf:ghl:n:os:V?",
                ["algo=", "create", "file=", "gui", "help", "length=",
                 "number", "output", "script", "search=", "version"])
        except getopt.GetoptError, err:
            print str(err), "\n"
            self.usage()
            return 2

        if args:
            labels = args
        else:
            labels = False

        for o, a in opts:
            if o in ("-g", "--gui"):
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
                return
            elif o in ("-a", "--algo"):
                algoname = a.lower()
                if algoname in algos.algorithms:
                    console.setAlgo(algoname)
                else:
                    print 'error: algo "{algo}" does not exist'.format(algo=a)
                    return 1
                a_flag = True
            elif o in ("-n", "--number"):
                try:
                    seqno = int(a)
                except ValueError:
                    print 'error: sequence number must be a number\n'
                    self.usage()
                    return 1
                console.setSeqNo(seqno)
            elif o in ("-c", "--create"):
                console.createLabel = True
            elif o in ("-l", "--length"):
                try:
                    length = int(a)
                except ValueError:
                    print 'error: length must be a number\n'
                    self.usage()
                    return 1
                console.setLength(length)
            elif o in ("-f", "--file"):
                f_flag = a
            elif o in ("-s", "--search"):
                if f_flag:
                    lf = Filehandler(settings, file_location=f_flag)
                else:
                    lf = Filehandler(settings)

                if lf.file_found:
                    result = lf.search(a)

                    if not result:
                        print('{execname}: could not find a label with '
                              '"{label}" in labelfile'
                              .format(execname=execname, label=a))
                        return
                    elif isinstance(result, int):
                        print('{execname}: {qty} labels found, please be more '
                              'specific').format(execname=execname, qty=result)
                        return

                    console.interactive(result, lf)
                    return
                else:
                    print ('error: could not load labelfile at '
                           '"{loc}"\n').format(loc=lf.file_location)
                    return 1
            elif o in ("-o", "--output"):
                console.setCurses(False)
            elif o in ("-h", "-?", "--help"):
                self.usage()
                return
            elif o in ("-V", "--version"):
                print versionStr, '-', __version_info__, 'running on', os.name
                return
            elif o in "--script":
                console.setScriptableIO()
            else:
                assert False, "unhandled option"

        if f_flag:
            lf = Filehandler(settings, file_location=f_flag)
        else:
            lf = Filehandler(settings)

        if labels:
            console.interactive(labels, lf)
        else:
            if a_flag:
                print('error: option -a can only be used when specifying '
                      'label(s) as argument(s)')
                return 1

            if lf.file_found:
                console.interactive(lf.algodict, lf)
                return
            else:
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


class DispassLabel(object):
    '''Command handler for ``dispass-label``'''

    def usage(self):
        '''Print help / usage information'''

        print('USAGE: dispass-label [-hlV] [-f <labelfile>] [--script]\n\n'
              'Options:\n'
              '-h, --help      show this help and exit\n'
              '-l, --list      print all labels and options found '
              'in labelfile\n'
              '-V, --version   show full version information and exit\n'
              '-f <labelfile>, --file=<labelfile>\n'
              '                set location of labelfile\n'
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

        try:
            opts, args = getopt.getopt(argv[1:], "f:hlV",
                                       ["file", "help", "list",
                                        "script", "version"])
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

        InteractiveEditor(settings, lf, interactive=True)

if __name__ == '__main__':
    sys.exit(Dispass().main(sys.argv))
