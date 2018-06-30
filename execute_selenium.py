import time
from split import parse_option
from selenium.webdriver.common.by import By
from selenium import webdriver as wd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


class ClickerException(Exception):
    pass


class Do(object):
    CLICK = "click"
    CLEAR = "clear"
    SEND_KEYS = "send_keys"


class WebClicker:
    def __init__(self, driver_exe_path, browser='firefox', profile_path='', browser_binary=None):

        self.webdriver = None
        self.profile = None
        try:
            if browser == 'firefox':
                if profile_path:
                    self.profile = wd.FirefoxProfile(profile_path)
                else:
                    self.profile = None
                self.webdriver = wd.Firefox(firefox_profile=self.profile, executable_path=driver_exe_path,
                                            firefox_binary=browser_binary)
            else:
                raise ClickerException('Not supported browser {0}'.format(browser))
        except Exception as e:
            print(e)
            print('Fail to initialize {0}'.format(browser))

    def execute_command(command, target, value, wait_element_sec=0):

        by_= {'id': By.ID,
              'ccs:': By.CSS_SELECTOR,
              'class': By.CLASS_NAME,}

        by, loc = parse_option(target)

        pass

    def get_element(self, how, what):
        try:
            element = self.webdriver.find_element(by=how, value=what)
            return element
        except NoSuchElementException as e:
            return None

    def wait_element(self, how: str, what: str, timeout_sec=1):

        for i in range(timeout_sec):
            if self.is_element_ready(how, what):
                print('Element found!')
                return True
            else:
                self.sleep(1)
                print('Waiting: {0}'.format(i), end='\r')

        print("Timeout")
        return False

    def do(self, what: str, how: By, loc: str, value='', timeout_sec=1):

        element = None

        for i in range(timeout_sec):
            element = self.get_element(how, loc)
            if element is not None:
                print('Element found!')
                break
            else:
                self.sleep(1)
                print('Waiting: {0}'.format(i), end='\r')

        if element is None:
            print("Timeout")
            return False

        try:
            action = getattr(element, what)
        except AttributeError:
            print("Wrong Action with element: {0}".format(what))
            return False

        for i in range(timeout_sec):
            try:
                if what == Do.SEND_KEYS:
                    action(value)
                else:
                    action()
                return True
            except ElementNotInteractableException:
                self.sleep(1)

        print("Do action failed")
        return False

    def get_element_value(self, how: By, path: str, timeout_sec=30):

        element = None

        for i in range(timeout_sec):
            element = self.get_element(how, path)
            if element is not None:
                print('Element found!')
                break
            else:
                self.sleep(1)
                print('Waiting:', i)

        if element is not None:
            return element.get_attribute('value')
        else:
            return 'Element not found!'

    def is_element_present(self, how, what):
        try:
            self.webdriver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_element_ready(self, how, what):
        if self.is_element_present(how, what):
            return self.webdriver.find_element(by=how, value=what).is_enabled()
        else:
            return False

    @staticmethod
    def sleep(time_sec):
            time.sleep(time_sec)
