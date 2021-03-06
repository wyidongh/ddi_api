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
        self.view_delete_all_view()
        self.view_delete_all_addr_group()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_query_record_with_domainname(self):
        print('授权管理】-【域管理】中在node1下添加域yamu.com和反向 域3.2.1.in-addr.arpa,test视图下面添加yamu.com')
        view1 = "test"
        group1 = "group1"
        self.view_add_addr_group(gname=group1, ip="192.168.6.0", mask="24")
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

        print('Step1: GET https://192.168.16.109:19393/api/dns/records/name?&domain=yamu.com&host=www&type=A&result=1.1.1.1')
        payload1 = {
                    "domain":domain1,
                    "host":"www",
                    "type":"A",
                    "result":"1.1.1.1"
                    }
        r1 = self.get(url=url1, params=payload1, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code1, res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success" and res1['data'] is not None):
                self.exception.add("Step1: " + str(r1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))


        print('Step2: GET https://192.168.16.109:19393/api/dns/records/name?&domain=yamu.com&host=www&type=a&result=1.1.1.1')
        payload2 = {
            "domain": domain1,
            "host": "www",
            "type": "a",
            "result": "1.1.1.1"
        }
        r2 = self.get(url=url1, params=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 400 and res2['code'] == "InvalidType"):
                self.exception.add("Step2: " + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))


        print('Step3: GET https://192.168.16.109:19393/api/dns/records/name?&domain=yamu.com&host=&type=A&result=3.3.3.3')
        payload3 = {
            "domain": domain1,
            "host": "",
            "type": "A",
            "result": "3.3.3.3"
        }
        r3 = self.get(url=url1, params=payload3,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code3,res3 = r3
            if not (status_code3 == 400 and res3['code'] == "RecordNotExisted"):
                self.exception.add('Step3: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))


        print('Step4: GET https://192.168.16.109:19393/api/dns/records/name?&domain=yamu.com&type=A&result=2.2.2.2')
        payload4 = {
            "domain": domain1,
            "type": "A",
            "result": "2.2.2.2"
        }
        r4 = self.get(url=url1,params=payload4,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 400 and res4['code'] == "RecordNotExisted"):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error) )

        print('Step5: GET https://192.168.16.109:19393/api/dns/records/name?&domain=yamu.com&host=*&type=A&result=2.2.2.2')
        payload5 = {
            "domain": domain1,
            "host": "*",
            "type": "A",
            "result": "2.2.2.2"
        }
        r5 = self.get(url=url1,params=payload5,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code5,res5 = r5
            if not (status_code5 == 400 and res5['code'] == "RecordNotExisted"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))


        print('Step6: GET https://192.168.16.109:19393/api/dns/records/name?&domain=yamu.com&host=aaa&type=A&result=2.2.2.2')
        payload6 = {
            "domain": domain1,
            "host": "aaa",
            "type": "A",
            "result": "2.2.2.2"
        }
        r6 = self.get(url=url1, params=payload6,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success" and res6['data'] is not None):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))


        print('Step7: GET https://192.168.16.109:19393/api/dns/records/name?domain=yamu.com&host=www&type=AAAA&result=11::22')
        payload7 = {
            "domain": domain1,
            "host": "www",
            "type": "AAAA",
            "result": "11::22"
        }
        r7 = self.get(url=url1, params=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 200 and res7['code'] == "Success" and res7['data'] is not None):
                self.exception.add('Step7: ' + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))


        print('Step8: GET https://192.168.16.109:19393/api/dns/records/name?domain=yamu.com&host=w1&type=CNAME&result=www.yamu.com')
        payload8 = {
            "domain": domain1,
            "host": "w1",
            "type": "CNAME",
            "result": "www.yamu.com"
        }
        r8 = self.get(url=url1, params=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success" and res8['data'] is not None):
                self.exception.add('Step8: ' + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))


        print('Step9: GET https://192.168.16.109:19393/api/dns/records/name?domain=yamu.com&host=www&type=TXT&result="v=spf-1-all"')
        payload9 = {
            "domain": domain1,
            "host": "www",
            "type": "TXT",
            "result": "v=spf-1-all"
        }
        r9 = self.get(url=url1, params=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success" and res9['data'] is not None):
                self.exception.add("Step9: " + str(r9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))


        print('Step10: GET https://192.168.16.109:19393/api/dns/records/name?domain=yamu.com&host=mail&type=MX&result=10,192.168.1.1')
        payload10 = {
            "domain": domain1,
            "host": "mail",
            "type": "MX",
            "result": "10,192.168.1.1"
        }
        r10 = self.get(url=url1, params=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success" and res10['data'] is not None):
                self.exception.add('Step10: ' + str(r10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: https://192.168.16.109:19393/api/dns/records/name?nodeNmae=node2&domain=yamu.com&host=www&type=A&result=3.3.3.3')
        payload11 = {
            "nodeName":self.nodename[1],
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3"
        }
        r11 = self.get(url=url1, params=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 200 and res11['code'] == "Success" and res11['data'] is not None):
                self.exception.add('Step11: ' + str(r11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: GET https://192.168.16.109:19393/api/dns/records/name?viewName=test&domain=test.com&host=www&type=A&result=1.1.1.1')
        payload12 = {
            "viewName": view1,
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "1.1.1.1"
        }
        r12 = self.get(url=url1, params=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 200 and res12['code'] == "Success" and res12['data'] is not None):
                self.exception.add('Step12: ' + str(r12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: GET https://192.168.16.109:19393/api/dns/records/name?&domain=3.2.1.in-addr.arpa&host=4&type=PTR&result=4.yamu.com')
        payload13 = {
            "domain": reverse_domain,
            "host": "4",
            "type": "PTR",
            "result": "4.yamu.com"
        }
        r13 = self.get(url=url1, params=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 200 and "Success" and res13['data'] is not None):
                self.exception.add('Step13: ' + str(r13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: https://192.168.16.109:19393/api/dns/records/name?nodeName=node10&domain=yamu.com&host=www&type=A&result=3.3.3.3')
        payload14 = {
            "nodeName": "node10",
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "3.3.3.3"
        }
        r14 = self.get(url=url1, params=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "NodeNotExisted"):
                self.exception.add('Step14: ' + str(r14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: GET https://192.168.16.109:19393/api/dns/records/name?viewName=test10&domain=test.com&host=www&type=A&result=1.1.1.1')
        payload15 = {
            "viewName": "test15",
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "1.1.1.1"
        }
        r15 = self.get(url=url1, params=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "ViewNotExisted"):
                self.exception.add('Step15: ' + str(r15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: GET https://192.168.16.109:19393/api/dns/records/name?domain=baidu.com&host=www&type=A&result=1.1.1.1')
        payload16 = {
            "domain": "baidu.com",
            "host": "www",
            "type": "A",
            "result": "1.1.1.1"
        }
        r16 = self.get(url=url1, params=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "ZoneNotExisted"):
                self.exception.add('Step16: ' + str(r16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))

        print('Step17: GET https://192.168.16.109:19393/api/dns/records/name?domain=yamu.com&host=abc&type=A&result=1.1.1.1')
        payload17 = {
            "domain": domain1,
            "host": "abc",
            "type": "A",
            "result": "1.1.1.1"
        }
        r17 = self.get(url=url1, params=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 400 and res17['code'] == "RecordNotExisted"):
                self.exception.add('Step17: ' + str(r17))
        else:
            self.exception.add('Step17: ' + str(self.api_error))


        print('Step18: GET https://192.168.16.109:19393/api/dns/records/name?domain=yamu.com&host=www&type=A&result=8.8.8.8')
        payload18 = {
            "domain": domain1,
            "host": "www",
            "type": "A",
            "result": "8.8.8.8"
        }
        r18 = self.get(url=url1, params=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 400 and res18['code'] == "InvalidResourceResult"):
                self.exception.add('Step18: ' + str(r18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))
