from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource

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
        sleep(3)
        cls.driver.quit()

    def setUp(self):
        self.exception = set()
        self.path_click('/html/body/div[1]/div[1]/header/div[1]/div/div[3]/div/div/div/ul/li[1]/h2/a')
        print('添加dns节点')
        self.dhs_node_add_dns_node(nodename=self.nodename[0], device=self.devices)
        print('为节点%s添加api用户%s' % (self.nodename, self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(3)

    def tearDown(self):

        self.sshexec('slave', "reboot")
        sleep(20)
        self.driver.refresh()
        sleep(1.5)
        self.driver.find_element_by_id('loginname').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_id('vcoe').send_keys('yamu')
        self.driver.find_element_by_id('login_btn').click()
        sleep(2)
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)


    def test_authentication_fail_scenairo(self):

        print('Step1: 将当前DDI系统切换为从服务器')
        url1 = "https://" + self.serverip[0] + ":19393/api/dns/zones"
        command1 = "reboot"
        self.sshexec('master',command1)

        sleep(90)

        print('Step2: 输入正确的用户名test，正确的密码admin123456')
        r1 = self.get(url=url1,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code1,res1 = r1
            if not(status_code1 == 500 and res1['code'] == "NotMaster"):
                self.exception.add('Step1: ' + str(r1))
        else:
            self.exception.add("Step1: " + self.api_error)


        print('Step3: 查询的节点名称不存在，用GET方法调用https://192.168.6.62:19393/api/dns/zones?nodeName=node100接口')
        url2 = "https://" + self.serverip[1] + ":19393/api/dns/zones"
        payload = {
            "nodeName": "node100"
        }

        r2 = self.get(url=url2, params=payload, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 400 and res2['code'] == "NodeNotExisted"):
                self.exception.add('Step2: ' + str(r2))
        else:
            self.exception.add("Step2: " + self.api_error)













