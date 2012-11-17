'''Dispass labelfile manager'''

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

import getopt
import os
import sys

import dispass
from filehandler import Filehandler
from interactive_editor import InteractiveEditor

versionStr = dispass.versionStr
__version_info__ = dispass.__version_info__


class DispassLabel(object):
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
                lf = Filehandler(file_location=a)
                f_flag = a
            elif o in ("-l", "--list"):
                l_flag = True
            elif o in "--script":
                script_flag = True
            else:
                assert False, "unhandled option"

        if f_flag:
            lf = Filehandler(file_location=f_flag)
        else:
            lf = Filehandler()

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

        InteractiveEditor(lf, interactive=True)

if __name__ == '__main__':
    sys.exit(DispassLabel().main(sys.argv))
