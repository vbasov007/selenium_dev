
import shlex


def line_split(line):
    return shlex.split(line)


def add_https_to_url(url: str):
    if not url.startswith(r'https://'):
        return r'https://' + url
    return url


