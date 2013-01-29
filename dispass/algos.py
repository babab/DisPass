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

import base64
import hashlib

algorithms = ('dispass1', 'dispass2')


class Dispass1:
    '''Dispass1 algorithm

    Tests:

    >>> dispass1 = Dispass1()
    >>> dispass1.digest('test', 'qqqqqqqq')
    'Y2Y4Y2Y0Yzg5Nzc1Yzc2MmI4OTU0ND'
    >>> dispass1.digestPasswordDict({'test': (30, None)}, 'qqqqqqqq')
    [('test', 'Y2Y4Y2Y0Yzg5Nzc1Yzc2MmI4OTU0ND')]
    >>> dispass1.digest('test2', 'qqqqqqqq', 50)
    'NmQzNjUzZTlhNTc4NWFlNTU5ZTVkZGQ5ZTc2NzliZjgzZDQ1Zj'
    >>> dispass1.digestPasswordDict({'test2': (50, )}, 'qqqqqqqq')
    [('test2', 'NmQzNjUzZTlhNTc4NWFlNTU5ZTVkZGQ5ZTc2NzliZjgzZDQ1Zj')]
    '''

    @staticmethod
    def digest(label, password, length=30, seqno=None):
        '''Create and return secure hash of message

        A secure hash/message digest formed by hashing a string (formed by
        concatenating label+password) with the sha512 algorithm, encoding
        this hash with base64 and stripping it down to the first `length`
        characters.

        :Parameters:
            - `label`: String. Labelname
            - `password`: String. The input password
            - `length`: Length of output hash (optional)
            - `seqno`: Sequence number. Not used in Dispass1

        :Return:
            - The secure hash of `label` + `password`
        '''

        sha = hashlib.sha512()
        sha.update(str(label) + str(password))
        r = base64.b64encode(sha.hexdigest(), '49').replace('=', '')

        return str(r[:length])

    @staticmethod
    def digestPasswordDict(indentifierDict, password):
        '''Creat secure hashes of a dict of `{identifier:(length, )}`

        A secure hash/message digest formed by hashing the `message` with
        the sha512 algorithm, encoding this hash with base64 and stripping
        it down to the first `length` characters.

        :Parameters:
            - `indentifierDict`: A dict of `{identifier: (length, None)}`
            - `password`: The password to use for hashing entries

        :Return:
            - A list of '(identifier: (length, seqno)), passphrase)' entries
        '''

        hashed = []

        for identifier, params in indentifierDict.iteritems():
            sha = hashlib.sha512()
            sha.update(identifier + password)
            r = base64.b64encode(sha.hexdigest(), '49').replace('=', '')
            hashed.append((identifier, str(r[:params[0]])))

        return hashed


class Dispass2:
    '''Dispass2 algorithm

    Tests:

    >>> dispass2 = Dispass2()
    >>> dispass2.digest('test', 'qqqqqqqq')
    'ZTdiNGNkYmQ2ZjFmNzc3NGFjZWEwMz'
    >>> dispass2.digestPasswordDict({'test': (30, 1)}, 'qqqqqqqq')
    [('test', 'ZTdiNGNkYmQ2ZjFmNzc3NGFjZWEwMz')]
    >>> dispass2.digest('test2', 'qqqqqqqq', 50, 10)
    'NGEwNjMxMzZiMzljODVmODk4OWQ1ZmE4YTRlY2E4ODZkZjZlZW'
    >>> dispass2.digestPasswordDict({'test2': (50, 10)}, 'qqqqqqqq')
    [('test2', 'NGEwNjMxMzZiMzljODVmODk4OWQ1ZmE4YTRlY2E4ODZkZjZlZW')]
    '''

    @staticmethod
    def digest(label, password, length=30, seqno=1):
        '''Create and return secure hash of message

        A secure hash/message digest formed by hashing a string (formed by
        concatenating label+seqno+password) with the sha512 algorithm, encoding
        this hash with base64 and stripping it down to the first `length`
        characters.

        :Parameters:
            - `label`: String. Labelname
            - `password`: String. The input password
            - `length`: Length of output hash (optional)
            - `seqno`: Integer. Sequence number.

        :Return:
            - The secure hash of `label` + `seqno` + `password`
        '''

        sha = hashlib.sha512()
        sha.update(str(label) + str(seqno) + str(password))
        r = base64.b64encode(sha.hexdigest(), '49').replace('=', '')

        return str(r[:length])

    @staticmethod
    def digestPasswordDict(indentifierDict, password):
        '''Creat secure hashes of a dict of `{identifier:(length, seqno)}`

        A secure hash/message digest formed by hashing the `message` with
        the sha512 algorithm, encoding this hash with base64 and stripping
        it down to the first `length` characters.

        :Parameters:
            - `indentifierDict`: A dict of `{identifier: (length, seqno)}`
            - `password`: The password to use for hashing entries

        :Return:
            - A list of '(identifier: (length, seqno)), passphrase)' entries
        '''

        hashed = []

        for identifier, params in indentifierDict.iteritems():
            sha = hashlib.sha512()
            sha.update(identifier + str(params[1]) + password)
            r = base64.b64encode(sha.hexdigest(), '49').replace('=', '')
            hashed.append((identifier, str(r[:params[0]])))

        return hashed

if __name__ == '__main__':
    import doctest
    doctest.testmod()
