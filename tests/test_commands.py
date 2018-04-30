'''Tests for running commands'''

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

from helpers import cmd_output_startswith

from dispass.dispass import DispassCommand


def test_main_command_no_arguments():
    '''commands: without arguments returns exit status 2'''
    cmd = DispassCommand([])
    assert cmd.run() == 2


def test_main_command_version_info():
    '''commands: get version info via all possible combinations'''
    usage_string = "DisPass 0.3.0 (0, 3, 0, 'final', 0)"

    cmd = DispassCommand(['-V'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['--version'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['version'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_main():
    '''commands: get help for main command via all possible combinations'''
    usage_string = 'usage: dispass [options] <command> [<args>]'
    cmd = DispassCommand([])
    assert cmd.usage.startswith(usage_string)
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help'])
    assert cmd_output_startswith(cmd, usage_string)
