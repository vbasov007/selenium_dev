
import shlex


def line_split(line):
    return shlex.split(line)


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


def add_https_to_url(url: str):
    if not url.startswith(r'https://'):
        return r'https://' + url
    return url


def parse_command(command_str: str, possible_commands=[], possible_options=[]) -> dict:

    cmd_dict = dict()

    cmd_list = line_split(command_str)

    if len(possible_commands) > 0:
        if cmd_list[0] in possible_commands:
            cmd_dict.update({'command': cmd_list[0]})
    else:
        cmd_dict.update({'command': cmd_list[0]})

    for s in cmd_list[1:]:
        name, value = parse_option(s)
        if len(possible_options):
            if name in possible_options:
                cmd_dict.update({name: value})
        else:
            cmd_dict.update({name: value})

    return cmd_dict
