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

from collections import OrderedDict
import getopt


def stripargstring(string):
    return string.replace(':', '').replace('=', '')


class CommandBase(object):
    '''Base class for (sub)commands'''

    usagestr = 'usage: dispass subcommand [options]'
    '''String. Usage synopsis'''

    description = ''
    '''String. Small description of subcommand'''

    optionList = {}
    '''Dictionary of options

    Example::

        optionList = {
            'help': ('h', 'show this help information'),
            'dry-run': ('n', 'only print output without actually running'),
            'file=': ('f:', 'use specified file'),
            'debug': (None, 'show debug information'),
        }

    '''

    usageTextExtra = ''
    '''String. Optional extra usage information'''

    def __init__(self, settings, argv):
        self.argv = argv
        self.error = None
        self.longopts = []
        self.settings = settings
        self.shortopts = ''
        self.usage = ''

        # Create usage information
        opthelp = ''
        self.optionList = OrderedDict(sorted(self.optionList.items()))
        for flag, val in self.optionList.iteritems():
            self.longopts.append(flag)
            if val[0]:
                self.shortopts += val[0]
                opthelp += ('-{short}, --{flag:15} {desc}\n'
                            .format(short=stripargstring(val[0]),
                                    flag=stripargstring(flag), desc=val[1]))
            else:
                opthelp += ('--{flag:19} {desc}\n'
                            .format(flag=stripargstring(flag), desc=val[1]))

        self.usage = self.usagestr
        if self.description:
            self.usage += '\n\n{desc}'.format(desc=self.description)
        if self.optionList:
            self.usage += '\n\nOptions:\n{opts}'.format(opts=opthelp)
        if self.usageTextExtra:
            self.usage += '\n\n{help}'.format(help=self.usageTextExtra)

        # Parse arguments and options
        try:
            self.opts, self.args = getopt.getopt(self.argv, self.shortopts,
                                                 self.longopts)
        except getopt.GetoptError, err:
            self.error = err
