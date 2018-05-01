'''Decorator for commands that read labels'''

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

from dispass.dispass import settings
from dispass.filehandler import Filehandler


def _run_with_labelfile(func, optional):
    def run(inst, *args, **kwargs):
        if inst.parentFlags['file']:
            lf = Filehandler(settings, file_location=inst.parentFlags['file'])
        else:
            lf = Filehandler(settings)

        if not inst.flags['help']:
            if not lf.file_found and not optional:
                print('error: could not load labelfile at "{loc}"'
                      .format(loc=lf.file_location))
                return 1

        func(inst, lf, *args, **kwargs)

    return run


def read_labels(optional=False):
    '''Decorate the `run` method of CLS.

    An instance of dispass.labelfile.Filehandler is added to the front
    of the argument list of the `run` method, after self. This file is
    ready for reading.

    '''
    def func(cls):
        cls.run = _run_with_labelfile(cls.run, optional)
        return cls

    return func
