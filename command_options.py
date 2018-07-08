
locator_strategies = ['id=""', 'name=""', 'xpath=""', 'link_text=""', 'tag=""', 'class=""', 'css=""', 'partial_link_text=""']

command_options = {
    'start': ['url=""'],
    'run': ['file=""'],
    'shutdown': [],
    'set': ['driver_exe_path=""', 'browser=""', 'profile_path=""', 'browser_binary=""'],
    'find_elements': locator_strategies,
    'switch_to_frame': 'index=',
    'wait': ['time='] + locator_strategies,
    'click': locator_strategies,
    'clear': locator_strategies,
    'sendkeys': ['string=""'] + locator_strategies,
    'send_ctrl_key': ['key=""'] + locator_strategies,
    'get': ['url=""'],
    'html': ['-inner', '-outer'] + locator_strategies,
    'page_html': [],
    'get_attribute': ['attr=""'] + locator_strategies}

