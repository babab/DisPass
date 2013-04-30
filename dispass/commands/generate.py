'''generate passphrases for one or more labels'''

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

from dispass.algos import algorithms
from dispass.cli import CLI
from dispass.common import CommandBase
from dispass.dispass import settings
from dispass.filehandler import Filehandler


class Command(CommandBase):
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
        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            if not lf.promptForCreation(silent=self.flags['silent']):
                return 1

        if not self.args or self.flags['help']:
            print self.usage
            return 1

        algo = self.settings.algorithm
        length = self.settings.passphrase_length
        seqno = self.settings.sequence_number

        override = False
        if self.flags['algo']:
            if self.flags['algo'] in algorithms:
                algo = self.flags['algo']
            override = True
        if self.flags['length']:
            try:
                length = int(self.flags['length'])
            except ValueError:
                print 'Error: length argument must be a number'
                return 1
            override = True
        if self.flags['seqno']:
            seqno = self.flags['seqno']
            override = True

        console = CLI(lf)
        console.verifyPassword = self.flags['verify']

        if self.flags['password']:
            password = self.flags['password']
        else:
            password = console.passwordPrompt()

        for arg in self.args:
            labeltup = lf.labeltup(arg)
            if labeltup and not override:
                console.generate(password, labeltup)
            else:
                console.generate(password, (arg, length, algo, seqno))
        del password

        if self.flags['stdout']:
            console.useCurses = False
            console.scriptableIO = True

        if not console.output():
            print('Error: could not generate keys')
            return 1
        else:
            return 0
