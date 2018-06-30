from execute_selenium import WebClicker
from split import add_https_to_url
from split import parse_command


class Cmd(object):
    NONAME = 'noname'
    COMMAND = 'command'
    QUIT = 'quit'
    EXIT = 'exit'
    URL = 'url'
    FILE = 'file'

class CmdProcessor:
    def __init__(self):
        self.driver_exe_path = None
        self.browser = None
        self.profile_path = None
        self.browser_binary = None
        self.webclicker = None

        self.start_config()

    def command_list(self):
        all_methods = [func for func in dir(self) if callable(getattr(self, func))]
        return [name[:-4] for name in all_methods if name[-4:] == "_cmd"]

    def call(self, command_dict):
        try:
            getattr(self, command_dict[Cmd.COMMAND] + '_cmd', self.called_unknown)(command_dict)
        except Exception as e:
            print('Error!')
            print(e)
        return


    def called_unknown(self, command_dict):
        print('Unknown command: {0}'.format(command_dict[Cmd.COMMAND]))
        return

    def start_cmd(self, command_dict):
        self.webclicker = WebClicker(self.driver_exe_path,
                                     browser=self.browser,
                                     profile_path=self.profile_path,
                                     browser_binary=self.browser_binary)
        if Cmd.URL in command_dict:
            url = command_dict[Cmd.URL]
        elif Cmd.NONAME in command_dict:
            url = command_dict[Cmd.NONAME]
        else:
            print("No URL provided!")
            return

        self.webclicker.webdriver.get(add_https_to_url(url))

    def run_cmd(self, command_dict):
        with open(command_dict[Cmd.FILE]) as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines]
        for line in lines:
            print(line)
            command = parse_command(line)
            self.call(command)

    def shutdown_cmd(self, command_dict):
        self.webclicker.webdriver.stop_client()
        self.webclicker.webdriver.close()

    def set_cmd(self, command_dict):
        if 'driver_exe_path' in command_dict:
            self.driver_exe_path = command_dict['driver_exe_path']
            print("**{0}**".format(self.driver_exe_path))
        if 'browser' in command_dict:
            self.browser = command_dict['browser']
            print("**{0}**".format(self.browser))
        if 'profile_path' in command_dict:
            self.profile_path = command_dict['profile_path']
            print("**{0}**".format(self.profile_path))
        if 'browser_binary' in command_dict:
            self.browser_binary = command_dict['browser_binary']
            print("**{0}**".format(self.browser_binary))

    def start_config(self):
        self.run_cmd({Cmd.COMMAND: 'setup', Cmd.FILE: 'config.txt'})

