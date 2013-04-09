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

from dispass.cli import CLI
from dispass.common import CommandBase
from dispass.dispass import settings
from dispass.filehandler import Filehandler


class Command(CommandBase):
    usagestr = 'usage: dispass generate <label> [<label2>] [<label3>] [...]'
    description = 'Generate passphrases for one or more labels'
    optionList = (
        ('help',    ('h', False, 'show this help information')),
        ('silent',  ('s', False, 'do not show a prompt when errors occur')),
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
            return

        algo = self.settings.algorithm
        length = self.settings.passphrase_length
        seqno = self.settings.sequence_number

        console = CLI(lf)
        password = console.passwordPrompt()

        for arg in self.args:
            console.generate(password, (arg, length, algo, seqno))
        del password
        console.output()
