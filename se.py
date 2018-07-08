
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from prompt_toolkit.validation import Validator, ValidationError

from prompt_toolkit.completion import Completer, Completion

from cmd_processor import CmdProcessor, parse_command
from cmd_processor import Cmd

from cmd_processor import completer
from command_options import command_options


class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        completion, position = completer(document.text, command_options, [*command_options])
        for word in completion:
            yield Completion(word, start_position=position)


cmd_proc = CmdProcessor()
# SECompleter = WordCompleter(cmd_proc.command_list(), ignore_case=True)

session = PromptSession(
    '>>>>',
    history=FileHistory('history.txt'),
    auto_suggest=AutoSuggestFromHistory(),
    completer=MyCustomCompleter())


while 1:
    user_input = session.prompt()

    command = parse_command(user_input)
    if command[Cmd.COMMAND] == Cmd.QUIT or command[Cmd.COMMAND] == Cmd.EXIT:
        cmd_proc.shutdown_cmd()
        break

    cmd_proc.call(parse_command(user_input))

