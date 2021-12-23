from core import config

import sys
import zipfile
import tarfile
import os
from time import sleep

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


class MainFunctions:

    driver_type = None

    def detect_os(self):

        if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):

            if os.path.exists("C:\\Program Files\\Mozilla Firefox"):
                self.driver_type = "firefox"
            elif os.path.exists("C:\\Program Files (x86)\\Google") | os.path.exists("C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome"):
                self.driver_type = "chrome"

            return "windows"

        elif sys.platform.startswith('linux'):
            self.driver_type = "firefox"
            return "linux"

        elif sys.platform.startswith('darwin'):
            self.driver_type = "firefox"
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

        with open(config.ACC_FILE, "r") as f:
            lines = f.readlines()

        for line in lines:

            if ":" in line and "#" not in line:
                line = line.split(":")
                account = {
                    "username": line[0],
                    "passwd": line[1]
                }
                accounts.append(account)

        return accounts

    def comment_account(self, username, additional_note=""):

        with open(config.ACC_FILE, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):

            if username in line:
                if additional_note != "":
                    lines[i] = line.replace(username, f"# [{additional_note}] {username}")
                    break
                else:
                    lines[i] = line.replace(username, f"#{username}")
                    break
    
        with open(config.ACC_FILE, "w") as f:
            f.writelines(lines)

    def get_tweets(self):

        tweets = []

        with open(config.TWEETS_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                tweets.append(line.strip())

        return tweets

    def get_hashtags(self):

        hashtags = []

        with open(config.HASHTAGS_FILE, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                hashtags.append(line.strip())

        full_hashtag = ""

        for hashtag in hashtags:
            full_hashtag += hashtag + " "

        return full_hashtag

