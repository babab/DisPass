# vim: set et ts=4 sw=4 sts=4:

'''Generate and disperse/dispell passwords'''

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
__version_info__ = (0, 1, 0, 'alpha', 7)
__version__ = '0.1a7'
versionStr = 'DisPass ' + __version__

class globalSettings:
    '''Global settings used in controlling program flow'''
    useCurses = None
    '''Switch passphrase output to stdout if not True'''

    hasTk = None
    '''False if Tkinter could not be imported'''

settings = globalSettings()

# Python stdlib - required
import base64
import getopt
import getpass
import hashlib
import os
import sys

# Python stdlib - optional
try:
    import curses
    settings.useCurses = True
except ImportError:
    settings.useCurses = False

from gui import GUI

def CLI(labels, pwTypoCheck=False, useCurses=True):
    while True:
        inp = getpass.getpass()
        if pwTypoCheck:
            inp2 = getpass.getpass("Again:")
            if inp == inp2:
                break;
            else:
                print "Passwords do not match. Please try again."
        else:
            break

    if useCurses:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        stdscr.addstr(0, 0, versionStr + " - press 'q' to quit", curses.A_BOLD)
        stdscr.addstr(1, 0, "Your passphrase(s)", curses.A_BOLD)
        divlen = len(max(labels, key=len)) + 2
        j = 3
        for i in labels:
            stdscr.addstr(j,  0, i, curses.A_BOLD)
            stdscr.addstr(j, divlen, digest(i + inp), curses.A_REVERSE)
            j += 1
        del inp
        stdscr.refresh()

        while True:
            c = stdscr.getch()
            if c == ord('q'):
                break

        curses.nocbreak()
        curses.echo()
        curses.endwin()
    else:
        for i in labels:
            print "%25s %s" % (i, digest(i + inp))

def digest(message):
    '''Create and return secure hash of message

    A secure hash/message digest formed by hashing the `message` with
    the sha512 algorithm, encoding this hash with base64 and stripping
    it down to the first 30 characters.

    :Parameters:
        - `message`: The string from which to form the digest

    :Return:
        - The secure hash of `message`
    '''
    d = hashlib.sha512()
    d.update(message)
    shastr = d.hexdigest()

    # replace + and / with 4 and 9 respectively
    r = base64.b64encode(shastr, '49')
    r = r.replace('=','') # remove '=' if it's there
    r = r[:30]
    return str(r)

def usage():
    if os.name == 'nt':
        print "%s(nt) - http://dispass.babab.nl/" % versionStr
        print
        print 'When DisPass is started without arguments, the graphical'
        print 'version will be started. To use the command line,'
        print 'submit one or more labels.'
        print
        print 'USAGE: dispass [options] [label] [label2] [label3] [...]'
        print
        print 'Options:'
        print '-c, --create    use if this passphrase is new (check input PW)'
        print '-h, --help      show this help and exit'
        print '-V, --version   show full version information and exit'
    else:
        print "%s(%s) - http://dispass.babab.nl/" % (versionStr, os.name)
        print
        print "When DisPass is executed as 'gdispass' or 'dispass -g',"
        print 'the graphical version will be started.'
        print
        print 'USAGE: dispass [-co] label [label2] [label3] [...]'
        print '       dispass -g | -h | -V'
        print '       gdispass'
        print
        print 'Options:'
        print '-c, --create    use if this passphrase is new (check input PW)'
        print '-g, --gui       start guided graphical version of DisPass'
        print '-h, --help      show this help and exit'
        print '-o, --output    output passphrases to stdout (instead of the '
        print '                more secure way of displaying via curses)'
        print '-V, --version   show full version information and exit'

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "cghoV",
                ["create", "gui", "help", "output", "version"])
    except getopt.GetoptError, err:
        print str(err), "\n"
        usage()
        sys.exit(2)

    if args:
        labels = args
    else:
        labels = False

    pwTypoCheck = False
    for o, a in opts:
        if o in ("-g", "--gui"):
            GUI()
            return
        elif o in ("-c", "--create"):
            pwTypoCheck = True
        elif o in ("-o", "--output"):
            settings.useCurses = False
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-V", "--version"):
            print versionStr, '-', __version_info__, 'running on', os.name
            sys.exit()
        else:
            assert False, "unhandled option"

    if labels:
        CLI(labels, pwTypoCheck, settings.useCurses)
    else:
        if os.name == 'nt':
            usage()
            print '-' * 78
            print 'Starting GUI...'
            GUI()
        else:
            usage()

if __name__ == '__main__':
    main(sys.argv)
