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
        self.dhs_node_add_dns_node(nodename=self.nodename[1])
        print('为节点%s添加api用户%s' % (self.nodename[0], self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(4)

    def tearDown(self):
        self.authorization_delete_all_domain()
        # self.view_delete_all_view()
        # self.view_delete_all_addr_group()

        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_add_auth_record_hostname_validation_check(self):

        print('Step1: 点击【域管理】在node1下的default视图，添加域test.com，在node2下添加yamu.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        domain2 = "yamu.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])
        domain_a = "3.2.1"
        arpa_type1 = "in-addr.arpa"
        reverse_domain1 = domain_a + "." + arpa_type1
        self.authorization_add_reverse_domain(domainname=domain_a, arpa_type=arpa_type1,
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)
        domain_b = "a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.1.2.3.4"
        arpa_type2 = "ip6.arpa"
        reverse_domain2 = domain_b + "." + arpa_type2
        self.authorization_add_reverse_domain(domainname=domain_b, arpa_type=arpa_type2,
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step2: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名为空')
        payload2 = {
                    "domain": domain1,
                    "host": "",
                    "result": {"data": "1.1.1.1"}
                    }
        r2 = self.post(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add('Step2: ' + str(res2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 点击【记录管理】，查看步骤2添加的记录')
        self.authorization_enter_record_page()
        flag = self.authorization_find_specific_record(nodename=self.nodename[0], record=domain1, type='A',res='1.1.1.1')
        if not flag:
            self.exception.add('Step3: 页面未发现指定记录')

        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名为数字、字母、下划线、中杠线组成')
        payload4 = {
            "domain": domain1,
            "host": "_host123-new",
            "result": {"data": "6.6.6.6"}
        }
        r4 = self.post(url=url1, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 点击【记录管理】，查看步骤4添加的记录')
        self.authorization_enter_record_page()
        flag = self.authorization_find_specific_record(nodename=self.nodename[0],record="_host123-new." + domain1,type='A',res='6.6.6.6')
        if not flag:
            self.exception.add('Step5: 页面未发现指定记录')

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加A类型记录，主机名为*')
        payload6 = {
            "domain": domain1,
            "host": "*",
            "result": {"data": "6.6.6.6"}
        }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录，主机名为*')
        payload7 = {
                    "domain": domain1,
                    "host": "*",
                    "type": "AAAA",
                    "result": {"data": "111::222"}
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 200 and res7['code'] == "Success"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录，主机名为*')
        payload8 = {
                    "domain": domain1,
                    "host": "*",
                    "type": "MX",
                    "result": {"preference": 10, "data": "mail.qq.com"}
                    }
        r8 = self.post(url=url1, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success"):
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        print('Step9: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加IPV4反向域的PTR类型记录，主机名为*')
        payload9 = {
                    "domain": reverse_domain1,
                    "host": "5",
                    "type": "PTR",
                    "result": {"data": "5.test.com"}
                    }
        r9 = self.post(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加IPV6反向域的PTR类型记录，主机名为*')
        payload10 = {
                    "domain": reverse_domain2,
                    "host": "b",
                    "type": "PTR",
                    "result": {"data": "b.test.com"}
                    }
        r10 = self.post(url=url1, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success"):
                self.exception.add('Step10: ' + str(res10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名包含了特殊字符')
        payload11 = {
                    "domain": domain1,
                    "host": "*.t@3",
                    "result": {"data": "1.1.1.1"}
                    }
        r11 = self.post(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "InvalidParam"):
                self.exception.add('Step11: ' + str(res11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，CNAME类型的记录主机名为*')
        payload12 = {
                    "domain": domain1,
                    "host": "*",
                    "type": "CNAME",
                    "result": {"data": "www.qq.com"}
                    }
        r12 = self.post(url=url1, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "InvalidParam"):
                self.exception.add('Step12: ' + str(res12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，NS类型的记录主机名为*')
        payload13 = {
                    "domain": domain1,
                    "host": "*",
                    "type": "NS",
                    "result": {"data": "NS.qq.com"}
                    }
        r13 = self.post(url=url1, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 400 and res13['code'] == "InvalidParam"):
                self.exception.add('Step13: ' + str(res13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名包含下划线且在label的结尾')
        payload14 = {
                    "domain": domain1,
                    "host": "host_",
                    "result": {"data": "1.1.1.1"}
                    }
        r14 = self.post(url=url1, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "InvalidParam"):
                self.exception.add('Step14: ' + str(res14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名包含下划线且后面直接跟中杠线')
        payload15 = {
                    "domain": domain1,
                    "host": "_-host",
                    "result": {"data": "1.1.1.1"}
                    }
        r15 = self.post(url=url1, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "InvalidParam"):
                self.exception.add('Step15: ' + str(res15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名包含下划线，且一个label有一个以上的下划线')
        payload16 = {
                    "domain": domain1,
                    "host": "_h_ost",
                    "result": {"data": "1.1.1.1"}
                    }
        r16 = self.post(url=url1, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "InvalidParam"):
                self.exception.add('Step16: ' + str(res16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))

        print('Step17: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名包含中杠线且在label的开头')
        payload17 = {
            "domain": domain1,
            "host": "-host",
            "result": {"data": "1.1.1.1"}
        }
        r17 = self.post(url=url1, json=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 400 and res17['code'] == "InvalidParam"):
                self.exception.add('Step17: ' + str(res17))
        else:
            self.exception.add('Step17: ' + str(self.api_error))

        print('Step18: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，主机名中一个label超过63个字符')
        payload18 = {
            "domain": domain1,
            "host": "Assasasdsadsadsadasdasdasdasdsadsadsaddsdsadasdasdsadsdsd1234444",
            "result": {"data": "1.1.1.1"}
        }
        r18 = self.post(url=url1, json=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 400 and res18['code'] == "InvalidParam"):
                self.exception.add('Step18: ' + str(res18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))

        print('Step19: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv4反向域的域+主机名的label数超过6个')
        payload19 = {
            "domain": reverse_domain1,
            "host": "5.4",
            "type": "PTR",
            "result": {"data": "5.test.com"}
        }
        r19 = self.post(url=url1, json=payload19, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19, res19 = r19
            if not (status_code19 == 400 and res19['code'] == "InvalidParam"):
                self.exception.add('Step19: ' + str(res19))
        else:
            self.exception.add('Step19: ' + str(self.api_error))

        print('Step20: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv4反向域的主机名为负数')
        payload20 = {
            "domain": reverse_domain1,
            "host": "-1",
            "type": "PTR",
            "result": {"data": "6.test.com"}
        }
        r20 = self.post(url=url1, json=payload20, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code20, res20 = r20
            if not (status_code20 == 400 and res20['code'] == "InvalidParam"):
                self.exception.add('Step20: ' + str(res20))
        else:
            self.exception.add('Step20: ' + str(self.api_error))

        print('Step21: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv4反向域的主机名超过255')
        payload21 = {
            "domain": reverse_domain1,
            "host": "256",
            "type": "PTR",
            "result": {"data": "6.test.com"}
        }
        r21 = self.post(url=url1, json=payload21, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code21, res21 = r21
            if not (status_code21 == 400 and res21['code'] == "InvalidParam"):
                self.exception.add('Step21: ' + str(res21))
        else:
            self.exception.add('Step21: ' + str(self.api_error))

        print('Step22: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv4反向域的主机名为非数字')
        payload22 = {
            "domain": reverse_domain1,
            "host": "a",
            "type": "PTR",
            "result": {"data": "6.test.com"}
        }
        r22 = self.post(url=url1, json=payload22, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code22, res22 = r22
            if not (status_code22 == 400 and res22['code'] == "InvalidParam"):
                self.exception.add('Step22: ' + str(res22))
        else:
            self.exception.add('Step22: ' + str(self.api_error))

        print('Step23: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv6反向域的域名label总数超过34个')
        payload23 = {
            "domain": reverse_domain2,
            "host": "f.b",
            "type": "PTR",
            "result": {"data": "6.test.com"}
        }
        r23 = self.post(url=url1, json=payload23, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code23, res23 = r23
            if not (status_code23 == 400 and res23['code'] == "InvalidParam"):
                self.exception.add('Step23: ' + str(res23))
        else:
            self.exception.add('Step23: ' + str(self.api_error))

        print('Step24: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv6反向域的主机名为负数')
        payload24 = {
            "domain": reverse_domain2,
            "host": "-1",
            "type": "PTR",
            "result": {"data": "6.test.com"}
        }
        r24 = self.post(url=url1, json=payload24, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code24, res24 = r24
            if not (status_code24 == 400 and res24['code'] == "InvalidParam"):
                self.exception.add('Step24: ' + str(res24))
        else:
            self.exception.add('Step24: ' + str(self.api_error))

        print('Step25: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，ipv6反向域的主机名不在0-f范围内')
        payload25 = {
            "domain": reverse_domain2,
            "host": "g",
            "type": "PTR",
            "result": {"data": "6.test.com"}
        }
        r25 = self.post(url=url1, json=payload25, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code25, res25 = r25
            if not (status_code25 == 400 and res25['code'] == "InvalidParam"):
                self.exception.add('Step25: ' + str(res25))
        else:
            self.exception.add('Step25: ' + str(self.api_error))

        print('Step26: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，域名总长度超过255个字符内')
        payload26 = {
            "domain": domain1,
            "host": "a" * 256 ,
            "type": "A",
            "result": {"data": "1.1.1.1"}
        }
        r26 = self.post(url=url1, json=payload26, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code26, res26 = r26
            if not (status_code26 == 400 and res26['code'] == "InvalidParam"):
                self.exception.add('Step26: ' + str(res26))
        else:
            self.exception.add('Step26: ' + str(self.api_error))

        print('Step27: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，域名总长度超过255个字符内')
        payload27 = {
            "domain": domain1,
            "result": {"data": "1.1.1.1"}
        }
        r27 = self.post(url=url1, json=payload27, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code27, res27 = r27
            if not (status_code27 == 400 and res27['code'] == "InvalidHost"):
                self.exception.add('Step27: ' + str(res27))
        else:
            self.exception.add('Step27: ' + str(self.api_error))