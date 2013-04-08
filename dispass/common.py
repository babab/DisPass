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


class CommandBase(object):
    '''Base class for (sub)commands'''

    usagestr = 'usage: dispass subcommand [options]'
    '''String. Usage synopsis'''

    description = ''
    '''String. Small description of subcommand'''

    optionList = {}
    '''Dictionary of options (as list of 2-tuples).
    This will be transformed to an OrderedDict when initializing the object.

    Example::

        optionList = (
            ('help', ('h', False, 'show this help information')),
            ('dry-run', ('n', False,
                         'only print output without actually running')),

            # To specify that an option requires an argument
            # just add a string that describes it
            ('file', ('f', '<filename>', 'use specified file')),

            # Use an empty string to ommit short option
            ('debug', ('', False, 'show debug information')),
        )

    '''

    usageTextExtra = ''
    '''String. Optional extra usage information'''

    def __init__(self, settings, argv):
        '''Initialize (sub)command object

        :Parameters:
            - `settings`: Instance of `dispass.dispass.Settings`
            - `argv`: List of arguments. E.g. `sys.argv[1:]`
        '''

        # Instance vars
        self.error = None
        '''Thrown by GetoptError when parsing illegal arguments.'''

        self.flags = {}
        '''Dict of parsed options and corresponding arguments, if any.'''

        self.parentFlags = {}
        '''Dict of registered `flags` of parent Command object.'''

        self.usage = ''
        '''String with usage information

        The string is compiled using the values found for
        `usagestr`, `description`, `optionList` and `usageTextExtra`.
        '''

        self.optionList = OrderedDict(self.optionList)
        self.settings = settings

        # Local vars
        longopts = []
        shortopts = ''

        # Create usage information and build dict of possible flags
        opthelp = ''
        for flag, val in self.optionList.iteritems():
            spec = flag + '=' if val[1] else flag
            longopts.append(spec)
            self.flags.update({flag: None})

            if val[1]:
                flagstring = ('{flag}={argument}'
                              .format(flag=flag, argument=val[1]))
            else:
                flagstring = flag

            if val[0]:
                shortopts += val[0] + ':' if val[1] else val[0]
                opthelp += ('-{short}, --{flag:17} {desc}\n'
                            .format(short=val[0], flag=flagstring,
                                    desc=val[2]))
            else:
                opthelp += ('--{flag:21} {desc}\n'
                            .format(flag=flag, desc=val[2]))

        self.usage = self.usagestr
        if self.description:
            self.usage += '\n\n{desc}'.format(desc=self.description)
        if self.optionList:
            self.usage += '\n\nOptions:\n{opts}'.format(opts=opthelp)
        if self.usageTextExtra:
            self.usage += '\n{help}'.format(help=self.usageTextExtra)

        # Parse arguments and options
        try:
            opts, self.args = getopt.getopt(argv, shortopts, longopts)
        except getopt.GetoptError, err:
            self.error = err
            return  # Stop when an invalid option is parsed

        for opt in opts:
            # Compare each option with optionList
            for flag, val in self.optionList.iteritems():
                if opt[0][1] != '-':
                    # Short tags
                    if opt[0][1] == val[0]:
                        if val[1]:
                            self.flags[flag] = opt[1]
                        else:
                            self.flags[flag] = True
                else:
                    # Long tags
                    if opt[0][2:] == flag:
                        if val[1]:
                            self.flags[flag] = opt[1]
                        else:
                            self.flags[flag] = True

    def registerParentFlag(self, optionName, value):
        '''Register a flag of a parent command

        :Parameters:
            - `optionName`: String. Name of option
            - `value`: Mixed. Value of parsed flag`
        '''
        self.parentFlags.update({optionName: value})
        return self
