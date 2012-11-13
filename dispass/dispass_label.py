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
from labelfile import FileHandler
from interactive_editor import InteractiveEditor

versionStr = dispass.versionStr
__version_info__ = dispass.__version_info__


def usage():
    '''Print help / usage information'''

    print 'USAGE: dispass-label [-hlV] [-f <labelfile>] [--script]'
    print
    print 'Options:'
    print '-h, --help      show this help and exit'
    print '-l, --list      print all labels and options found in labelfile'
    print '-V, --version   show full version information and exit'
    print '-f <labelfile>, --file=<labelfile>'
    print '                set location of labelfile'
    print "--script        optimize input/output for 'wrapping' dispass-label"


def main(argv):
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
        usage()
        return 2

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        elif o in ("-V", "--version"):
            print versionStr, '-', __version_info__, 'running on', os.name
            return
        elif o in ("-f", "--file"):
            lf = FileHandler(file_location=a)
            if lf.file_found:
                f_flag = a
            else:
                print ('error: could not load labelfile at '
                       '"{loc}"\n').format(loc=lf.file_location)
                return 1
        elif o in ("-l", "--list"):
            l_flag = True
        elif o in "--script":
            script_flag = True
        else:
            assert False, "unhandled option"

    if f_flag:
        lf = FileHandler(file_location=f_flag)
    else:
        lf = FileHandler()

    if not lf.file_found:
        print 'error: could not load labelfile at %s\n' % lf.file_location
        usage()
        return 1

    if l_flag:
        lf.printLabels(script_flag)
        return

    InteractiveEditor(lf, interactive=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
