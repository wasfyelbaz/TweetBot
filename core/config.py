# DON'T CHANGE, UNLESS YOU UNDERSTAND WHAT YOU DOIN

VERSION = "1.6"

ACC_FILE = "accounts.txt"
TWEETS_FILE = "tweets.txt"
HASHTAGS_FILE = "hashtags.txt"

TWITTER_URL = "https://twitter.com/"
TWITTER_LOGIN_URL = TWITTER_URL + "login"
TWITTER_USERNAME_FIELD = "session[username_or_email]"
TWITTER_PASSWD_FIELD = "session[password]"

ACCOUNT_NOT_FOUND_STATUS_CODE = -1
BLOCKED_US_FROM_LOGIN_STATUS_CODE = -2
WRONG_PASSWORD_STATUS_CODE = 0
SUCCESSFULL_LOGIN_STATUS_CODE = 1

SLEEP_RANGE = [3, 7]

CHECK_AFTER_N_TWEETS = 5

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
