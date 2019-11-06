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
        self.dhs_node_add_dns_node(nodename=self.nodename[0], device=self.devices[0:1])
        self.dhs_node_add_dns_node(nodename=self.nodename[1], device=self.devices[1:2])
        print('为节点%s添加api用户%s' % (self.nodename[0], self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(4)

    def tearDown(self):
        self.authorization_delete_all_domain()
        self.view_delete_all_view()
        self.view_delete_all_addr_group()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_modify_record_with_domainname(self):
        print('授权管理】-【域管理】中在node1下添加域yamu.com和反向 域3.2.1.in-addr.arpa,test视图下面添加yamu.com')
        view1 = "test"
        group1 = "group1"
        self.view_add_addr_group(gname=group1, ip=self.sourceip[1], mask="32")
        self.view_add_view(nodename=self.nodename[0], gname=group1, view=view1)

        domain1 = "yamu.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname=view1,
                                               ns_name=ns_name1, ns_ip=self.serverip[0])
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        domain_a = "3.2.1"
        arpa_type = "in-addr.arpa"
        reverse_domain = domain_a + "." + arpa_type
        self.authorization_add_reverse_domain(domainname=domain_a, arpa_type=arpa_type,
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)

        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="1.1.1.1")
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="2.2.2.2")
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="3.3.3.3")
        self.authorization_add_a_record(nodename=self.nodename[1], domain=domain1, host="www", res="1.1.1.1")
        self.authorization_add_a_record(nodename=self.nodename[1], domain=domain1, host="www", res="2.2.2.2")
        self.authorization_add_a_record(nodename=self.nodename[1], domain=domain1, host="www", res="3.3.3.3")
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="1.1.1.1", view=view1)
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="2.2.2.2", view=view1)
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="3.3.3.3",view=view1)
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="aaa", res="1.1.1.1")
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="aaa", res="2.2.2.2")
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="aaa", res="3.3.3.3")
        self.authorization_add_aaaa_record(nodename=self.nodename[0], domain=domain1, host="www", res="11::22")
        self.authorization_add_aaaa_record(nodename=self.nodename[0], domain=domain1, host="www", res="11::33")
        self.authorization_add_cname_record(nodename=self.nodename[0], domain=domain1, host="w1", res="www.yamu.com")
        self.authorization_add_cname_record(nodename=self.nodename[0], domain=domain1, host="w2", res="www.yamu.com")
        self.authorization_add_txt_record(nodename=self.nodename[0], domain=domain1, host="www", res="v=spf-1-all")
        self.authorization_add_mx_record(nodename=self.nodename[0], domain=domain1, host="mail", res="192.168.1.1", preference=10)
        self.authorization_add_mx_record(nodename=self.nodename[0], domain=domain1, host="mail", res="192.168.1.1", preference=20)
        self.authorization_add_mx_record(nodename=self.nodename[0], domain=domain1, host="mail", res="192.168.1.2", preference=10)
        self.authorization_add_ptr_record(nodename=self.nodename[0],domain=reverse_domain,host="4",res="4.yamu.com")
        self.authorization_add_ptr_record(nodename=self.nodename[0],domain=reverse_domain,host="5",res="5.yamu.com")


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records/name"

        print('Step1: ')
        payload1 = {
                    "domain":domain1,
                    "host":"www",
                    "type":"A",
                    "result":"1.1.1.1",
                    "update": {
                    "result": {"data": "7.7.7.7"}
                    }
                    }
        r1 = self.put(url=url1, json=payload1, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code1, res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success"):
                self.exception.add("Step1: " + str(r1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0],qname="www." + domain1,rdtype='A')
        if not self.error is None or not "7.7.7.7" in self.short:
            self.exception.add("Step1: A类型解析错误")

        print('Step2: ')
        payload2 = {
            "domain": domain1,
            "host": "aaa",
            "type": "A",
            "result": "1.1.1.1",
            "update": {
            "result": {"data": "8.8.8.8"}
            }
        }
        r2 = self.put(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add("Step2: " + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0], qname="aaa." + domain1, rdtype='A')
        if not self.error is None or not "8.8.8.8" in self.short:
            self.exception.add("Step2: A类型解析错误")

        print('Step3')
        payload3 = {
            "domain": domain1,
            "host": "www",
            "type": "AAAA",
            "result": "11::22",
            "update": {
            "result": {"data": "11::55"}
            }
        }
        r3 = self.put(url=url1, json=payload3,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code3,res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0], qname="www." + domain1, rdtype='AAAA')
        if not self.error is None or not "11::55" in self.short:
            self.exception.add("Step3: AAAA类型解析错误")


        print('Step4: ')
        payload4 = {
            "domain": domain1,
            "host": "w1",
            "type": "CNAME",
            "result": "www.yamu.com",
            "update": {
            "result": {"data": "ccc.yamu.com"}
            }
        }
        r4 = self.put(url=url1,json=payload4,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error) )

        sleep(15)

        self.query(service=self.serverip[0], qname="w1." + domain1, rdtype='CNAME')
        if not self.error is None or not "ccc.yamu.com." in self.short:
            self.exception.add("Step4: CNAME类型解析错误")


        print('Step5: ')
        payload5 = {
            "domain": domain1,
            "host": "www",
            "type": "TXT",
            "result": "v=spf-1-all",
            "update": {
            "result": {"data": "v=spf-8-all"}
            }
        }
        r5 = self.put(url=url1,json=payload5,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code5,res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0], qname="www." + domain1, rdtype='TXT')
        if not self.error is None or not '"v=spf-8-all"' in self.short:
            self.exception.add("Step5: TXT类型解析错误")

        print('Step6: ')
        payload6 = {
            "domain": domain1,
            "host": "mail",
            "type": "MX",
            "result": "10,192.168.1.1",
            "update": {
            "result": {"preference": 10,"data": "192.179.11.1"}
            }
        }
        r6 = self.put(url=url1, json=payload6,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success"):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0], qname="mail." + domain1, rdtype='MX')
        if not self.error is None or not "10 192.179.11.1." in self.short:
            self.exception.add("Step6: MX类型解析错误")

        print('Step7: ')
        payload7 = {
            "nodeName": self.nodename[1],
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3",
            "update": {
            "result": {"data": "9.9.9.9"}
            }
        }
        r7 = self.put(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 200 and res7['code'] == "Success"):
                self.exception.add('Step7: ' + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[1], qname="www." + domain1, rdtype='A')
        if not self.error is None or not "9.9.9.9" in self.short:
            self.exception.add("Step7: A类型解析错误")

        print('Step8: ')
        payload8 = {
            "viewName":view1,
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "1.1.1.1",
            "update": {
            "result": {"data": "10.10.10.10"}
            }
        }
        r8 = self.put(url=url1, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success"):
                self.exception.add('Step8: ' + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0], qname="www." + domain1, rdtype='A', source=self.sourceip[1])
        if not self.error is None or not "10.10.10.10" in self.short:
            self.exception.add("Step8: A类型解析错误")


        print('Step9: ')
        payload9 = {
            "domain": reverse_domain,
            "host": "4",
            "type": "PTR",
            "result": "4.yamu.com",
            "update": {
            "result": {"data": "11.yamu.com"}
            }
        }
        r9 = self.put(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add("Step9: " + str(r9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        sleep(15)

        self.query(service=self.serverip[0], qname="4." + reverse_domain, rdtype='PTR')
        if not self.error is None or not "11.yamu.com." in self.short:
            self.exception.add("Step9: PTR类型解析错误")

        print('Step10: ')
        payload10 = {
            "nodeName": "node10",
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "2.2.2.2",
            "update": {
            "result": {"data": "211.1.1.1"}
            }
        }
        r10 = self.put(url=url1, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 400 and res10['code'] == "NodeNotExisted"):
                self.exception.add('Step10: ' + str(r10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: ')
        payload11 = {
            "viewName":"test11",
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "2.2.2.2",
            "update": {
            "result": {"data": "211.1.1.1"}
            }
        }
        r11 = self.put(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "ViewNotExisted"):
                self.exception.add('Step11: ' + str(r11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: ')
        payload12 = {
            "domain": "baidu.com",
            "host": "www",
            "type": "A",
            "result": "2.2.2.2",
            "update": {
            "result": {"data": "211.1.1.1"}
            }
        }
        r12 = self.put(url=url1, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "ZoneNotExisted"):
                self.exception.add('Step12: ' + str(r12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: ')
        payload13 = {
            "domain": domain1,
            "host": "eee",
            "type": "A",
            "result": "2.2.2.2",
            "update": {
            "result": {"data": "211.1.1.1"}
            }
        }
        r13 = self.put(url=url1, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 400 and res13['code'] == "RecordNotExisted"):
                self.exception.add('Step13: ' + str(r13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: ')
        payload14 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "33.33.33.33",
            "update": {
            "result": {"data": "211.1.1.1"}
            }
        }
        r14 = self.put(url=url1, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "RecordNotExisted"):
                self.exception.add('Step14: ' + str(r14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: ')
        payload15 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "7.7.7.7",
            "update": {
            "result": {"data": "192.168.2.256"}
            }
        }
        r15 = self.put(url=url1, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "InvalidParam"):
                self.exception.add('Step15: ' + str(r15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: ')
        payload16 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "7.7.7.7",
            "update": {
            "result": {"data": "3.3.3.3"}
            }
        }
        r16 = self.put(url=url1, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "InvalidParam"):
                self.exception.add('Step16: ' + str(r16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))

        print('Step17: ')
        payload17 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3",
            "update": {
            "result": {"data": "3.3.3.3"},
            "weight": 5,
            "ttl": 360,
            "status": 0,
            "comment": "test"
            }
        }
        r17 = self.put(url=url1, json=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 200 and res17['code'] == "Success"):
                self.exception.add('Step17: ' + str(r17))
        else:
            self.exception.add('Step17: ' + str(self.api_error))


        print('Step18: ')
        payload18 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3",
            "update": {
            "result": {"data": "3.3.3.3"},
            "weight": 5000
            }
        }
        r18 = self.put(url=url1, json=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 400 and res18['code'] == "InvalidWeight"):
                self.exception.add('Step18: ' + str(r18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))

        print('Step19: ')
        payload19 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3",
            "update": {
            "result": {"data": "3.3.3.3"},
            "ttl": 8640001
            }
        }
        r19 = self.put(url=url1, json=payload19, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19, res19 = r19
            if not (status_code19 == 400 and res19['code'] == "InvalidTtl"):
                self.exception.add('Step19: ' + str(r19))
        else:
            self.exception.add('Step19: ' + str(self.api_error))

        print('Step20: ')
        payload20 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3",
            "update": {
            "result": {"data": "3.3.3.3"},
            "status": 2
            }
        }
        r20 = self.put(url=url1, json=payload20, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code20, res20 = r20
            if not (status_code20 == 400 and res20['code'] == "InvalidStatus"):
                self.exception.add('Step20: ' + str(r20))
        else:
            self.exception.add('Step20: ' + str(self.api_error))

        print('Step21: ')
        payload21 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3",
            "update": {
            "result": {"data": "3.3.3.3"},
            "comment": 'a' * 201
            }
        }
        r21 = self.put(url=url1, json=payload21, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code21, res21 = r21
            if not (status_code21 == 400 and res21['code'] == "InvalidComment"):
                self.exception.add('Step21: ' + str(r21))
        else:
            self.exception.add('Step21: ' + str(self.api_error))