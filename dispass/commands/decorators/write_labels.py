'''Decorator for commands that write labels'''

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

from dispass.dispass import settings
from dispass.filehandler import Filehandler


def _run_with_labelfile(func):
    def run(inst, *args, **kwargs):
        if inst.parentFlags['file']:
            lf = Filehandler(settings, file_location=inst.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not lf.file_found:
            if not lf.promptForCreation(silent=inst.flags['silent']):
                return 1

        if not lf.is_writeable():
            print('error: can\'t save to "{loc}", not writeable'
                  .format(loc=lf.file_location))
            return 1

        func(inst, lf, *args, **kwargs)

        if not inst.flags['dry-run']:
            lf.save()

    return run


def write_labels(cls):
    '''Decorate the `run` method of CLS.

    An instance of dispass.labelfile.Filehandler is added to the front
    of the argument list of the `run` method, after self. This file is
    ready for writing. After the `run` method is finished, the label
    file is automatically saved. A `dry-run` flag is also added to the
    command indicating that the labelfile should not actually be
    saved.

    '''
    cls.run = _run_with_labelfile(cls.run)
    cls.optionList += (
        ('dry-run', ('n', False, 'do not actually add label to labelfile')),
    )

    return cls
