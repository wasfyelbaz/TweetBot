from core import config

from time import sleep

import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TwitterActions:

    driver = None

    def __int__(self):
        pass

    def login(self, login_username, login_password):

        print(f"[+] Going to {config.TWITTER_LOGIN_URL}")

        # go to twitter's login page
        self.driver.get(config.TWITTER_LOGIN_URL)

        try:
            # trying to locate the username field for 10 seconds max
            username_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, "//input[@autocomplete ='username']")))
        except selenium.common.exceptions.TimeoutException:
            print("[-] Check your internet connection !")
            self.driver.quit()
            exit()

        print(f"[+] Trying to login as {login_username}")
        sleep(1)

        try:
            # trying to enter 5 numbers with slow rate to check if an error will occur
            for i in range(5):
                username_field.send_keys(i)
                sleep(.3)
            # if succeeded, then the input field will be cleared
            username_field.clear()

        except:
            # if an error occured, then the page will be reloaded
            self.driver.get(config.TWITTER_LOGIN_URL)
            sleep(3)
            # trying to locate the username field once again for 10 seconds max
            username_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, "//input[@autocomplete ='username']")))

        # entering the username with human speed
        for i in range(len(login_username)):
            username_field.send_keys(login_username[i])
            sleep(.1)

        sleep(1)

        # clicking enter to go to the password input
        username_field.send_keys(Keys.RETURN)

        sleep(5)

        try:
            # trying to locate the password field for 10 seconds max
            passwd_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
        except selenium.common.exceptions.TimeoutException:
            try:
                # checking if there is no such account
                WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//input[@autocomplete ='username']")))
                return config.ACCOUNT_NOT_FOUND_STATUS_CODE
            except:
                # checking if twitter blocked us
                WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")))
                return config.BLOCKED_US_FROM_LOGIN_STATUS_CODE #"[+] Twitter blocked us from loging in for a while"

        # entering password
        passwd_field.clear()
        passwd_field.send_keys(login_password)
        sleep(.1)
        passwd_field.send_keys(Keys.RETURN)

        sleep(5)

        try:
            # checking if the password is wrong
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
            return config.WRONG_PASSWORD_STATUS_CODE

        except:
            return config.SUCCESSFULL_LOGIN_STATUS_CODE

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

        if "Something went wrong, but don't worry — let's give it another shot." in elements:
            return True

        return False
