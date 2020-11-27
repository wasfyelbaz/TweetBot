from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import random

ACC_FILE = "accounts.txt"
TWEETS_FILE = "tweets.txt"
HASHTAGS_FILE = "hashtags.txt"

TWITTER_URL = "https://twitter.com/"
TWITTER_LOGIN_URL = TWITTER_URL + "login"
TWITTER_USERNAME_FIELD = "session[username_or_email]"
TWITTER_PASSWD_FIELD = "session[password]"


def get_accounts():

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


def get_tweets():

    tweets = []

    with open(TWEETS_FILE, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            tweets.append(line.strip())

    return tweets


def get_hashtags():

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

        username_field = self.driver.find_element_by_name(TWITTER_USERNAME_FIELD)
        passwd_field = self.driver.find_element_by_name(TWITTER_PASSWD_FIELD)

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

        print("[+] Tweeting (+)")


twitterActions = TwitterActions()

if len(get_tweets()) >= 95:
    lines_to_delete = len(get_tweets()) - 95
    exit(f"[-] Please delete {lines_to_delete}")


def start(username, passwd):

    try:
        driver = webdriver.Firefox()
    except selenium.common.exceptions.WebDriverException:
        exit("Couldn't find geckodriver:\nPlease download it from https://github.com/mozilla/geckodriver/releases and add it to your PATH.")

    driver.minimize_window()
    twitterActions.driver = driver

    login_status = twitterActions.login(username, passwd)

    hashtags = get_hashtags()

    def go_tweet(tweet_string):

        twitterActions.tweet(tweet_string, hashtags)
        sleep(random.randrange(5, 15))

    if login_status is True:

        for tweet in get_tweets():
            go_tweet(tweet)

    else:

        print("[-] Couldn't login")

    driver.quit()


for account in get_accounts():

    start(account["username"], account["passwd"])
