from core import banners
from core import config
from core import TwitterActions
from core import MainFunctions

from time import sleep
import random
import os

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

DRIVER_TYPE = ""
TWEETS_TWEETED = 0

parser = argparse.ArgumentParser(description='Developed By SyncV.')
parser.add_argument('-fd', '--firefox-driver', action='store_true', help='Force the bot to use firefox (geckodriver).')
parser.add_argument('-cd', '--chrome-driver', action='store_true', help='Force the bot to use chrome (chromium).')
parser.add_argument('-v', '--version', action="store_true", help="show software version.")
args = parser.parse_args()

if args.version is True:
    exit(f"TweetBot Version: {config.VERSION}V")

mainFunctions = MainFunctions.MainFunctions()
twitterActions = TwitterActions.TwitterActions()

if os.path.isfile(config.ACC_FILE) is not True:
    exit(f"[-] Couldn't find {config.ACC_FILE} !")

if os.path.isfile(config.TWEETS_FILE) is not True:
    exit(f"[-] Couldn't find {config.TWEETS_FILE} !")

if os.path.isfile(config.HASHTAGS_FILE) is not True:
    exit(f"[-] Couldn't find {config.HASHTAGS_FILE} !")

if len(mainFunctions.get_tweets()) > 95:
    lines_to_delete = len(mainFunctions.get_tweets()) - 95
    exit(f"[-] Please delete {lines_to_delete} lines")

OS = mainFunctions.detect_os()
print(random.choice(banners.banners_list))

if args.firefox_driver is True:
    mainFunctions.driver_type = "firefox"

elif args.chrome_driver is True:
    mainFunctions.driver_type = "chrome"


def start(username, passwd):

    driver = None

    if mainFunctions.driver_type == "firefox":

        try:
            driver = webdriver.Firefox()

        except selenium.common.exceptions.WebDriverException:
            architecture = input("[*] OS Architecture (32 or 64): ")

            if OS == "windows":
                downloaded_file = mainFunctions.download_driver(config.GECKODRIVERS_URLS[f"win{architecture}-geckodriver"])
                mainFunctions.handle_downloaded_driver(downloaded_file, OS)
                driver = webdriver.Firefox()

            elif OS == "linux":
                downloaded_file = mainFunctions.download_driver(config.GECKODRIVERS_URLS[f"linux{architecture}-geckodriver"])
                mainFunctions.handle_downloaded_driver(downloaded_file, OS)
                driver = webdriver.Firefox()

            elif OS == "macos":
                downloaded_file = mainFunctions.download_driver(config.GECKODRIVERS_URLS["macos-geckodriver"])
                mainFunctions.handle_downloaded_driver(downloaded_file, OS)
                driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver')

    elif mainFunctions.driver_type == "chrome":

        try:
            driver = webdriver.Chrome()
        except selenium.common.exceptions.WebDriverException:

            if OS == "windows":
                downloaded_file = mainFunctions.download_driver(config.CHROMIUM_URLS["win32-chromium"])
                mainFunctions.handle_downloaded_driver(downloaded_file, OS)
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

    hashtags = mainFunctions.get_hashtags()

    def go_tweet(tweet_string):

        twitterActions.tweet(tweet_string, hashtags)
        sleep(.9)

        if tweet_string in str(twitterActions.check_tweet().strip()):
            print("[-] Couldn't Tweet")
        else:
            print("[+] Tweeted")

        global TWEETS_TWEETED
        TWEETS_TWEETED += 1

        sleep(random.randrange(config.SLEEP_RANGE[0], config.SLEEP_RANGE[1]))

    if login_status == config.SUCCESSFULL_LOGIN_STATUS_CODE:

        for tweet in mainFunctions.get_tweets():

            global TWEETS_TWEETED
            if TWEETS_TWEETED % config.CHECK_AFTER_N_TWEETS == 0:
                if twitterActions.check_if_banned() is True:
                    print("[-] Account may be banned from tweeting, please check if it's been banned !")
                    if len(mainFunctions.get_accounts()) > 1:
                        print("[+] Moving to the next account")
                    break

            go_tweet(tweet)

    elif login_status == config.ACCOUNT_NOT_FOUND_STATUS_CODE:
        # Account couldn't be found
        print(f"[-] Account {username} not found !")
        # Commenting the account from the accounts.txt
        mainFunctions.comment_account(username, "Account not found")

    elif login_status == config.BLOCKED_US_FROM_LOGIN_STATUS_CODE:
        driver.quit()
        exit(f"[-] Twitter blocked us from login, try again later !")

    elif login_status == config.WRONG_PASSWORD_STATUS_CODE:
        print(f"[-] Couldn't login with {username}, wrong password !")
        # Commenting the account from the accounts.txt
        mainFunctions.comment_account(username, "Wrong password")

    driver.quit()


for account in mainFunctions.get_accounts():

    start(account["username"], account["passwd"])
