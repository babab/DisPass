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
    print 'USAGE: dispass [-cghoV] [-f <labelfile>] [-s <string>] [--script]'
    print '       dispass [-co] [-l <length>] <label> [<label2>] [...]',
    print '[--script]\n', '       gdispass'
    print
    print 'Options:'
    print '-c, --create    use if this passphrase is new (check input PW)'
    print '-g, --gui       start guided graphical version of DisPass'
    print '-h, --help      show this help and exit'
    print '-o, --output    output passphrases to stdout (instead of the '
    print '                more secure way of displaying via curses)'
    print '-V, --version   show full version information and exit'
    print
    print '-l <length>, --length=<length>'
    print '                set length of passphrase (default: 30, max: 171)'
    print '-s <string>, --search=<string>'
    print ' ' * 15, 'dispass label from file that uniquely matches <string>'
    print '-f <labelfile>, --file=<labelfile>'
    print '                set location of labelfile (default: ~/.dispass)'
    print "--script        optimize input/output for 'wrapping' dispass"


def main(argv):
    '''Entry point and handler of command options and arguments

    :Parameters:
        - `argv`: List of command arguments
    '''

    execname = argv[0].split('/').pop()
    console = cli.CLI()
    f_flag = None
    o_flag = None
    script_flag = None

    try:
        opts, args = getopt.getopt(argv[1:], "cf:ghl:os:V",
                ["create", "file=", "gui", "help", "length=", "output",
                    "script", "search=", "version"])
    except getopt.GetoptError, err:
        print str(err), "\n"
        usage()
        return 2

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
                return 1
            console.setLength(length)
        elif o in ("-f", "--file"):
            lf = labelfile.FileHandler(file_location=a)
            if lf.file_found:
                f_flag = a
            else:
                print 'error: could not load labelfile at "%s"\n' \
                        % lf.file_location
                return 1
        elif o in ("-s", "--search"):
            if f_flag:
                lf = labelfile.FileHandler(file_location=f_flag)
            else:
                lf = labelfile.FileHandler()

            if lf.file_found:
                result = lf.search(a)

                if not result:
                    print '%s: could not find a label with "%s" in labelfile' \
                            % (execname, a)
                    return
                elif isinstance(result, int):
                    print '%s: %s labels found, please be more specific' \
                            % (execname, result)
                    return

                console.interactive(result)
                return
            else:
                print 'error: could not load labelfile at "%s"\n' \
                        % lf.file_location
                return 1
        elif o in ("-o", "--output"):
            console.setCurses(False)
        elif o in ("-h", "--help"):
            usage()
            return
        elif o in ("-V", "--version"):
            print versionStr, '-', __version_info__, 'running on', os.name
            return
        elif o in "--script":
            console.setScriptableIO()
        else:
            assert False, "unhandled option"

    if labels:
        console.interactive(labels)
    else:
        if f_flag:
            lf = labelfile.FileHandler(file_location=f_flag)
        else:
            lf = labelfile.FileHandler()

        if lf.file_found:
            console.interactive(lf.labels)
            return
        else:
            print 'error: could not load labelfile at %s\n' % lf.file_location
            usage()
            return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
