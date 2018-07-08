from execute_selenium import WebClicker
from execute_selenium import get_html_by_element
from selenium.webdriver.common.keys import Keys
import shlex
import re
from lxml import etree, html


def print_pretty_html(html_str):
    doc = html.fromstring(html_str)
    print(etree.tostring(doc, encoding='unicode', pretty_print=True))


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
        url = get_url(command_dict)
        if url:
            self.webclicker.get_website(url)
        else:
            print('No URL provided! Open empty page!')

    def run_cmd(self, command_dict):
        with open(command_dict[Cmd.FILE]) as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines]
        for line in lines:
            if len(line) > 0:
                if line[0] == '''#''':
                    continue
                print(line)
                command = parse_command(line)
                if command['command'] == 'stop_script':
                    print("Stop script!")
                    return
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
        name, value = get_locator(command_dict)
        elements = self.webclicker.find_elements(name, value)
        print_web_elements(elements)


    def start_config(self):
        self.run_cmd({Cmd.COMMAND: 'setup', Cmd.FILE: 'config.txt'})

    def switch_to_frame_cmd(self, command_dict):
        if 'index' in command_dict:
            index = int(command_dict['index'])
            self.webclicker.switch_to_frame_by_index(index)
        else:
            name, value = get_locator(command_dict)
            self.webclicker.switch_to_frame(name, value)

    def wait_cmd(self, command_dict):
        if 'time' in command_dict:
            time_sec = int(command_dict['time'])
        else:
            time_sec = 1

        how, value = get_locator(command_dict)
        if len(how) > 0 and len(value) > 0:
            self.webclicker.wait_element(how, value, time_sec)
        else:
            self.webclicker.sleep(time_sec)

    def click_cmd(self, command_dict):
        name, value = get_locator(command_dict)
        self.webclicker.click(name, value)

    def clear_cmd(self, command_dict):
        name, value = get_locator(command_dict)
        self.webclicker.clear(name, value)

    def sendkeys_cmd(self, command_dict):
        name, value = get_locator(command_dict)
        if 'string' in command_dict:
            string = command_dict['string']
        else:
            string = ''

        end = ''
        if '-enter' in command_dict:
            end = Keys.RETURN

        self.webclicker.send_string(name, value, string + end)

    def send_ctrl_key_cmd(self, command_dict):
        name, value = get_locator(command_dict)
        if 'key' in command_dict:
            self.webclicker.send_ctrl_key(name, value, command_dict['key'])


    def get_cmd(self, command_dict):
        url = get_url(command_dict)
        if url:
            self.webclicker.get_website(url)
        else:
            print("No URL provided!")

    def html_cmd(self, command_dict):
        name, value = get_locator(command_dict)

        if "-outer" in command_dict:
            html = self.webclicker.get_html(name, value, inner=False)
        else:
            html = self.webclicker.get_html(name, value, inner=True)

        print_pretty_html(html)

    def page_html_cmd(self, command_dict):
        print_pretty_html(self.webclicker.get_full_html())

    def switch_to_window_cmd(self, command_dict):
        if 'window_name' in command_dict:
            self.webclicker.switch_to_window(command_dict['window_name'])

    def get_attribute_cmd(self, command_dict):
        name, value = get_locator(command_dict)
        if "attr" in command_dict:
            print('Attribute {0} = {1}'.format(command_dict['attr'],
                                               self.webclicker.get_attribute(name, value, command_dict['attr'])))


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

        html = get_html_by_element(elem, inner=False)
        print_pretty_html(html)


def completer(command_str: str, options_dict, all_commands):

    if len(command_str) < 2:
        return all_commands, -len(command_str)

    words = shlex.split(command_str)

    if len(words) == 1 and command_str[-1] != ' ':
        return [w for w in all_commands if re.match(words[0], w)], -len(words[0])

    if len(words) >= 1 and command_str[-1] == ' ':
        if words[0] in options_dict:
            return options_dict[words[0]], 0

    if len(words) >= 2 and command_str[-1] != ' ':
        if words[0] in options_dict:
            res = options_dict[words[0]]
            return [w for w in res if re.match(words[-1], w)], -len(words[-1])

    return [], 0


def parse_command(command_str: str) -> dict:

    cmd_dict = dict()

    cmd_list = shlex.split(command_str)

    cmd_dict.update({'command': cmd_list[0]})

    for s in cmd_list[1:]:
        name, value = parse_option(s)
        cmd_dict.update({name: value})

    return cmd_dict


def parse_option(target):
    res = target.split("=", 1)
    res = [a.strip(' "\'') for a in res]

    if not res:
        return '', ''

    if len(res) < 2:
        value = '1'
        name = res[0]
    else:
        name = res[0].strip()
        value = res[1].strip()

    return name, value


def get_locator(command_dict: dict):
    locator_by = ['id', 'name', 'xpath', 'link_text', 'tag', 'class', 'css', 'partial_link_text']
    for name in locator_by:
        if name in command_dict:
            return name, command_dict[name]
    return '', ''

def get_url(command_dict: dict):
    if Cmd.URL in command_dict:
        return command_dict[Cmd.URL]
    else:
        return ''
