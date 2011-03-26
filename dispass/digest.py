# vim: set et ts=4 sw=4 sts=4:

'''Create a message digest'''

# Copyright (c) 2011 Benjamin Althues <benjamin@babab.nl>
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

__docformat__ = 'restructuredtext'
__version__ = '0.1.0-dev'

import base64
import hashlib
import re

def create(message):
    '''Create and return secure hash of message
    
    A secure hash/message digest formed by hashing the `message` with
    the sha512 algorithm, encoding this hash with base64 and stripping 
    it down to the first 30 characters.

    :Parameters:
        - `message`: The string from which to form the digest

    :Return:
        - The secure hash of `message`
    '''
    d = hashlib.sha512()
    d.update(message)
    shastr = d.hexdigest()

    # replace + and / with 4 and 9 respectively
    r = base64.b64encode(shastr, '49')
    r = r.replace('=','') # remove '=' if it's there
    r = r[:30]
    return str(r)
