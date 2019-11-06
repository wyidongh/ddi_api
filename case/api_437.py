from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource
from requests.auth import HTTPBasicAuth


class RunTest(TestCase, Tools, ddi_api, system, resource):
    @classmethod
    def setUpClass(cls):
        cls.get_info()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get(cls.websites)
        cls.driver.find_element_by_id('loginname').send_keys(cls.username)
        cls.driver.find_element_by_id('password').send_keys(cls.password)
        cls.driver.find_element_by_id('vcoe').send_keys('yamu')
        cls.driver.find_element_by_id('login_btn').click()

    @classmethod
    def tearDownClass(cls):
        sleep(1)
        cls.driver.quit()

    def setUp(self):
        self.exception = set()
        self.path_click('/html/body/div[1]/div[1]/header/div[1]/div/div[3]/div/div/div/ul/li[1]/h2/a')
        print('添加dns节点')
        self.dhs_node_add_dns_node(nodename=self.nodename[0],device=self.devices)
        print('为节点%s添加api用户%s' % (self.nodename, self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(3)

    def tearDown(self):

        self.delete_api_user()
        self.dns_node_delete_all_node()
        sleep(2)
        if self.exception:
            raise Exception(self.exception)


    def test_authentication_fail_scenairo(self):

        url = "https://" + self.serverip[0] + ":19393/api/dns/zones"

        print('Step1: 通过requests库的http的auth字段进行鉴权，输入正确的用户名test、密码为空 auth=("test", "")')
        r1 = self.get(url=url,auth=HTTPBasicAuth(self.api_user,""))

        if self.api_error is  None:
            status_code1 = r1[0]
            res1 = r1[1]
            if not (status_code1 == 401 and res1["code"] == "AuthorizationFail"):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)

        print('Step2: 不输入用户名，输入正确的密码“admin123456” auth=("", "admin123456")')
        r2 = self.get(url=url, auth=HTTPBasicAuth("", self.api_password))
        if self.api_error is  None:
            status_code2 = r2[0]
            res2 = r2[1]
            if not (status_code2 == 401 and res2["code"] == "AuthorizationFail"):
                self.exception.add("Step2:" + str(res2))
        else:
            self.exception.add("Step2: " + self.api_error)

        print('Step3: 输入正确的用户名为test，错误的密码为test123456 auth=（"test"，“test123456”）')
        r3 = self.get(url=url, auth=HTTPBasicAuth(self.api_user, "test123456"))
        if self.api_error is None:
            status_code3 = r3[0]
            res3 = r3[1]
            if not (status_code3 == 401 and res3["code"] == "AuthorizationFail"):
                self.exception.add("Step3:" + str(res3))
        else:
            self.exception.add("Step3: " + self.api_error)

        print('Step4: 输入错误的用户名为test1，正确的密码为admin123456 auth=（“test1”，“admin123456”）')
        r4 = self.get(url=url, auth=HTTPBasicAuth("test1", self.api_password))
        if self.api_error is None:
            status_code4 = r4[0]
            res4 = r4[1]
            if not (status_code4 == 401 and res4["code"] == "AuthorizationFail"):
                self.exception.add("Step1:" + str(res4))
        else:
            self.exception.add("Step1: " + self.api_error)

        print('Step5: 输入错误的用户名为test1，错误的密码为admin1234 auth=（“test1”，“admin123456”）')
        r5 = self.get(url=url, auth=HTTPBasicAuth("test1", "test123456"))
        if self.api_error is None:
            status_code5 = r5[0]
            res5 = r5[1]
            if not (status_code5 == 401 and res5["code"] == "AuthorizationFail"):
                self.exception.add("Step1:" + str(res5))
        else:
            self.exception.add("Step1: " + self.api_error)

        print('Step6: 不输入用户名和密码 auth=（“”，“”）')
        r6 = self.get(url=url, auth=HTTPBasicAuth("", ""))
        if self.api_error is  None:
            status_code6 = r6[0]
            res6 = r6[1]
            if not (status_code6 == 401 and res6["code"] == "AuthorizationFail"):
                self.exception.add("Step1:" + str(res6))
        else:
            self.exception.add("Step1: " + self.api_error)
