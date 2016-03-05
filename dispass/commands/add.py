'''Subcommand module `add`; contains only a single class `Command`'''

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

from dispass import algos
from dispass.dispass import settings
from dispass.cli import CLI
from dispass.filehandler import Filehandler
from dispass.interactive_editor import InteractiveEditor


class Command(CommandBase):
    '''Add a new label to the labelfile and generate passphrase.'''
    usagestr = (
        'usage: dispass add [-g] [-n] [-s] <labelspec> [<labelspec2>] [...]\n'
        '       dispass add [-i] [-g] [-h]'
    )
    description = (
        'Add a new label to the labelfile and generate passphrase.\n'
        'The labelspec looks like this:\n\n'
        '    label[:size[:algorithm[:sequence_number]]]'
    )
    optionList = (
        ('interactive', ('i', False, 'add label in an interactive manner')),
        ('generate', ('g', False,
                      'immediately generate passphrase after adding it')),
        ('help',    ('h', False, 'show this help information')),
        ('dry-run', ('n', False, 'do not actually add label to labelfile')),
        ('silent',  ('s', False, 'do not print success message')),
    )

    def run(self):
        '''Parse labels and add them using `FileHandler.add`.

        When the -i flag is passed, add them using `InteractiveEditor.add`
        '''

        newlabels = []
        '''A list of labelnames that have been added.'''

        if self.parentFlags['file']:
            lf = Filehandler(settings, file_location=self.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            if not lf.promptForCreation(silent=self.flags['silent']):
                return 1

        if self.flags['interactive']:
            intedit = InteractiveEditor(settings, lf, interactive=False)
            newlabels.append(intedit.add())
        else:
            if not self.args or self.flags['help']:
                print(self.usage)
                return

            for arg in set(self.args):
                labelspec = arg.split(':')
                params = len(labelspec)

                length = 0
                try:
                    length = params >= 2 and int(labelspec[1])
                except ValueError:
                    pass

                if not length:
                    length = settings.passphrase_length

                algo = params >= 3 and labelspec[2] or settings.algorithm
                if not algo in algos.algorithms:
                    algo = settings.algorithm

                seqno = 0
                if algo != 'dispass1':
                    try:
                        seqno = params >= 4 and int(labelspec[3])
                    except ValueError:
                        pass

                if not seqno:
                    seqno = settings.sequence_number

                if lf.add(labelname=labelspec[0], length=length, algo=algo,
                          seqno=seqno):
                    newlabels.append(labelspec[0])
                    if not self.flags['silent']:
                        print("Label '{name}' saved".format(name=labelspec[0]))
                else:
                    if not self.flags['silent']:
                        print("Label '{name}' already exists in labelfile"
                              .format(name=labelspec[0]))

            if not self.flags['dry-run']:
                lf.save()

        if self.flags['generate'] and newlabels:
            console = CLI(lf)
            console.verifyPassword = True
            password = console.passwordPrompt()

            for label in newlabels:
                console.generate(password, lf.labeltup(label))
            del password

            if not console.output():
                if not self.flags['silent']:
                    print('Error: could not generate passphrase')
                return 1
            else:
                return 0
