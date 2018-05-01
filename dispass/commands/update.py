'''Subcommand module `add`; contains only a single class `Command`'''

# Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2018  Benjamin Althues <benjamin@babab.nl>
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
from dispass.commands.decorators import write_labels


@write_labels
class Command(CommandBase):
    '''Update the information relating to a label'''

    usagestr = (
        'usage: dispass update [-n] [-s] <label> '
        '[<size>]:[<algorithm>]:[<sequence_number>]\n'
        '       dispass update [-h]'
    )

    description = (
        'Update information for a label'
    )

    optionList = (
        ('help',    ('h', False, 'show this help information')),
        ('silent',  ('s', False, 'do not print success message')),
    )

    def run(self, lf):
        '''Parse the arguments and update them using `FileHandler.update`.'''

        if not len(self.args) == 2 or self.flags['help']:
            print(self.usage)
            return

        labelname = self.args[0]

        try:
            tmp_length, tmp_algo, tmp_seqno = self.args[1].split(':')
        except ValueError:
            print('Invalid update specification: {}'.format(self.args[1]))
            return 2

        try:
            length = int(tmp_length) if tmp_length else None
        except ValueError:
            length = None

        if tmp_algo and tmp_algo in algos.algorithms:
            algo = tmp_algo
        else:
            algo = None

        seqno = None
        if algo != 'dispass1':
            try:
                seqno = tmp_seqno if tmp_seqno else None
            except ValueError:
                pass

        if lf.update(labelname, length=length, algo=algo, seqno=seqno):
            if not self.flags['silent']:
                print("Label '{name}' updated".format(name=labelname))
        else:
            if not self.flags['silent']:
                print("Label '{name}' could not be updated"
                      .format(name=labelname))
