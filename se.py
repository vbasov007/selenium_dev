
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
# from prompt_toolkit.contrib.completers import WordCompleter
from cmd_processor import CmdProcessor, parse_command
from cmd_processor import Cmd

cmd_proc = CmdProcessor()
# SECompleter = WordCompleter(cmd_proc.command_list(), ignore_case=True)

while 1:
    user_input = prompt('SE>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        # completer=SECompleter,
                        )

    command = parse_command(user_input)
    if command[Cmd.COMMAND] == Cmd.QUIT or command[Cmd.COMMAND] == Cmd.EXIT:
        cmd_proc.shutdown_cmd()
        break

    cmd_proc.call(parse_command(user_input))

