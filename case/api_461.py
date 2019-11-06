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


    def test_query_sepcific_doamin(self):
        url1 = "https://" + self.serverip[0] + ":19393/api/dns/zones"

        print('Step1: 点击【域管理】在节点node1下添加正向授权域yamu.com和反向授权域3.2.1.in-addr.arpa，在节点node2下添加正向授权域test.com')
        domain1 = "yamu.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])
        print('添加反向域3.2.1.in-addr.arpa')
        reverse_domain = "3.2.1"
        self.authorization_add_reverse_domain(domainname=reverse_domain, arpa_type="in-addr.arpa",
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)

        domain2 = "test.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])

        print('Step2: 点【视图管理】在节点node1下添加视图v1')
        view1 = "view1"
        self.view_add_addr_group("group1",ip="1.1.1.0",mask=24)
        self.view_add_view(nodename=self.nodename[0],view=view1,gname="group1")

        print('Step3: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones，不指定任何参数，默在api用户所在的节点下所有视图下查询，查看返回结果')
        r3 = self.get(url=url1,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code3,res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success" and len(res3['data']) > 0):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add("Step3: "+ self.api_error)

        print('Step4: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？nodeName=node1，指定nodeName为api用户所在的节点，查看返回结果')
        payload4 = {"nodeName":self.nodename[0]}
        r4 = self.get(url=url1,params=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if (status_code4 == 200 and res4['code'] == "Success" and len(res4['data']) == 2):
                for zone in res4['data']:
                    nodename = zone.get('nodeName')
                    if nodename != self.nodename[0]:
                        self.exception.add('Step4:' + str(res4))
            else:
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add("Step4: " + self.api_error)

        print('Step5: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？nodeName=node2，指定nodeName不是api用户所在的节点，查看返回结果')
        payload5 = {"nodeName": self.nodename[1]}
        r5 = self.get(url=url1, params=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if (status_code5 == 200 and res5['code'] == "Success"):
                for zone in res5['data']:
                    nodename = zone.get('nodeName')
                    domainname = zone.get('domain')
                    if not (nodename == self.nodename[1] and domainname == domain2) :
                        self.exception.add('Step5:' + str(res5))
            else:
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add("Step5: " + self.api_error)

        print('Step6: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？viewName=v123，指定的视图不存在，查看返回结果')
        payload6 = {"viewName": "v123"}
        r6 = self.get(url=url1, params=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success" and len(res6['data']) == 0):
                self.exception.add("Step6: " + str(res6))
        else:
            self.exception.add("Step6: " + self.api_error)

        print('Step7: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？viewName=default，指定的视图存在，查看返回结果')
        payload7 = {"viewName": "default"}
        r7 = self.get(url=url1, params=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if (status_code7 == 200 and res7['code'] == "Success" and len(res7['data']) == 2):
                for zone in res7['data']:
                    nodename = zone.get('nodeName')
                    viewname = zone.get('viewName')
                    if nodename != self.nodename[0] or viewname != "default":
                        self.exception.add('Step7:' + str(res7))
            else:
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add("Step7: " + self.api_error)

        print('Step8: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？viewName=default，指定的视图存在但没有视图下没有授权域，查看返回结果')
        payload8 = {"viewName": view1}
        r8 = self.get(url=url1, params=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success" and len(res8['data']) == 0):
                self.exception.add("Step8: " + str(res8))
        else:
            self.exception.add("Step8: " + self.api_error)

        print('Step9: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？domain=yamu.com，授权域存在，查看返回结果')
        payload9 = {"domain": domain1}
        r9 = self.get(url=url1, params=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if (status_code9 == 200 and res9['code'] == "Success" and len(res9['data']) == 1):
                for zone in res9['data']:
                    domainname = zone.get('domain')
                    if domainname != domain1 :
                        self.exception.add('Step9:' + str(res9))
            else:
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add("Step9: " + self.api_error)

        print('Step10: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？domain=abc.com，授权域不存在，查看返回结果')
        payload10 = {"domain": "abc.com"}
        r10 = self.get(url=url1, params=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success" and len(res10['data']) == 0):
                self.exception.add("Step10: " + str(res10))
        else:
            self.exception.add("Step10: " + self.api_error)

        print('Step11: 点击【域管理】，在节点node1的视图v1下再添加授权域yamu.com')
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname=view1,
                                               ns_name=ns_name1, ns_ip=self.serverip[0])


        print('Step12: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？domain=test.com，授权域存在，查看返回结果')
        payload12 = {"domain":domain1}
        r12 = self.get(url=url1, params=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if (status_code12 == 200 and res12['code'] == "Success" and len(res12['data']) == 2):
                for zone in res12['data']:
                    viewname = zone.get('viewName')
                    domainname = zone.get('domain')
                    if not domainname == domain1:
                        self.exception.add('Step12:' + str(res12))
            else:
                self.exception.add('Step12: ' + str(res12))
        else:
            self.exception.add("Step12: " + self.api_error)

        print('Step13: 点击【域管理】，在节点node1的视图default下再添加授权域123.com和sss.com.cn')
        domain3 = "123.com"
        domain4 = "ss.com.cn"
        ns_name3 = "ns" + domain3
        ns_name4 = "ns." + domain4
        self.authorization_add_standard_domain(domainname=domain3, nodename=self.nodename[0], viewname="default",
                                               ns_name=ns_name3, ns_ip=self.serverip[0])
        self.authorization_add_standard_domain(domainname=domain4, nodename=self.nodename[0], viewname="default",
                                               ns_name=ns_name4, ns_ip=self.serverip[0])


        print('Step14: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？domain=com，根据域名进行模糊匹配，查看返回结果')
        payload14 = {"domain": "com"}
        r14 = self.get(url=url1, params=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if (status_code14 == 200 and res14['code'] == "Success" and len(res14['data']) == 4):
                for zone in res14['data']:
                    domainname = zone.get('domain')
                    if "com" not in str(domainname):
                        self.exception.add('Step14:' + str(res14))
            else:
                self.exception.add('Step14: ' + str(res14))
        else:
            self.exception.add("Step14: " + self.api_error)

        print('Step15: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？start=0，从第一页开始查询，查看返回结果')
        payload15 = {"start": "0"}
        r15 = self.get(url=url1, params=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 200 and res15['code'] == "Success" and len(res15['data']) == 5):
                self.exception.add('Step15: ' + str(res15))
        else:
            self.exception.add("Step15: " + self.api_error)

        print('Step16: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？start=1，从不存在的页码开始查询，查看返回结果')
        payload16 = {"start": "1"}
        r16 = self.get(url=url1, params=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 200 and res16['code'] == "Success" and len(res16['data']) == 0):
                self.exception.add('Step16: ' + str(res16))
        else:
            self.exception.add("Step16: " + self.api_error)


        print('Step17: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？length=10，指定每页显示的条数，查看返回结果')
        payload17 = {"length": "10"}
        r17 = self.get(url=url1, params=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 200 and res17['code'] == "Success" and len(res17['data']) == 5):
                self.exception.add('Step17: ' + str(res17))
        else:
            self.exception.add("Step17: " + self.api_error)

        print('Step18: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？length=1000，指定的每页显示条数值不存在，查看返回结果')
        payload18 = {"length": "1000"}
        r18 = self.get(url=url1, params=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 200 and res18['code'] == "Success" and len(res18['data']) == 5):
                self.exception.add('Step18: ' + str(res18))
        else:
            self.exception.add("Step18: " + self.api_error)



        print('Step19: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones?nodeName=node1&viewName=v1&domain=yamu.com&start=0&length=25，指定查询参数，查看返回结果')
        payload19 = {"length": "25",
                     "nodeName": self.nodename[0],
                     "viewName": view1,
                     "domain": domain1,
                     "start": "0"
                     }
        r19 = self.get(url=url1, params=payload19, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19, res19 = r19
            if (status_code19 == 200 and res19['code'] == "Success"):
                for zone in res19['data']:
                    nodename = zone.get('nodeName')
                    viewname = zone.get('viewName')
                    domainname = zone.get('domain')
                    if not (nodename == self.nodename[0] and viewname == view1 and domainname == domain1):
                        self.exception.add('Step19: ' + str(res19))
            else:
                self.exception.add('Step19: ' + str(res19))
        else:
            self.exception.add("Step19: " + self.api_error)


        print('Step20: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones/5baa0ba5f580523d1986bd5c，指定授权域的ID进行查询且该ID存在，查看返回结果')
        r20a = self.get(url=url1, auth=(self.api_user, self.api_password))
        id = ""
        if self.api_error is None:
            status_code20a,res20a = r20a
            for zone in res20a["data"]:
                domainname = zone.get("domain")
                viewname = zone.get('viewName')
                if domainname == domain1 and viewname == "default" :
                    id = zone.get("id")
                    break
                else:
                    continue
            if not (status_code20a == 200 and res20a["code"] == "Success" and bool(id)):
                self.exception.add("Step20a:" + str(res20a))
        else:
            self.exception.add("Step20a: " + self.api_error)

        url2 = url1 + "/" + str(id)
        r20b = self.get(url=url2,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code20b,res20b = r20b
            if not (status_code20b == 200 and res20b['code'] == "Success"):
                self.exception.add("Step20b: " + str(res20b))
        else:
            self.exception.add("Step20b: " + str(self.api_error))


        print('Step21: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones/123456，指定授权域的ID进行查询且该ID不存在，查看返回结果')
        url3 = url1 + "/" + "123456"
        r21 = self.get(url=url3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code21, res21 = r21
            if not (status_code21 == 400 and res21['code'] == "ZoneNotExisted"):
                self.exception.add("Step21: " + str(res21))
        else:
            self.exception.add("Step21: " + str(self.api_error))




        #添加域test1.com-test7.com
        for i in range(1,8):
            domain = "test" + str(i) + ".com"
            ns_name = "ns." + domain
            print('开始添加域: %s' % domain)
            self.authorization_add_standard_domain(domainname=domain, nodename=self.nodename[0], viewname='default',
                                                   ns_name=ns_name, ns_ip=self.serverip[0])

        sleep(2)
        print('Step22: 点击【域管理】页面，一共显示节点node1下一共有12个域，分别为yamu.com-default、3.2.1.in-addr.arpa、yamu.com-v1、123.com、sss.com.cn、test1.com到test7.com')
        self.authorization_enter_domain_page()
        domain_count = self.authorization_get_domain_count(nodename=self.nodename[0])
        if not (domain_count == 12):
            self.exception.add("Step22,域数量" + str(domain_count) )


        print('Step23: 用GET方法调用接口https://192.168.6.62:19393/api/dns/zones？start=1&length=10，从第二页开始查，查看返回结果')
        payload23 = {"start": "1",
                     "length": "10"}
        r23 = self.get(url=url1, params=payload23, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code23, res23 = r23
            if not (status_code23 == 200 and res23['code'] == "Success" and len(res23['data']) == 2):
                self.exception.add('Step23: ' + str(res23))
        else:
            self.exception.add("Step23: " + self.api_error)

































