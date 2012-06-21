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

import getopt
import os
import sys

import cli
import gui
import labelfile

def usage():
    '''Print help / usage information'''

    print "%s - http://dispass.babab.nl/" % (versionStr)
    print
    print "When DisPass is executed as 'gdispass' or 'dispass -g',"
    print 'the graphical version will be started.'
    print
    print 'USAGE: dispass [-cghoV] [-f labelfile]'
    print '       dispass [-co] [-l length] label [label2] [label3] [...]'
    print '       gdispass'
    print
    print 'Options:'
    print '-c, --create    use if this passphrase is new (check input PW)'
    print '-g, --gui       start guided graphical version of DisPass'
    print '-h, --help      show this help and exit'
    print '-o, --output    output passphrases to stdout (instead of the '
    print '                more secure way of displaying via curses)'
    print '-V, --version   show full version information and exit'
    print
    print '-f <labelfile>, --file=<labelfile>'
    print '                set location of labelfile (default: ~/.dispass)'
    print '-l <length>, --length=<length>'
    print '                set length of passphrase (default: 30, max: 171)'


def main(argv):
    '''Entry point and handler of command options and arguments

    :Parameters:
        - `argv`: List of command arguments
    '''

    console = cli.CLI()

    try:
        opts, args = getopt.getopt(argv[1:], "cf:ghl:oV",
                ["create", "file=", "gui", "help", "length=", "output",
                    "version"])
    except getopt.GetoptError, err:
        print str(err), "\n"
        usage()
        sys.exit(2)

    if args:
        labels = args
    else:
        labels = False

    for o, a in opts:
        if o in ("-g", "--gui"):
            gui.GUI()
            return
        elif o in ("-c", "--create"):
            console.setPrompt(promptDouble=True)
        elif o in ("-l", "--length"):
            try:
                length = int(a)
            except ValueError:
                print 'error: length must be a number\n'
                usage()
                sys.exit(1)
            console.setLength(length)
        elif o in ("-f", "--file"):
            lf = labelfile.FileHandler(file_location=a)
            if lf.file_found:
                console.interactive(lf.labels)
            else:
                print 'error: could not load labelfile at "%s"\n' \
                        % lf.file_location
                usage()
            sys.exit(1)
        elif o in ("-o", "--output"):
            console.setCurses(False)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-V", "--version"):
            print versionStr, '-', __version_info__, 'running on', os.name
            sys.exit()
        else:
            assert False, "unhandled option"

    if labels:
        console.interactive(labels)
    else:
        lf = labelfile.FileHandler()
        if lf.file_found:
            console.interactive(lf.labels)
        else:
            print 'error: could not load labelfile at %s\n' % lf.file_location
            usage()
            sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
