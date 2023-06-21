from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys

"""
/html/body/div[4]/div[1]/table/tbody/tr[1]/button[1] web1
/html/body/div[4]/div[1]/table/tbody/tr[1]/button[2] web2 
 
/html/body/div[4]/div[1]/table/tbody/tr[2]/button[1] pwn1
/html/body/div[4]/div[1]/table/tbody/tr[2]/button[2] pwn2
"""


class Spider():
    browser = None

    CHALLANGE_TO_PATH = {
        "web": '1',
        "pwn": '2',
        "reverse": '3',
        "misc": '4',
        "mobile": '5'
    }

    def __init__(self):
        # print("[+]Init selenium...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        CHROME_DRIVER_PATH = "./chromedriver_win32/chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)

    def login(self,username, password):
        self.browser.get('https://iscc.isclab.org.cn/login')
        self.browser.find_element(By.XPATH, '/html/body/div[1]/form/input[1]').send_keys(username)
        self.browser.find_element(By.XPATH, '/html/body/div[1]/form/input[2]').send_keys(password)
        self.browser.find_element(By.XPATH, '/html/body/div[1]/form/div[2]/button').click()

    def logout(self):
        self.browser.get('https://iscc.isclab.org.cn/logout')

    # /html/body/div[4]/div[1]/table/tbody/tr[1]/button[1]

    def getChallange(self,challangeType, challangeNum):
        self.browser.get('https://iscc.isclab.org.cn/challenges')
        time.sleep(3)
        xpath = f"/html/body/div[3]/div[1]/table/tbody/tr[{self.CHALLANGE_TO_PATH[challangeType]}]/button[{challangeNum}]"
        self.browser.find_element(By.XPATH, xpath).click()
        print("[+]Waiting for 2.5 seconds to load the page...")
        time.sleep(2.5)

    def submitFlag(self,flag):
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div/input[1]").send_keys(flag)
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div/button").click()
        time.sleep(1)
        response = self.browser.find_element(By.XPATH, "/html/body/div[2]/div/button").text
        return (response)

    def autoSubmitFlag(self,username, password, challangeType, challangeNum, flag):
        # _challange = challange.split(' ')
        self.login(username, password)
        self.getChallange(challangeType, challangeNum)
        # getChallange(_challange[0], _challange[1])
        if "ISCC{" in flag:
            self.submitFlag(flag)
        else:
            self.submitFlag("ISCC{" + flag + "}")
        self.logout()


if __name__ == "__main__":
    spider = Spider()
    spider.autoSubmitFlag(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    pass
