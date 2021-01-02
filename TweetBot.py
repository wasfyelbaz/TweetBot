from time import sleep
import random
import os
import sys
import zipfile
import tarfile

try:
    import argparse
except ImportError:
    print("* Couldn't find requests, trying to install argparse using pip3 ..")
    os.system("pip3 install argparse")
    try:
        import argparse
    except ImportError:
        print("* Couldn't find requests, trying to install argparse using pip ..")
        os.system("pip install argparse")
        import argparse

try:
    import requests
except ImportError:
    print("* Couldn't find requests, trying to install requests using pip3 ..")
    os.system("pip3 install requests")
    try:
        import requests
    except ImportError:
        print("* Couldn't find requests, trying to install requests using pip ..")
        os.system("pip install requests")
        import requests

try:
    from selenium import webdriver
except ImportError:
    print("* Couldn't find selenium, trying to install selenium using pip3 ..")
    os.system("pip3 install selenium")
    try:
        from selenium import webdriver
    except ImportError:
        print("* Couldn't find selenium, trying to install selenium using pip ..")
        os.system("pip3 install selenium")
        from selenium import webdriver

import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

VERSION = "1.4"

ACC_FILE = "accounts.txt"
TWEETS_FILE = "tweets.txt"
HASHTAGS_FILE = "hashtags.txt"

TWITTER_URL = "https://twitter.com/"
TWITTER_LOGIN_URL = TWITTER_URL + "login"
TWITTER_USERNAME_FIELD = "session[username_or_email]"
TWITTER_PASSWD_FIELD = "session[password]"

SLEEP_RANGE = [3, 7]

TWEETS_TWEETED = 0
CHECK_AFTER_N_TWEETS = 5
DRIVER_TYPE = ""

GECKODRIVERS_VERSION = "v0.28.0"
GECKODRIVERS_URLS = {
    "win32-geckodriver": f"https://github.com/mozilla/geckodriver/releases/download/{GECKODRIVERS_VERSION}/geckodriver-{GECKODRIVERS_VERSION}-win32.zip",
    "win64-geckodriver": f"https://github.com/mozilla/geckodriver/releases/download/{GECKODRIVERS_VERSION}/geckodriver-{GECKODRIVERS_VERSION}-win64.zip",
    "linux32-geckodriver": f"https://github.com/mozilla/geckodriver/releases/download/{GECKODRIVERS_VERSION}/geckodriver-{GECKODRIVERS_VERSION}-linux32.tar.gz",
    "linux64-geckodriver": f"https://github.com/mozilla/geckodriver/releases/download/{GECKODRIVERS_VERSION}/geckodriver-{GECKODRIVERS_VERSION}-linux64.tar.gz",
    "macos-geckodriver": f"https://github.com/mozilla/geckodriver/releases/download/{GECKODRIVERS_VERSION}/geckodriver-{GECKODRIVERS_VERSION}-macos.tar.gz"
                }

CHROMIUM_VERSION = "88.0.4324.27"
CHROMIUM_URLS = {
    "win32-chromium": f"https://chromedriver.storage.googleapis.com/{CHROMIUM_VERSION}/chromedriver_win32.zip",
    "linux64-chromium": f"https://chromedriver.storage.googleapis.com/{CHROMIUM_VERSION}/chromedriver_linux64.zip",
    "macos-chromium": f"https://chromedriver.storage.googleapis.com/{CHROMIUM_VERSION}/chromedriver_mac64.zip"
                }

banner1 = r"""
                                     |\    /|     
                                  ___| \,,/_/     
                               ---__/ \/    \     
                              __--/     (D)  \    
                              _ -/    (_      \   
                             // /       \_ / ==\  
       __-------_____--___--/           / \_ O o) 
      /                                 /   \==/  
     /                                 /          
    ||          )                   \_/\          
    ||         /              _      /  |         
    | |      /--______      ___\    /\  :         
    | /   __-  - _/   ------    |  |   \ \        
     |   -  -   /                | |     \ )      
     |  |   -  |                 | )     | |      
      | |    | |                 | |    | |       
      | |    < |                 | |   |_/        
      < |    /__\                <  \    TweetBot V """ + VERSION + """ 
      /__\\                       /___\\            

"""
banner2 = r"""
                                        | 
                    ____________    __ -+-  ____________ 
                    \_____     /   /_ \ |   \     _____/
                     \_____    \____/  \____/    _____/
                      \_____    TweetBot        _____/
                         \___________  ___________/
                                   /____\                         
                                       `-.___.-' Version: """ + VERSION + """ 
"""


