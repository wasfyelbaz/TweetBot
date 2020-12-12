from time import sleep
import random
import os
import sys
import zipfile

try:
    import requests
except ImportError:
    print("* Couldn't find requests, trying to install requests ..")
    os.system("pip install requests")
    import requests

try:
    from selenium import webdriver
except ImportError:
    print("* Couldn't find selenium, trying to install selenium ..")
    os.system("pip install selenium")
    from selenium import webdriver

import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

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

GECKODRIVERS_URLS = {
    "win32-geckodriver": "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-win32.zip",
    "win64-geckodriver": "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-win64.zip",
    "linux32-geckodriver": "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz",
    "linux64-geckodriver": "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz",
    "macos-geckodriver": "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-macos.tar.gz"
                }

banner1 = """
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
      < |    /__\                <  \    TweetBot V 1.2
      /__\                       /___\            

"""
banner2 = '''
                                        | 
                    ____________    __ -+-  ____________ 
                    \_____     /   /_ \ |   \     _____/
                     \_____    \____/  \____/    _____/
                      \_____    TweetBot        _____/
                         \___________  ___________/
                                   /____\                         
                                       `-.___.-' Version: 1.2
'''


banner3 = '''
          |_|_|
          |_|_|              _____
          |_|_|     ____    |*_*_*| TweetBot V -> 1.2
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
'''
banner_list = [banner1, banner2, banner3]


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
            return "linux"

        elif sys.platform.startswith('darwin'):
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
            pass
        elif operating_system == "macos":
            pass

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

        loop = True
        while loop is True:
            try:
                text_area = self.driver.find_element_by_class_name("public-DraftEditor-content")
                loop = False
            except:
                sleep(2)

        text_area.clear()
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


MainFunctions = MainFunctions()
twitterActions = TwitterActions()

if len(MainFunctions.get_tweets()) > 95:
    lines_to_delete = len(MainFunctions.get_tweets()) - 95
    exit(f"[-] Please delete {lines_to_delete} lines")

OS = MainFunctions.detect_os()
print(random.choice(banner_list))


def start(username, passwd):

    if DRIVER_TYPE == "firefox":

        try:
            driver = webdriver.Firefox()
        except selenium.common.exceptions.WebDriverException:
            architecture = input("[*] OS Architecture (32 or 64): ")

            if OS == "windows":
                downloaded_file = MainFunctions.download_driver(GECKODRIVERS_URLS[f"win{architecture}-geckodriver"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)

            elif OS == "linux":
                downloaded_file = MainFunctions.download_driver(GECKODRIVERS_URLS[f"linux{architecture}-geckodriver"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)

            elif OS == "macos":
                downloaded_file = MainFunctions.download_driver(GECKODRIVERS_URLS["macos-geckodriver"])
                MainFunctions.handle_downloaded_driver(downloaded_file, OS)

            driver = webdriver.Firefox()

    elif DRIVER_TYPE == "chrome":

        try:
            driver = webdriver.Chrome()
        except selenium.common.exceptions.WebDriverException:
            exit("Couldn't find chromedriver:\nPlease download it from https://chromedriver.chromium.org/ and add it to your PATH.")

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
