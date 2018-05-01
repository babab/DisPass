'''Tests for running commands'''

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


def test_help_for_command_add():
    '''commands: get help for add command via all possible combinations'''
    usage_string = (
        'usage: dispass add [-g] [-n] [-s] <labelspec> [<labelspec2>] [...]\n'
        '       dispass add [-i] [-g] [-h]'
    )

    cmd = DispassCommand(['add', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['add', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'add'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_disable():
    '''commands: get help for disable command via all possible combinations'''
    usage_string = 'usage: dispass disable <label>'

    cmd = DispassCommand(['disable', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['disable', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'disable'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_enable():
    '''commands: get help for enable command via all possible combinations'''
    usage_string = 'usage: dispass enable <label>'

    cmd = DispassCommand(['enable', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['enable', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'enable'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_generate():
    '''commands: get help for generate command via all possible combinations'''
    usage_string = (
        'usage: dispass generate [options] <label> '
        '[<label2>] [<label3>] [...]'
    )

    cmd = DispassCommand(['generate', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['generate', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'generate'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_gui():
    '''commands: get help for gui command via all possible combinations'''
    usage_string = 'usage: dispass gui [-h]'

    cmd = DispassCommand(['gui', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['gui', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'gui'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_help():
    '''commands: get help for help command'''
    cmd = DispassCommand(['help', 'help'])
    assert cmd_output_startswith(cmd, 'usage: dispass help [<command>]')


def test_help_for_command_increment():
    '''commands: get help for increment command via all combinations'''
    usage_string = (
        'usage: dispass increment [-n] [-s] <label>\n'
        '       dispass increment [-h]'
    )

    cmd = DispassCommand(['increment', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['increment', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'increment'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_list():
    '''commands: get help for list command via all combinations'''
    usage_string = 'usage: dispass list [-h] [-n] [--script]'

    cmd = DispassCommand(['list', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['list', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'list'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_remove():
    '''commands: get help for remove command via all combinations'''
    usage_string = (
        'usage: dispass remove [-n] [-s] <labelname> [<labelname2>] [...]\n'
        '       dispass remove [-i] [-h]'
    )

    cmd = DispassCommand(['remove', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['remove', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'remove'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_update():
    '''commands: get help for update command via all combinations'''
    usage_string = (
        'usage: dispass update [-n] [-s] <label> '
        '[<size>]:[<algorithm>]:[<sequence_number>]\n'
        '       dispass update [-h]'
    )

    cmd = DispassCommand(['update', '-h'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['update', '--help'])
    assert cmd_output_startswith(cmd, usage_string)

    cmd = DispassCommand(['help', 'update'])
    assert cmd_output_startswith(cmd, usage_string)


def test_help_for_command_version():
    '''commands: get help for version command via all combinations'''
    cmd = DispassCommand(['help', 'version'])
    assert cmd_output_startswith(cmd, 'usage: dispass version')
