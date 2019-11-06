from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.dnspage import dnspage
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource
from requests.auth import HTTPBasicAuth


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

    def test_query_sepcific_doamin(self):

        print('Step1: 在节点node1下添加视图v1')
        view1 = "v1"
        group1 = "group1"
        self.view_add_addr_group(gname=group1,ip="192.168.1.0",mask="24")
        self.view_add_view(nodename=self.nodename[0], gname=group1,view=view1)


        print('Step2: 点击【域管理】在节点node1下的defaul和v1视图下分别添加正向授权域test.com，在default视图下再添加反向授权域3.2.1.in-addr.arpa，在节点node2下添加正向授权域yamu.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname=view1,
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        reverse_domain = "3.2.1"
        self.authorization_add_reverse_domain(domainname=reverse_domain, arpa_type="in-addr.arpa",
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)

        domain2 = "yamu.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])


        print('Step3: 点击【记录管理】添加各种记录，如 附件截图所示')

        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="1.1.1.1", view='default')
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="2.2.2.2", view=view1)

        self.authorization_add_aaaa_record(nodename=self.nodename[0],domain=domain1,host="www",res="11::22")
        self.authorization_add_aaaa_record(nodename=self.nodename[0], domain=domain1, host="www", res="11::22",view=view1)

        self.authorization_add_mx_record(nodename=self.nodename[0],domain=domain1,host="",res="mail.test.com")
        self.authorization_add_mx_record(nodename=self.nodename[0], domain=domain1, host="", res="mail.test.com", view=view1)

        self.authorization_add_cname_record(nodename=self.nodename[0], domain=domain1,host="c",res="www.test.com")
        self.authorization_add_cname_record(nodename=self.nodename[0], domain=domain1, host="c", res="www.test.com",view=view1)

        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"
        print('Step4: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？nodeName=node100，指定查询的节见不存在，查看返回结果')
        payload4 = {
                     "nodeName": "node100"
                    }
        r4 = self.get(url=url1,params=payload4,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 400 and res4['code'] == "NodeNotExisted"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？nodeName=node1')
        payload5 = {
            "nodeName": self.nodename[0]
        }
        r5 = self.get(url=url1, params=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if status_code5 == 200 and res5['code'] == "Success" and len(res5['data']) == 13:
                for zone in res5['data']:
                    nodename5 = zone.get('nodeName')
                    if not (nodename5 == self.nodename[0]):
                        self.exception.add('Step5: ' + str(res5))
            else:
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))


        print('Step6: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？nodeName=node2，指定nodeName不是api用户所在的节点')
        payload6 = {
            "nodeName": self.nodename[1]
        }
        r6 = self.get(url=url1, params=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if status_code6 == 200 and res6['code'] == "Success" and len(res6['data']) == 2:
                for zone in res6['data']:
                    nodename6 = zone.get('nodeName')
                    if not (nodename6 == self.nodename[1]):
                        self.exception.add('Step6: ' + str(res6))
            else:
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？viewName=v123，指定的视图不存在，查看返回结果')
        payload7 = {
            "viewName": "v123"
        }
        r7 = self.get(url=url1, params=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 200 and res7['code'] == "Success" and len(res7['data']) == 0):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？viewName=default，指定的视图存在，查看返回结果')
        payload8 = {
            "viewName": "default"
        }
        r8 = self.get(url=url1, params=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if status_code8 == 200 and res8['code'] == "Success" and len(res8['data']) == 7:
                for zone in res8['data']:
                    viewname8 = zone.get('viewName')
                    if not (viewname8 == "default"):
                        self.exception.add('Step8: ' + str(res8))
            else:
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))


        print('Step9: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？domain=3.2.1.in-addr.arpa，授权域存在，查看返回结果')
        payload9 = {
            "domain": "3.2.1.in-addr.arpa"
        }
        r9 = self.get(url=url1, params=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success" and len(res9['data']) == 1):
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))


        print('Step10: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？domain=abc.com，授权域不存在，查看返回结果')
        payload10 = {
            "domain": "abc.com"
        }
        r10 = self.get(url=url1, params=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success" and len(res10['data']) == 0):
                self.exception.add('Step10: ' + str(res10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))


        print('Step11: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？domain=test.com，授权域存在与多个视图下，查看返回结果')
        payload11 = {
            "domain": domain1
        }
        r11 = self.get(url=url1, params=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if status_code11 == 200 and res11['code'] == "Success" and len(res11['data']) == 12:
                for zone in res11['data']:
                    domainname11 = zone.get('domain')
                    if not (domainname11 == domain1):
                        self.exception.add('Step11: ' + str(res11))
            else:
                self.exception.add('Step11: ' + str(res11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？host=ftp，主机名不存在，查看返回结果')
        payload12 = {
            "host": "ftp"
        }
        r12 = self.get(url=url1, params=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 200 and res12['code'] == "Success" and len(res12['data']) == 0):
                self.exception.add('Step12: ' + str(res12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？host=www，主机名存在，查看返回结果')
        payload13 = {
            "host": "www"
        }
        r13 = self.get(url=url1, params=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if status_code13 == 200 and res13['code'] == "Success" and len(res13['data']) == 4:
                for zone in res13['data']:
                    host13 = zone.get('host')
                    if not (host13 == "www." + domain1):
                        self.exception.add('Step13: ' + str(res13))
            else:
                self.exception.add('Step13: ' + str(res13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))


        print('Step14: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？start=0，从第一页开始查询，查看返回结果')
        payload14 = {
            "start": "0"
        }
        r14 = self.get(url=url1, params=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 200 and res14['code'] == "Success" and len(res14['data']) == 13):
                self.exception.add('Step14: ' + str(res14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？start=1，从不存在的页码开始查询，查看返回结果')
        payload15 = {
            "start": "100"
        }
        r15 = self.get(url=url1, params=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 200 and res15['code'] == "Success" and len(res15['data']) == 0):
                self.exception.add('Step15: ' + str(res15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？length=10，指定每页显示的条数，查看返回结果')
        payload16 = {
            "length": "10"
        }
        r16= self.get(url=url1, params=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 200 and res16['code'] == "Success" and len(res16['data']) == 10):
                self.exception.add('Step16: ' + str(res16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))

        print('Step17: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records？length=1000，指定的每页显示条数值不存在，查看返回结果')
        payload17 = {
            "length": "1000"
        }
        r17 = self.get(url=url1, params=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 200 and res17['code'] == "Success" and len(res17['data']) == 13):
                self.exception.add('Step17: ' + str(res17))
        else:
            self.exception.add('Step17: ' + str(self.api_error))

        print('Step18: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records?nodeName=node1&viewName=v1&domain=test.com&host=wwwstart=0&length=10，指定查询参数，查看返回结果')
        payload18 = {
            "nodeName": self.nodename[0],
            "viewName": view1,
            "domain": domain1,
            "host": "www",
            "start": "0",
            "length": "10"
        }
        r18 = self.get(url=url1, params=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if status_code18 == 200 and res18['code'] == "Success" and len(res18['data']) == 2:
                for zone in res18['data']:
                    nodename18 = zone.get('nodeName')
                    viewname18 = zone.get('viewName')
                    host18 = zone.get('host')
                    if not (nodename18 == self.nodename[0] and viewname18 == view1 and host18 == 'www.' + domain1):
                        self.exception.add('Step18: ' + str(res18))
            else:
                self.exception.add('Step18: ' + str(res18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))


        print('Step19: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records/5badea702a86c0a7516c042e，指定授权域的ID进行查询且该ID存在，查看返回结果（可先查出所有的授权域，根据结果中的id进行查询）')
        payload19 = {
            "viewName": view1
        }
        r19a = self.get(url=url1, params=payload19, auth=(self.api_user, self.api_password))
        id = ""
        if self.api_error is None:
            status_code19a, res19a = r19a
            if status_code19a == 200 and res19a["code"] == "Success" and len(res19a['data']) > 0:
                id = res19a['data'][0].get('id')
            else:
                self.exception.add("Step19a:" + str(res19a))
        else:
            self.exception.add("Step19a: " + self.api_error)
        url2 = url1 + "/" + str(id)
        r19b = self.get(url=url2,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19b,res19b = r19b
            if not (status_code19b == 200 and res19b['code'] == "Success"):
                self.exception.add('Step19b ' + str(res19b))
        else:
            self.exception.add('Step19b ' + str(self.api_error))

        print('Step20: 用GET方法调用接口https://192.168.6.62:19393/api/dns/records/123456，指定授权域的ID进行查询且该ID不存在，查看返回结果')
        url3 = url1 + "/123456"
        r20 = self.get(url=url3,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code20,res20 = r20
            if not (status_code20 == 400 and res20['code'] == 'RecordNotExisted'):
                self.exception.add('Step20: ' + str(res20))
        else:
            self.exception.add('Step20: ' + str(self.api_error))
