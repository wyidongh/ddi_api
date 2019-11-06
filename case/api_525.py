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

    def test_modify_record_result(self):

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

        print('Step4: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bbf19928889ee7be5a92367接口，将r1.test.com的A解析结果修改为1.2.3.4')
        payload4 = {"result" : {"data": "1.2.3.4"}}
        r4 = self.put(url=url2,json=payload4,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error) )


        print('Step5: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bbf19928889ee7be5a92367接口，将r1.test.com的A解析结果修改为-1.2.3.4')
        payload5 = {"result": {"data": "-1.2.3.4"}}
        r5 = self.put(url=url2,json=payload5,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code5,res5 = r5
            if not (status_code5 == 400 and res5['code'] == "InvalidParam"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bbf19928889ee7be5a92367接口，将r1.test.com的A解析结果修改为1.2.3.256')
        payload6 = {"result": {"data": "1.2.3.256"}}
        r6 = self.put(url=url2, json=payload6,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidParam"):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 点击【记录管理】，新增r5.test.com的aaaa的解析结果为11::22')
        self.authorization_add_aaaa_record(nodename=self.nodename[0],domain=domain1,host="r5",res="11::22",weight=1,ttl=100)

        print('Step8: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=test.com&host=r5接口，查出步骤7中记录的id')
        payload8 = {
            "domain": domain1,
            "host": "r5",
            "type": "AAAA"
        }
        r8 = self.get(url=url1, params=payload8, auth=(self.api_user, self.api_password))
        id2 = ""
        if self.api_error is None:
            status_code8, res8 = r8
            if status_code8 == 200 and res8['code'] == "Success" and len(res8['data']) == 1:
                id2 = res8['data'][0]['id']
            else:
                self.exception.add('Step8: ' + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        url3 = url1 + "/" + str(id2)

        print('Step9: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为f0ea::')
        payload9 = {"result": {"data": "f0ea::"}}
        r9 = self.put(url=url3, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add("Step9: " + str(r9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为::')
        payload10 = {"result": {"data": "::"}}
        r10 = self.put(url=url3, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success"):
                self.exception.add('Step10: ' + str(r10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为1111:2222::3333:4444:5555:6666:7777:8888')
        payload11 = {"result": {"data": "1111:2222:3333:4444:5555:6666:7777:8888"}}
        r11 = self.put(url=url3, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 200 and res11['code'] == "Success"):
                self.exception.add('Step11: ' + str(r11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为不合法超过8段')
        payload12 = {"result": {"data": "1111:2222:3333:4444:5555:6666:7777:8888:ffff"}}
        r12 = self.put(url=url3, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "InvalidParam"):
                self.exception.add('Step12: ' + str(r12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为不合法，缩写格式错误')
        payload13 = {"result": {"data": "11::22::"}}
        r13 = self.put(url=url3, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 400 and res13['code'] == "InvalidParam"):
                self.exception.add('Step13: ' + str(r13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为不合法，label取值不合法')
        payload14 = {"result": {"data": "11::fg"}}
        r14 = self.put(url=url3, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "InvalidParam"):
                self.exception.add('Step14: ' + str(r14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc0033c8889ee7be5a92384接口，将r5.test.com的AAAA解析结果修改为不合法，label取值不合法')
        payload15 = {"result": {"data": "11::-1"}}
        r15 = self.put(url=url3, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "InvalidParam"):
                self.exception.add('Step15: ' + str(r15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 点击【记录管理】，添加s1.test.com的ns记录为ns1.test.com')
        self.authorization_add_ns_record(nodename=self.nodename[0],domain=domain1,host="s1",res="ns1.test.com")

        print('Step17: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=test.com&host=s1接口，查出步骤16中记录的id')
        payload17 = {
            "domain": domain1,
            "host": "s1",
            "type": "NS"
        }
        r17 = self.get(url=url1, params=payload17, auth=(self.api_user, self.api_password))
        id3 = ""
        if self.api_error is None:
            status_code17, res17 = r17
            if status_code17 == 200 and res17['code'] == "Success" and len(res17['data']) == 1:
                id3 = res17['data'][0]['id']
            else:
                self.exception.add('Step17: ' + str(r17))
        else:
            self.exception.add('Step17: 获取指定记录ID失败' + str(self.api_error))

        url4 = url1 + "/" + str(id3)

        print('Step18: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc00a008889ee7be5a923a8接口，将s1.test.com的NS解析结果修改为其他合法的域名')
        payload18 = {"result": {"data": "_dns-1.test.com"}}
        r18 = self.put(url=url4, json=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 200 and res18['code'] == "Success"):
                self.exception.add('Step18: ' + str(r18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))

        print('Step19: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc00a008889ee7be5a923a8接口，将s1.test.com的NS解析结果修改为不合法的域名')
        payload19 = {"result": {"data": "^*=.dns.test.com"}}
        r19 = self.put(url=url4, json=payload19, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19, res19 = r19
            if not (status_code19 == 400 and res19['code'] == "InvalidParam"):
                self.exception.add('Step19: ' + str(r19))
        else:
            self.exception.add('Step19: ' + str(self.api_error))

        print('Step20: 点击【记录管理】，添加www.test.com和www1.test.com的A记录解析结果为1.1.1.1')
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www", res="1.1.1.1", weight=1,ttl=100)
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="www1", res="1.1.1.1", weight=1,ttl=100)

        print('Step21: 点击【记录管理】，添加cn1.test.com的cname记录解析结果为www.test.com')
        self.authorization_add_cname_record(nodename=self.nodename[0],domain=domain1,host="cn1",res="www.test.com")

        print('Step22: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=test.com&host=cn1接口，查出步骤16中记录的id')
        payload22 = {
            "domain": domain1,
            "host": "cn1",
            "type": "CNAME"
        }
        r22 = self.get(url=url1, params=payload22, auth=(self.api_user, self.api_password))
        id4 = ""
        if self.api_error is None:
            status_code22, res22 = r22
            if status_code22 == 200 and res22['code'] == "Success" and len(res22['data']) == 1:
                id4 = res22['data'][0]['id']
            else:
                self.exception.add('Step22: ' + str(r22))
        else:
            self.exception.add('Step22:' + str(self.api_error))

        url5 = url1 + "/" + str(id4)

        print('Step23: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc048bb8889ee7be5a923ca接口，将cn1.test.com的CNAME解析结果修改为本域存在的另一个域名')
        payload23 = {"result": {"data": "www1.test.com"}}
        r23 = self.put(url=url5, json=payload23, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code23, res23 = r23
            if not (status_code23 == 200 and res23['code'] == "Success"):
                self.exception.add('Step23: ' + str(r23))
        else:
            self.exception.add('Step23: ' + str(self.api_error))

        print('Step24: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc048bb8889ee7be5a923ca接口，将cn1.test.com的CNAME解析结果修改为非本域的域名')
        payload24 =  {"result": {"data": "www.qq.com"}}
        r24 = self.put(url=url5, json=payload24, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code24, res24 = r24
            if not (status_code24 == 200 and res24['code'] == "Success"):
                self.exception.add('Step24: ' + str(r24))
        else:
            self.exception.add('Step24: ' + str(self.api_error))

        print('Step25: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc048bb8889ee7be5a923ca接口，将cn1.test.com的CNAME解析结果修改为本域不存的域名')
        """
        2.2.1以后版本CNAME记录允许添加本域不存在的域名
        """

        payload25 = {"result": {"data": "www123.test.com"}}
        r25 = self.put(url=url5, json=payload25, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code25, res25 = r25
            if not (status_code25 == 200 and res25['code'] == "Success"):
                self.exception.add('Step25: ' + str(r25))
        else:
            self.exception.add('Step25: ' + str(self.api_error))

        print('Step26: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc048bb8889ee7be5a923ca接口，将cn1.test.com的CNAME解析结果修改为非法的域名')
        payload26 = {"result": {"data": "_&-www_.qq.com"}}
        r26 = self.put(url=url5, json=payload26, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code26, res26 = r26
            if not (status_code26 == 400 and res26['code'] == "InvalidParam"):
                self.exception.add('Step26: ' + str(r26))
        else:
            self.exception.add('Step26: ' + str(self.api_error))

        print('Step27: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc048bb8889ee7be5a923ca接口，将cn1.test.com的CNAME解析结果修改为本域中只存在NS记录的域名')
        payload27 = {"result": {"data": "s1.test.com"}}
        r27 = self.put(url=url5, json=payload27, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code27, res27 = r27
            if not (status_code27 == 200 and res27['code'] == "Success"):
                self.exception.add('Step27: ' + str(r27))
        else:
            self.exception.add('Step27: ' + str(self.api_error))

        print('Step2: 点击【记录管理】，添加r1.test.com的A记录的解析结果为1.1.1.1,权重为1，ttl为100，备注为空')
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="r1", res="1.1.1.1", weight=1,
                                        ttl=100)


        print('Step28: 点击【记录管理】，添加mx1的MX记录解析结果为优先级为10，域名为mail.qq.com')
        self.authorization_add_mx_record(nodename=self.nodename[0],domain=domain1,host="mx1",res="mail.qq.com",preference=10)



        print('Step29: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=test.com&host=mx1接口，查出步骤28中记录的id')
        payload29 = {
            "domain": domain1,
            "host": "mx1",
            "type": "MX"
        }
        r29 = self.get(url=url1, params=payload29, auth=(self.api_user, self.api_password))
        id5 = ""
        if self.api_error is None:
            status_code29, res29 = r29
            if status_code29 == 200 and res29['code'] == "Success" and len(res29['data']) == 1:
                id5 = res29['data'][0]['id']
            else:
                self.exception.add('Step29: ' + str(r29))
        else:
            self.exception.add('Step29: ' + str(self.api_error))

        url6 = url1 + "/" + str(id5)

        print('Step30: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc04e918889ee7be5a923ed接口，将mx1.test.com的MX类型的解析结果修改为优先级为0，域名合法')
        payload30 = {"result": {"preference": 0, "data": "mail.baidu.com"}}
        r30 = self.put(url=url6, json=payload30, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code30, res30 = r30
            if not (status_code30 == 200 and res30['code'] == "Success"):
                self.exception.add('Step30: ' + str(r30))
        else:
            self.exception.add('Step30: ' + str(self.api_error))

        print('Step31: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc04e918889ee7be5a923ed接口，将mx1.test.com的MX类型的解析结果修改为优先级为1，域名合法')
        payload31 = {"result": {"preference": 1, "data": "mail.baidu.com"}}
        r31 = self.put(url=url6, json=payload31, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code31, res31 = r31
            if not (status_code31 == 200 and res31['code'] == "Success"):
                self.exception.add('Step31: ' + str(r31))
        else:
            self.exception.add('Step31: ' + str(self.api_error))

        print('Step32: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc04e918889ee7be5a923ed接口，将mx1.test.com的MX类型的解析结果修改为优先级为65535')
        payload32 = {"result": {"preference": 65535, "data": "mail.baidu.com"}}
        r32 = self.put(url=url6, json=payload32, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code32, res32 = r32
            if not (status_code32 == 200 and res32['code'] == "Success"):
                self.exception.add('Step32: ' + str(r32))
        else:
            self.exception.add('Step32: ' + str(self.api_error))

        print('Step33: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc04e918889ee7be5a923ed接口，将mx1.test.com的MX类型的解析结果修改为优先级为-1')
        payload33 = {"result": {"preference": -1, "data": "mail.baidu.com"}}
        r33 = self.put(url=url6, json=payload33, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code33, res33 = r33
            if not (status_code33 == 400 and res33['code'] == "InvalidParam"):
                self.exception.add('Step33: ' + str(r33))
        else:
            self.exception.add('Step33: ' + str(self.api_error))

        print('Step34: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc04e918889ee7be5a923ed接口，将mx1.test.com的MX类型的解析结果修改为优先级为65536，域名合法')
        payload34 = {"result": {"preference": 65536, "data": "mail.baidu.com"}}
        r34 = self.put(url=url6, json=payload34, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code34, res34 = r34
            if not (status_code34 == 400 and res34['code'] == "InvalidParam"):
                self.exception.add('Step34: ' + str(r34))
        else:
            self.exception.add('Step34: ' + str(self.api_error))

        print('Step35: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc04e918889ee7be5a923ed接口，将mx1.test.com的MX类型的解析结果修改为优先级为合法，域名不合法')
        payload35 = {"result": {"preference": 20, "data": "_^mail.baidu.com"}}
        r35 = self.put(url=url6, json=payload35, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code35, res35 = r35
            if not (status_code35 == 400 and res35['code'] == "InvalidParam"):
                self.exception.add('Step35: ' + str(r35))
        else:
            self.exception.add('Step35: ' + str(self.api_error))

        print('Step36: 点击【记录管理】，添加ipv4反向域和ipv6反向域，分别为3.2.1.in-addr.arpa和a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.1.2.3.4.ip6.arpa')
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

        print('Step37: 点击【记录管理】，添加ipv4反向域的记录10.3.2.1.in-addr.arpa的解析结果为10.test.com')
        self.authorization_add_ptr_record(nodename=self.nodename[0],domain=reverse_domain1,host="10",res="10.test.com")

        print('Step38: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=3.2.1.in-addr.arpa&host=10接口，查出步骤37中记录的id')
        payload38 = {
            "domain": reverse_domain1,
            "host": "10",
            "type": "PTR"
        }
        r38 = self.get(url=url1, params=payload38, auth=(self.api_user, self.api_password))
        id6 = ""
        if self.api_error is None:
            status_code38, res38 = r38
            if status_code38 == 200 and res38['code'] == "Success" and len(res38['data']) == 1:
                id6 = res38['data'][0]['id']
            else:
                self.exception.add('Step38: ' + str(r38))
        else:
            self.exception.add('Step38: ' + str(self.api_error))

        url7 = url1 + "/" + str(id6)

        print('Step39: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc052f78889ee7be5a92401接口，将反向域的解析结果修改为一级域')
        payload39 = {"result": {"data": "org"}}
        r39 = self.put(url=url7, json=payload39, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code39, res39 = r39
            if not (status_code39 == 200 and res39['code'] == "Success"):
                self.exception.add('Step39: ' + str(r39))
        else:
            self.exception.add('Step39: ' + str(self.api_error))

        print('Step40: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc052f78889ee7be5a92401接口，将反向域的解析结果修改为根')
        payload40 = {"result": {"data": "."}}
        r40 = self.put(url=url7, json=payload40, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code40, res40 = r40
            if not (status_code40 == 200 and res40['code'] == "Success"):
                self.exception.add('Step40: ' + str(r40))
        else:
            self.exception.add('Step40: ' + str(self.api_error))

        print('Step41: 点击【记录管理】，添加ipv6反向域b.a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.1.2.3.4.ip6.arpa的ptr记录为11.yamu.com')
        self.authorization_add_ptr_record(nodename=self.nodename[0], domain=reverse_domain2, host="b",res="11.test.com")

        print('Step42: 用GET方法调用https://192.168.6.62:19393/api/dns/records?domain=a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.1.2.3.4.ip6.arpa&host=b接口')
        payload42 = {
            "domain": reverse_domain2,
            "host": "b",
            "type": "PTR"
        }
        r42 = self.get(url=url1, params=payload42, auth=(self.api_user, self.api_password))
        id7 = ""
        if self.api_error is None:
            status_code42, res42 = r42
            if status_code42 == 200 and res42['code'] == "Success" and len(res42['data']) == 1:
                id7 = res42['data'][0]['id']
            else:
                self.exception.add('Step42: ' + str(r38))
        else:
            self.exception.add('Step42: ' + str(self.api_error))

        url8 = url1 + "/" + str(id7)
        print('Step43: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc054a28889ee7be5a92417接口，将反向域的解析结果修改为合法的域名')
        payload43 = {"result": {"data": "11.test.com"}}
        r43 = self.put(url=url8, json=payload43, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code43, res43 = r43
            if not (status_code43 == 200 and res43['code'] == "Success"):
                self.exception.add('Step43: ' + str(r43))
        else:
            self.exception.add('Step43: ' + str(self.api_error))

        print('Step44: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bc052f78889ee7be5a92401接口，将反向域的解析结果修改为不合法的域名,')
        payload44 = {"result": {"data": "_-dns**.yamu.com"}}
        r44 = self.put(url=url8, json=payload44, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code44, res44 = r44
            if not (status_code44 == 400 and res44['code'] == "InvalidParam"):
                self.exception.add('Step44: ' + str(r44))
        else:
            self.exception.add('Step44: ' + str(self.api_error))

