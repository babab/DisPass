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


from nose.tools import eq_

import dispass.algos


def test_algos_Dispass1_default():
    '''algos: Dispass1 digest returns the correct passphrase'''
    passphrase = dispass.algos.Dispass1.digest('test', 'qqqqqqqq')
    eq_(passphrase, 'Y2Y4Y2Y0Yzg5Nzc1Yzc2MmI4OTU0ND')


def test_algos_Dispass1_length50():
    '''algos: Dispass1 digest returns the passphrase with a length of 50'''
    passphrase = dispass.algos.Dispass1.digest('test2', 'qqqqqqqq', 50)
    eq_(passphrase, 'NmQzNjUzZTlhNTc4NWFlNTU5ZTVkZGQ5ZTc2NzliZjgzZDQ1Zj')


def test_algos_Dispass2_default():
    '''algos: Dispass2 digest returns the correct passphrase'''
    passphrase = dispass.algos.Dispass2.digest('test', 'qqqqqqqq')
    eq_(passphrase, 'ZTdiNGNkYmQ2ZjFmNzc3NGFjZWEwMz')


def test_algos_Dispass2_length50():
    '''algos: Dispass2 digest returns the passphrase with a length of 50'''
    passphrase = dispass.algos.Dispass2.digest('test2', 'qqqqqqqq', 50, 1)
    eq_(passphrase, 'YjFjMzlhZDA3ZmFhNjg4MThlNDFmM2IxYTk0NWJiMjEyYzdlMT')


def test_algos_Dispass2_seqno10():
    '''algos: Dispass2 digest returns the passphrase with a seqno of 10'''
    passphrase = dispass.algos.Dispass2.digest('test2', 'qqqqqqqq', 50, 10)
    eq_(passphrase, 'NGEwNjMxMzZiMzljODVmODk4OWQ1ZmE4YTRlY2E4ODZkZjZlZW')
