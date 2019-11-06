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

    def test_add_auth_domain_validation_check(self):
        url1 = "https://" + self.serverip[0] + ":19393/api/dns/zones"

        print('Step1: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的正向域abc1.com')
        payload1 = {
                    "domain": "abc1.com"
                    }

        r1 = self.post(url=url1,json=payload1,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success"):
                self.exception.add('Step1: ' + str(res1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的正向域_sip.abc-2.com')
        payload2 = {
                    "domain": "_sip.abc-2.com"
                    }
        r2 = self.post(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add('Step2: ' + str(res2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的正向域一级域org')
        payload3 = {
                    "domain": "org"
                    }
        r3 = self.post(url=url1, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的正向域34级域')
        # payload4 = {
        #             "domain": "a1.a2.a3.a4.a5.a6.a7.a8.a9.a10.a11.a12.a13.a14.a15.a16.a17.a18.a19.a20.a21.a22.a23.a24.a25.a26.a27.a28.a29.a30.a31.a32.a33.com"
        #             }
        payload4 = {
            "domain": "a1.a2.a3.a4.a5.a6.com"
        }
        r4 = self.post(url=url1, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的正向域为根')
        payload5 = {
                    "domain": "."
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的ipv4反向域3.2.1.in-addr.arpa')
        payload6 = {
                    "domain": "3.2.1.in-addr.arpa"
                    }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名为正常的ipv6反向域1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa')
        payload7 = {
                    "domain": "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa"
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 200 and res7['code'] == "Success"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，添加的域已经存在')
        payload8 = {
                    "domain": "abc1.com"
                    }
        r8 = self.post(url=url1, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 400 and res8['code'] == "InvalidParam"):
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        print('Step9: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名称为空')
        payload9 = {
            "domain": ""
        }
        r9 = self.post(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 400 and res9['code'] == "InvalidDomain"):
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，缺少必填参数domain')
        payload10 = {
                    "nodeName": self.nodename[0]
                    }
        r10 = self.post(url=url1, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 400 and res10['code'] == "InvalidDomain"):
                self.exception.add('Step10: ' + str(res10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名包含特殊字符')
        payload11 = {
                    "domain": "@~abc1^.com"
                    }
        r11 = self.post(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "InvalidParam"):
                self.exception.add('Step11: ' + str(res11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名中下划线出现在label的结尾')
        payload12 = {
                    "domain": "abc_.com"
                    }
        r12 = self.post(url=url1, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "InvalidParam"):
                self.exception.add('Step12: ' + str(res12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名中下划线后紧跟中杠线')
        payload13 = {
                    "domain": "_-adc.com"
                    }
        r13 = self.post(url=url1, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 400 and res13['code'] == "InvalidParam"):
                self.exception.add('Step13: ' + str(res13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名中同一个label有1个以上的下划线')
        payload14 = {
                    "domain": "_a_bc.com"
                    }
        r14 = self.post(url=url1, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "InvalidParam"):
                self.exception.add('Step14: ' + str(res14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名中中杠线出现在label的开头')
        payload15 = {
                    "domain": "-abc.com"
                    }
        r15 = self.post(url=url1, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "InvalidParam"):
                self.exception.add('Step15: ' + str(res15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名中中杠线出现在label的结尾')
        payload16 = {
                    "domain": "abc-.com"
                    }
        r16 = self.post(url=url1, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "InvalidParam"):
                self.exception.add('Step16: ' + str(res16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))

        print('Step17: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名的label字符数超过最大长度为64的限制')
        payload17 = {
                    "domain": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef65"
                    }
        r17 = self.post(url=url1, json=payload17, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code17, res17 = r17
            if not (status_code17 == 400 and res17['code'] == "InvalidParam"):
                self.exception.add('Step17: ' + str(res17))
        else:
            self.exception.add('Step17: ' + str(self.api_error))

        print('Step18: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，域名的label数超过最多为33的限制')
        payload18 = {
                    "domain": "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa"
                    }
        r18 = self.post(url=url1, json=payload18, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code18, res18 = r18
            if not (status_code18 == 400 and res18['code'] == "InvalidParam"):
                self.exception.add('Step18: ' + str(res18))
        else:
            self.exception.add('Step18: ' + str(self.api_error))

        print('Step19: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，ipv4反向域的label数超过了5')
        payload19 = {
                    "domain": "4.3.2.1.in-addr.arpa"
                    }
        r19 = self.post(url=url1, json=payload19, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code19, res19 = r19
            if not (status_code19 == 400 and res19['code'] == "InvalidParam"):
                self.exception.add('Step19: ' + str(res19))
        else:
            self.exception.add('Step19: ' + str(self.api_error))

        print('Step20: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，ipv4反向域的label字符不合法')
        payload20 = {
                    "domain": "256.2.-1.in-addr.arpa"
                    }
        r20 = self.post(url=url1, json=payload20, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code20, res20 = r20
            if not (status_code20 == 400 and res20['code'] == "InvalidParam"):
                self.exception.add('Step20: ' + str(res20))
        else:
            self.exception.add('Step20: ' + str(self.api_error))

        print('Step21: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，ipv6反向域的label字符不合法')
        payload21 = {
                    "domain": "1.0.0.0.0.11.0.0.0.g.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa"
                    }
        r21 = self.post(url=url1, json=payload21, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code21, res21 = r21
            if not (status_code21 == 400 and res21['code'] == "InvalidParam"):
                self.exception.add('Step21: ' + str(res21))
        else:
            self.exception.add('Step21: ' + str(self.api_error))

        print('Step22: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，ipv6反向域的label字符为小写')
        payload22 = {
                    "domain": "1.0.0.0.0.1.0.0.0.a.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa"
                    }
        r22 = self.post(url=url1, json=payload22, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code22, res22 = r22
            if not (status_code22 == 200 and res22['code'] == "Success"):
                self.exception.add('Step22: ' + str(res22))
        else:
            self.exception.add('Step22: ' + str(self.api_error))

        print('Step23: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，ipv6反向域的label字符为大写')
        payload23 = {
            "domain": "1.0.0.0.0.1.0.0.0.A.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa"
        }
        r23 = self.post(url=url1, json=payload23, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code23, res23 = r23
            if not (status_code23 == 400 and res23['code'] == "InvalidParam" and "域已存在" in str(res23['msg'])):
                self.exception.add('Step23: ' + str(res23))
        else:
            self.exception.add('Step23: ' + str(self.api_error))

