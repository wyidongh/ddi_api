from time import sleep
from selenium import webdriver

class common():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def getElementText_by_xpath(self,element):
        s = ""
        for i in range(6):
            try:
                r = self.driver.find_element_by_xpath(element)
                s = r.text
                break
            except BaseException:
                sleep(0.5)
        #print("s: %s" % s)
        return s

    def getElementText_by_id(self,element):
        s = ""
        for i in range(6):
            try:
                r = self.driver.find_element_by_id(element)
                s = r.text
                break
            except BaseException:
                sleep(0.5)
        return s


    def isMatch(self,text1,text2):
        if text1 == text2:
            return True
        else:
            return False

    def isElementExist_by_xpath(self, element):
        flag = False
        for i in range(6):
            try:
                self.driver.find_element_by_xpath(element)
                flag = True
                break
            except BaseException:
                sleep(0.5)
        return flag