banner3 = """
          |_|_|
          |_|_|              _____
          |_|_|     ____    |*_*_*| TweetBot V -> """ + VERSION + """ 
 _______   _\__\___/ __ \____|_|_   _______
/ ____  |=|      \  <_+>  /      |=|  ____ \\
~|    |\|=|======\\\\______//======|=|/|    |~
 |_   |    \      |      |      /    |    |
  \==-|     \     |  OO  |     /     |----|~~/
  |   |      |    |      |    |      |____/~/
  |   |       \____\____/____/      /    / /
  |   |         {----------}       /____/ /
  |___|        /~~~~~~~~~~~~\     |_/~|_|/
   \_/        |/~~~~~||~~~~~\|     /__|\\
   | |         |    ||||    |     (/|| \)
   | |        /     |  |     \       \\\\
   |_|        |     |  |     |
              |_____|  |_____|
              (_____)  (_____)
              |     |  |     |
              |     |  |     |
              |/~~~\|  |/~~~\|
              /|___|\  /|___|\\
             <_______><_______>
"""

banner_list = [banner1, banner2, banner3]

parser = argparse.ArgumentParser(description='Developed By HDMX.')
parser.add_argument('-fd', '--firefox-driver', action='store_true', help='Force the bot to use firefox (geckodriver).')
parser.add_argument('-cd', '--chrome-driver', action='store_true', help='Force the bot to use chrome (chromium).')
parser.add_argument('-v', '--version', action="store_true", help="show software version.")
args = parser.parse_args()


