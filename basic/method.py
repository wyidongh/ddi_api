#coding:utf-8
from os import path
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
from json import loads

class Comply(object):
    def __init__(self):
        self.driver, self.exception = webdriver.Chrome(), set()

    @classmethod
    def get_info(cls):
        with open(path.join(path.dirname(path.split(path.realpath(__file__))[0]), 'testinfo.json'), 'r') as f:
            info = loads(f.read())
        cls.websites = info['ddiaddrs']
        cls.username = info['username']
        cls.password = info['password']
        cls.nodename = info['nodename']
        cls.devices = info['devices']
        cls.serverip = info['serverip']
        cls.sourceip = info['sourceip']
        cls.sshaddr = info['sshaddr']
        cls.sshport = info['sshport']
        cls.sshusername = info['sshusername']
        cls.sshpassword = info['sshpassword']
        cls.dhcpnode = info['dhcpnode']
        cls.api_user = info['api_user']
        cls.api_password = info['api_password']

    def sshexec(self, dtype, command):
        from paramiko import SSHClient
        from paramiko import AutoAddPolicy
        session, self.sshresult = SSHClient(), None
        session.set_missing_host_key_policy(AutoAddPolicy())
        try:
            session.connect(hostname=self.sshaddr[dtype], port=self.sshport[dtype], username=self.sshusername[dtype], password=self.sshpassword[dtype])
            _, stdout, stderr = session.exec_command(command)
            result = tuple(i.rstrip('\n') for i in stderr.readlines())
            if result != tuple():
                self.sshresult = result
                return
            self.sshresult = tuple(i.rstrip('\n') for i in stdout.readlines())
            print(self.sshresult)
        except BaseException:
            self.exception.add('ssh connection failed')
        finally:
            session.close()

    def id_click(self, idnum):
        for _ in range(6):
            try:
                self.driver.find_element_by_id(idnum).click()
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def id_send(self, idnum, value):
        for _ in range(6):
            try:
                self.driver.find_element_by_id(idnum).send_keys(value)
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def id_clear(self, idnum):
        for _ in range(6):
            try:
                self.driver.find_element_by_id(idnum).clear()
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def id_del(self, idnum):
        for _ in range(6):
            try:
                self.driver.find_element_by_id(idnum).send_keys(Keys.CONTROL+'a')
                self.driver.find_element_by_id(idnum).send_keys(Keys.BACKSPACE)
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def path_click(self, path):
        for _ in range(6):
            try:
                self.driver.find_element_by_xpath(path).click()
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def path_send(self, path, value):
        for _ in range(6):
            try:
                self.driver.find_element_by_xpath(path).send_keys(value)
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def path_clear(self, path):
        for _ in range(6):
            try:
                self.driver.find_element_by_xpath(path).clear()
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def path_del(self, path):
        for _ in range(6):
            try:
                self.driver.find_element_by_xpath(path).send_keys(Keys.CONTROL+'a')
                self.driver.find_element_by_xpath(path).send_keys(Keys.BACKSPACE)
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def id_select(self, idnum, value):
        for _ in range(6):
            try:
                Select(self.driver.find_element_by_id(idnum)).select_by_visible_text(value)
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def path_select(self, path, value):
        for _ in range(6):
            try:
                Select(self.driver.find_element_by_xpath(path)).select_by_visible_text(value)
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def alert(self):
        for _ in range(6):
            try:
                alert = self.driver.switch_to.alert
                self.alert_text = alert.text
                alert.accept()
                break
            except BaseException as error:
                self.error = error
                sleep(0.5)
        else:
            self.exception.add(self.error)

    def get_path(self, filename):
        self.file = path.join(path.dirname(path.split(path.realpath(__file__))[0]), 'case', filename)

    

