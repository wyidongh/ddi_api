from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.dnspage import dnspage
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource


class RunTest(TestCase, Tools, ddi_api, system, dnspage, resource):
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
        self.dhs_node_add_dns_node(nodename=self.nodename[0], device=self.devices)
        print('为节点%s添加api用户%s' % (self.nodename[0], self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(4)

    def tearDown(self):
        self.authorization_delete_all_domain()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_modify_record_ttl_and_comment(self):

        print('Step1: 点击【域管理】，添加域test.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        print('Step2: 点击【记录管理】，添加r1.test.com的A记录的解析结果为1.1.1.1,权重为1，ttl为100，备注为空')
        self.authorization_add_a_record(nodename=self.nodename[0],domain=domain1,host="r1",res="1.1.1.1",weight=1,ttl=100)


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step3: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=test.com&host=r1接口，查出步骤3中记录的id')
        payload3 = {
                    "domain": domain1,
                    "host": "r1"
                }
        r3 = self.get(url=url1,params=payload3,auth=(self.api_user,self.api_password))
        id = ""
        if self.api_error is None:
            status_code3,res3 = r3
            if status_code3 == 200 and res3['code'] == "Success" and len(res3['data']) == 1:
                id = res3['data'][0]['id']
            else:
                self.exception.add('Step3: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        url2 = url1 + "/" + str(id)

        print('Step4: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的权重修改为2,http的报文body为')
        payload4 = {"weight" : 2}
        r4 = self.put(url=url2,json=payload4,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error) )


        print('Step5: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的权重修改为254')
        payload5 = {"weight" : 254}
        r5 = self.put(url=url2,json=payload5,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code5,res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的权重修改为0')
        payload6 = {"weight" : 0}
        r6 = self.put(url=url2, json=payload6,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidWeight"):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的权重修改为255')
        payload7 = {"weight": 255}
        r7 = self.put(url=url2, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidWeight"):
                self.exception.add('Step7: ' + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的权重修改为负数')
        payload8 = {"weight": -1}
        r8 = self.put(url=url2, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 400 and res8['code'] == "InvalidWeight"):
                self.exception.add('Step8: ' + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))


        print('Step9: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的ttl修改为1')
        payload9 = {"ttl": 1}
        r9 = self.put(url=url2, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add("Step9: " + str(r9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的ttl修改为8640000')
        payload10 = {"ttl": 8640000}
        r10 = self.put(url=url2, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success"):
                self.exception.add('Step10: ' + str(r10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的ttl修改为0')
        payload11 = {"ttl": 0}
        r11 = self.put(url=url2, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "InvalidTtl"):
                self.exception.add('Step11: ' + str(r11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的ttl修改为8640001')
        payload12 = {"ttl": 8640001}
        r12 = self.put(url=url2, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "InvalidTtl"):
                self.exception.add('Step12: ' + str(r12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的status修改为0')
        payload13 = {"status": 0}
        r13 = self.put(url=url2, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 200 and res13['code'] == "Success"):
                self.exception.add('Step13: ' + str(r13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的status修改为2')
        payload14 = {"status": 2}
        r14 = self.put(url=url2, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "InvalidStatus"):
                self.exception.add('Step14: ' + str(r14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的备注为合法长度')
        payload15 = {"comment": "abcdefg"}
        r15 = self.put(url=url2, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 200 and res15['code'] == "Success"):
                self.exception.add('Step15: ' + str(r15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的备注为合法长度')
        payload16 = {"comment": "abcdefg"}
        r16 = self.put(url=url2, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 200 and res16['code'] == "Success"):
                self.exception.add('Step16: ' + str(r16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))

        print('Step17: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com的备注为超过100个字符')
        payload17 = {"comment": "a" * 101}
        r17 = self.put(url=url2, json=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 400 and res17['code'] == "InvalidParam"):
                self.exception.add('Step17: ' + str(r17))
        else:
            self.exception.add('Step17: ' + str(self.api_error))


        print('Step18: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/5bbf1a028889ee7be5a9236e接口，将r1.test.com解析结果修改为2.2.2.2，权重修改为2，ttl修改为100，status修改为0')
        payload18 = {
                    "result": {"data": "2.2.2.2"},
                    "weight": 2,
                    "ttl": 100,
                    "status": 0,
                    "comment": "测试"
                    }
        r18 = self.put(url=url2, json=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 200 and res18['code'] == "Success"):
                self.exception.add('Step18: ' + str(r18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))

        url3 = url1 + "/123456"
        print('Step19: 用PUT方法调用https://192.168.6.62:19393/api/dns/records/123456接口，修改不存在的id记录')
        payload19 = {"comment": "测试"}
        r19 = self.put(url=url3, json=payload19, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19, res19 = r19
            if not (status_code19 == 400 and res19['code'] == "RecordNotExisted"):
                self.exception.add('Step19: ' + str(r19))
        else:
            self.exception.add('Step19: ' + str(self.api_error))