class MainFunctions:

    def __int__(self):
        pass

    def detect_os(self):

        global DRIVER_TYPE

        if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):

            if os.path.exists("C:\\Program Files\\Mozilla Firefox"):
                DRIVER_TYPE = "firefox"
            elif os.path.exists("C:\\Program Files (x86)\\Google") | os.path.exists("C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome"):
                DRIVER_TYPE = "chrome"

            return "windows"

        elif sys.platform.startswith('linux'):
            DRIVER_TYPE = "firefox"
            return "linux"

        elif sys.platform.startswith('darwin'):
            DRIVER_TYPE = "firefox"
            return "macos"

    def download_driver(self, url):

        print('[+] Downloading driver')
        r = requests.get(url)
        file_name = url.split("/")[-1]

        with open(file_name, 'wb') as f:
            f.write(r.content)

        print(f'[+] Downloaded: {file_name}')
        return file_name

    def handle_downloaded_driver(self, file_path, operating_system):

        if operating_system == "windows":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(str(os.getcwd()))

        elif operating_system == "linux":
            with tarfile.open(file_path) as tar_ref:
                tar_ref.extractall(str(os.getcwd()))
            os.system(f"export PATH=$PATH:{os.getcwd()}")

        elif operating_system == "macos":
            with tarfile.open(file_path) as tar_ref:
                tar_ref.extractall(str(os.getcwd()))

        sleep(.3)
        os.remove(file_path)

    def get_accounts(self):

        accounts = []

        with open(ACC_FILE, "r") as f:
            lines = f.readlines()

        for line in lines:

            if ":" in line:
                line = line.split(":")
                account = {
                    "username": line[0],
                    "passwd": line[1]
                }
                accounts.append(account)

        return accounts

    def get_tweets(self):

        tweets = []

        with open(TWEETS_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                tweets.append(line.strip())

        return tweets

    def get_hashtags(self):

        hashtags = []

        with open(HASHTAGS_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                hashtags.append(line.strip())

        full_hashtag = ""

        for hashtag in hashtags:
            full_hashtag += hashtag + " "

        return full_hashtag


class TwitterActions:

    driver = None

    def __int__(self):
        pass

    def login(self, login_username, login_password):

        print(f"[+] Going to {TWITTER_LOGIN_URL}")
        self.driver.get(TWITTER_LOGIN_URL)

        try:
            username_field = self.driver.find_element_by_name(TWITTER_USERNAME_FIELD)
            passwd_field = self.driver.find_element_by_name(TWITTER_PASSWD_FIELD)
        except selenium.common.exceptions.NoSuchElementException:
            print("[-] Check your internet connection !")
            self.driver.quit()
            exit()

        print(f"[+] Trying to login as {login_username}")
        username_field.clear()
        username_field.send_keys(login_username)

        sleep(1)

        passwd_field.clear()
        passwd_field.send_keys(login_password)
        passwd_field.send_keys(Keys.RETURN)

        sleep(5)

        try:
            self.driver.find_element_by_name(TWITTER_USERNAME_FIELD)
        except:
            return True
        return False

    def tweet(self, string, hashtag):

        for i in range(5):

            try:
                text_area = self.driver.find_element_by_class_name("public-DraftEditor-content")
            except:
                sleep(2)

        try:
            text_area.clear()
        except:
            exit("[-] Couldn't find text_area ! Your internet may be slow or you interacted with the browser.")

        text_area.send_keys(string)
        text_area.send_keys(Keys.RETURN)
        text_area.send_keys(hashtag + " ")

        sleep(1)

        action = ActionChains(self.driver)
        action.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()

    def check_tweet(self):

        return self.driver.find_element_by_class_name("public-DraftEditor-content").text

    def check_if_banned(self):

        sleep(1)

        elements = []
        found_elements = self.driver.find_elements_by_class_name("r-bcqeeo")
        for element in found_elements:
            elements.append(element.text)

        if "Something went wrong, but don’t fret — let’s give it another shot." in elements:
            return True

        return False


if args.version is True:
    exit(f"TweetBot Version: {VERSION}V")

MainFunctions = MainFunctions()
twitterActions = TwitterActions()

if os.path.isfile(ACC_FILE) is not True:
    exit(f"[-] Couldn't find {ACC_FILE} !")

if os.path.isfile(TWEETS_FILE) is not True:
    exit(f"[-] Couldn't find {TWEETS_FILE} !")

if os.path.isfile(HASHTAGS_FILE) is not True:
    exit(f"[-] Couldn't find {HASHTAGS_FILE} !")

if len(MainFunctions.get_tweets()) > 95:
    lines_to_delete = len(MainFunctions.get_tweets()) - 95
    exit(f"[-] Please delete {lines_to_delete} lines")

OS = MainFunctions.detect_os()
print(random.choice(banner_list))

if args.firefox_driver is True:
    DRIVER_TYPE = "firefox"

elif args.chrome_driver is True:
    DRIVER_TYPE = "chrome"


def start(username, passwd):

    driver = None

    if DRIVER_TYPE == "firefox":

        try:
            driver = webdriver.Firefox()

        except selenium.common.exceptions.WebDriverException:
            architecture = input("[*] OS Architecture (32 or 64): ")

            if OS == "windows":
                downloaded_file = MainFunctions.download_driver(GECKODRIVERS_URLS[f"win{architecture}-geckodriver"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)
                driver = webdriver.Firefox()

            elif OS == "linux":
                downloaded_file = MainFunctions.download_driver(GECKODRIVERS_URLS[f"linux{architecture}-geckodriver"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)
                driver = webdriver.Firefox()

            elif OS == "macos":
                downloaded_file = MainFunctions.download_driver(GECKODRIVERS_URLS["macos-geckodriver"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)
                driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver')

    elif DRIVER_TYPE == "chrome":

        try:
            driver = webdriver.Chrome()
        except selenium.common.exceptions.WebDriverException:

            if OS == "windows":
                downloaded_file = MainFunctions.download_driver(CHROMIUM_URLS["win32-chromium"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)
            try:
                driver = webdriver.Chrome()
            except:
                exit("[-] Please update chrome to the latest version.\n"
                     "[*] You can install firefox instead of using chrome.")

    if driver is None:
        exit("[-] Unknown driver error !")

    driver.minimize_window()
    twitterActions.driver = driver

    login_status = twitterActions.login(username, passwd)

    hashtags = MainFunctions.get_hashtags()

    def go_tweet(tweet_string):

        twitterActions.tweet(tweet_string, hashtags)
        sleep(.9)

        if tweet_string in str(twitterActions.check_tweet().strip()):
            print("[-] Couldn't Tweet")
        else:
            print("[+] Tweeted")

        global TWEETS_TWEETED
        TWEETS_TWEETED += 1

        sleep(random.randrange(SLEEP_RANGE[0], SLEEP_RANGE[1]))

    if login_status is True:

        for tweet in MainFunctions.get_tweets():

            global TWEETS_TWEETED
            if TWEETS_TWEETED % CHECK_AFTER_N_TWEETS == 0:
                if twitterActions.check_if_banned() is True:
                    print("[-] Account may be banned from tweeting, please check if it's been banned !")
                    if len(MainFunctions.get_accounts()) > 1:
                        print("[+] Moving to the next account")
                    break

            go_tweet(tweet)
    else:
        print("[-] Couldn't login !")

    driver.quit()


for account in MainFunctions.get_accounts():

    start(account["username"], account["passwd"])
