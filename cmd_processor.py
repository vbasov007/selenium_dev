from execute_selenium import WebClicker
from split import add_https_to_url, line_split

# from pprint import pprint

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

        self.webclicker.get_website(url)

    def run_cmd(self, command_dict):
        with open(command_dict[Cmd.FILE]) as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines]
        for line in lines:
            print(line)
            command = parse_command(line)
            self.call(command)

    def shutdown_cmd(self, command_dict=None):
        self.webclicker.shutdown()

    def set_cmd(self, command_dict):
        if 'driver_exe_path' in command_dict:
            self.driver_exe_path = command_dict['driver_exe_path']
        if 'browser' in command_dict:
            self.browser = command_dict['browser']
        if 'profile_path' in command_dict:
            self.profile_path = command_dict['profile_path']
        if 'browser_binary' in command_dict:
            self.browser_binary = command_dict['browser_binary']

    def find_elements_cmd(self, command_dict):
        name = command_dict['name_']
        value = command_dict[name]
        elements = self.webclicker.find_elements(name, value)
        print_web_elements(elements)

    def start_config(self):
        self.run_cmd({Cmd.COMMAND: 'setup', Cmd.FILE: 'config.txt'})

    def switch_to_frame_cmd(self, command_dict):
        name = command_dict['name_']
        value = command_dict[name]
        self.webclicker.switch_to_frame(name, value)

    def wait_cmd(self, command_dict):
        if 'time' in command_dict:
            time_sec = int(command_dict['time'])
        else:
            time_sec = 1
        if 'name_' not in command_dict:
            self.webclicker.sleep(time_sec)
        else:
            how = command_dict['name_']
            value = command_dict[how]
            self.webclicker.wait_element(how, value, time_sec)

    def click_cmd(self, command_dict):
        name = command_dict['name_']
        value = command_dict[name]
        self.webclicker.click(name, value)

    def clear_cmd(self, command_dict):
        name = command_dict['name_']
        value = command_dict[name]
        self.webclicker.clear(name, value)

    def sendkeys_cmd(self, command_dict):
        name = command_dict['name_']
        value = command_dict[name]
        if 'string' in command_dict:
            string = command_dict['string']
        else:
            string = ''

        self.webclicker.send_keys(name, value, string)


def print_web_elements(elements):
    print('{0} elements'.format(len(elements)))
    for elem in elements:
        # e = dir(elem)
        # pprint(e)
        print('id={0}'.format(elem.id))
        print('is_displayed={0}'.format(elem.is_displayed()))
        print('is_enabled={0}'.format(elem.is_enabled()))
        print('is_selected={0}'.format(elem.is_selected()))
        print('tag_name={0}'.format(elem.tag_name))
        print('text={0}'.format(elem.text))


def parse_command(command_str: str, possible_commands=(), possible_options=()) -> dict:

    cmd_dict = dict()

    cmd_list = line_split(command_str)

    if len(possible_commands) > 0:
        if cmd_list[0] in possible_commands:
            cmd_dict.update({'command': cmd_list[0]})
    else:
        cmd_dict.update({'command': cmd_list[0]})

    for s in cmd_list[1:]:
        name, value = parse_option(s)
        if not name == 'time' and not name == 'string':
            cmd_dict.update({'name_': name})
        if len(possible_options):
            if name in possible_options:
                cmd_dict.update({name: value})
        else:
            cmd_dict.update({name: value})

    return cmd_dict


def parse_option(target):
    res = target.split("=", 1)
    res = [a.strip(' "\'') for a in res]

    if not res:
        return '',''

    if len(res) < 2:
        value = res[0]
        name = 'noname'
    else:
        name = res[0].strip()
        value = res[1].strip()

    return name, value
