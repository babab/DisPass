'''Subcommand module `generate`; contains only a single class `Command`'''

# Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2016  Benjamin Althues <benjamin@althu.es>
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

from pycommand import CommandBase

from dispass.algos import algorithms
from dispass.cli import CLI
from dispass.dispass import settings
from dispass.filehandler import Filehandler


class Command(CommandBase):
    '''Generate passphrases for one or more labels'''

    usagestr = (
        'usage: dispass generate [options] <label> [<label2>] [<label3>] [...]'
    )
    description = (
        'Generate passphrases for one or more labels\n\n'
        "Use the '-v' flag to ask for password twice to avoid typing errors"
    )
    optionList = (
        ('help',    ('h', False, 'show this help information')),
        ('verify',  ('v', False, 'verify password')),
        ('length',  ('l', '<length>', 'length of passphrase')),
        ('algo',    ('a', '<algorithm>', 'algorithm to use for generation')),
        ('seqno',   ('s', '<seqno>', 'sequence number to use for generation')),
        ('password', ('p', '<password>', 'password to use for generation')),
        ('stdout',  ('o', False, 'output passphrase(s) directly to stdout')),
        ('silent',  ('', False, 'do not show a prompt when errors occur')),
    )

    def run(self):
        '''Parse the various arguments and output passphrases for each label

        Each positional argument is a label. For each label, it will try to
        find (via `FileHandler.labletup`) if it is in the labelfile so other
        settings for the label can be applied. If it is not found, the default
        settings object defined as `dispass.dispass.settings` will be used. The
        parameters can be overridden through the various optargs.
        '''
        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            if not lf.promptForCreation(silent=self.flags['silent']):
                return 1

        if not self.args or self.flags['help']:
            print(self.usage)
            return 1

        algo = None
        length = None
        seqno = None

        if self.flags['algo']:
            if self.flags['algo'] in algorithms:
                algo = self.flags['algo']
        if self.flags['length']:
            try:
                length = int(self.flags['length'])
            except ValueError:
                print('Error: length argument must be a number')
                return 1
        if self.flags['seqno']:
            seqno = self.flags['seqno']

        console = CLI(lf)
        console.verifyPassword = self.flags['verify']

        if self.flags['password']:
            password = self.flags['password']
        else:
            password = console.passwordPrompt()

        for arg in self.args:
            labeltup = lf.labeltup(arg)
            if labeltup:
                console.generate(password, (arg, length or labeltup[1],
                                            algo or labeltup[2],
                                            seqno or labeltup[3],
                                            False))
            else:
                console.generate(password, (
                    arg, length or settings.passphrase_length,
                    algo or settings.algorithm,
                    seqno or settings.sequence_number,
                    False))
        del password

        if self.flags['stdout']:
            console.useCurses = False
            console.scriptableIO = True

        if not console.output():
            print('Error: could not generate keys')
            return 1
        else:
            return 0
