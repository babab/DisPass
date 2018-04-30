'''Tests for algorithms'''

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

import dispass.algos


def test_algos_Dispass1_default():
    '''algos: Dispass1 digest returns the correct passphrase'''
    passphrase = dispass.algos.Dispass1.digest('test', 'qqqqqqqq')
    assert passphrase == 'Y2Y4Y2Y0Yzg5Nzc1Yzc2MmI4OTU0ND'
    passphrase = dispass.algos.Dispass1.digest('test', 'abc#@123ZXY')
    assert passphrase == 'OGY5NjgxZGI4Yjk2ZDlhNTk1ZDU3Nz'


def test_algos_Dispass1_length50():
    '''algos: Dispass1 digest returns the passphrase with a length of 50'''
    passphrase = dispass.algos.Dispass1.digest('test2', 'qqqqqqqq', 50)
    assert passphrase == 'NmQzNjUzZTlhNTc4NWFlNTU5ZTVkZGQ5ZTc2NzliZjgzZDQ1Zj'
    passphrase = dispass.algos.Dispass1.digest('test2', 'abc#@123ZXY', 50)
    assert passphrase == 'ZmVjMjgwYjdjZmY2ZWJkMTYwZDM2OGQyZTFiOWIzMThjNzhjOD'


def test_algos_Dispass2_default():
    '''algos: Dispass2 digest returns the correct passphrase'''
    passphrase = dispass.algos.Dispass2.digest('test', 'qqqqqqqq')
    assert passphrase == 'ZTdiNGNkYmQ2ZjFmNzc3NGFjZWEwMz'
    passphrase = dispass.algos.Dispass2.digest('test', 'abc#@123ZXY')
    assert passphrase == 'ZjdiODhhOWQyZTc3MzM4ZGFjNmM5OW'


def test_algos_Dispass2_length50():
    '''algos: Dispass2 digest returns the passphrase with a length of 50'''
    passphrase = dispass.algos.Dispass2.digest('test2', 'qqqqqqqq', 50, 1)
    assert passphrase == 'YjFjMzlhZDA3ZmFhNjg4MThlNDFmM2IxYTk0NWJiMjEyYzdlMT'
    passphrase = dispass.algos.Dispass2.digest('test', 'abc#@123ZXY', 50, 1)
    assert passphrase == 'ZjdiODhhOWQyZTc3MzM4ZGFjNmM5OWQwMjJlMzZiZWI5ODRhNG'


def test_algos_Dispass2_seqno10():
    '''algos: Dispass2 digest returns the passphrase with a seqno of 10'''
    passphrase = dispass.algos.Dispass2.digest('test2', 'qqqqqqqq', 50, 10)
    assert passphrase == 'NGEwNjMxMzZiMzljODVmODk4OWQ1ZmE4YTRlY2E4ODZkZjZlZW'
    passphrase = dispass.algos.Dispass2.digest('test', 'abc#@123ZXY', 50, 10)
    assert passphrase == 'ODNmNmE5MjE4OGYzM2I1YmExNzI1M2E1Zjc2ZGFjN2I0ZDc5N2'


def test_algos_algoObject_dispass1():
    '''algos: algoObject can return a valid Dispass1 digest staticmethod'''
    a = dispass.algos.algoObject('dispass1')
    assert hasattr(a, 'digest')


def test_algos_algoObject_dispass2():
    '''algos: algoObject can return a valid Dispass2 digest staticmethod'''
    a = dispass.algos.algoObject('dispass2')
    assert hasattr(a, 'digest')
