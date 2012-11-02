# Copyright (c) 2011-2012 Benjamin Althues <benjamin@babab.nl>
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


def digest(message, length=30):
    '''Create and return secure hash of message

    A secure hash/message digest formed by hashing the `message` with
    the sha512 algorithm, encoding this hash with base64 and stripping
    it down to the first `length` characters.

    :Parameters:
        - `message`: The string from which to form the digest
        - `length`: Length of output hash (optional)

    :Return:
        - The secure hash of `message`
    '''

    sha = hashlib.sha512()
    sha.update(message)
    r = base64.b64encode(sha.hexdigest(), '49').replace('=', '')

    return str(r[:length])


def digestPasswordDict(indentifierDict, password):
    '''Creat secure hashes of a dict of `identifier:length` and a password

    A secure hash/message digest formed by hashing the `message` with
    the sha512 algorithm, encoding this hash with base64 and stripping
    it down to the first `length` characters.

    :Parameters:
        - `indentifierDict`: A dict of `{identifier: length,}` entries
        - `password`: The password to use for hashing entries

    :Return:
        - A list of 2-tuples of '(identifier, passphrase)'
    '''

    hashed = []

    for identifier, length in indentifierDict.iteritems():
        sha = hashlib.sha512()
        sha.update(identifier + password)
        r = base64.b64encode(sha.hexdigest(), '49').replace('=', '')
        hashed.append((identifier, str(r[:length])))

    return hashed
