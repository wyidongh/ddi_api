from .method import Comply
from .common import common
import re
from time import sleep


class dnspage(Comply, common):

    def authorization_add_standard_domain(self,domainname,nodename,ns_name,ns_ip,viewname="default",dnssec=False,note=""):

        self.authorization_enter_domain_page()
        #点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #self.path_click('//*[@id="app"]/div[3]/div/a[4]')
        #输入域名称
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入域名称"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入域名称"]',domainname)
        #选择节点
        self.path_select('//*[@id="form"]/div/div/select[@class="am-u-sm-2 am-radius validate[required]"]',nodename)
        #选择视图
        self.path_click('//*[@id="form"]/div/div/div/span/span[@class="el-cascader__label"]')
        self.path_click('//div/ul/li[text()="自定义"]')
        #self.path_click('//div/ul/li[@role="menuitem" and text()="' + viewname + '"]')
        self.path_click('//div/ul/li[@role="menuitem" and text()="%s"]' % viewname)
        #输入NS记录名称
        self.path_clear('//div/div/input[@placeholder="NS记录域名"]')
        self.path_send('//div/div/input[@placeholder="NS记录域名"]',ns_name)
        #输入NS记录IP
        self.path_clear('//*[@id="form"]/div/div/div/div/input[@placeholder="NS记录IP"]')
        self.path_send('//*[@id="form"]/div/div/div/div/input[@placeholder="NS记录IP"]',ns_ip)
        #self.path_send('//*[@id="form"]/div[12]/div[1]/div/div[2]/input',ns_ip)
        if dnssec:
            self.path_click('//*[@id="form"]/div/div/label[@for="dnssec"]')
        #输入备注
        self.path_clear('//*[@id="form"]/div/div/textarea[@placeholder="备注"]')
        self.path_send('//*[@id="form"]/div/div/textarea[@placeholder="备注"]',note)
        #点击保存
        self.path_click('//*[@id="zone-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_add_reverse_domain(self,domainname,arpa_type,nodename,ns_name,viewname="default",note=""):
        # 点击DNS
        self.path_click('//h2/a[text()="DNS"]')
        # 点击授权管理
        self.path_click('//div/nav/ul/li/a[text()="授权管理"]')
        # 点击域管理
        self.path_click('//div/ul/li/a[text()="域管理"]')
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #self.path_click('//*[@id="app"]/div[3]/div/a[4]')
        #选择反向域
        self.path_click('//*[@id="form"]/div/div/label/input[@value="1"]')
        #输入域名称
        self.path_clear('//*[@id="form"]/div/div/input[@class="am-radius am-radius"]')
        self.path_send('//*[@id="form"]/div/div/input[@class="am-radius am-radius"]',domainname)
        #选择arpa
        self.path_select('//*[@id="form"]/div/div[@class="am-u-sm-3"]/select',arpa_type)
        #选择节点
        self.path_select('//*[@id="form"]/div/div[@class="am-u-sm-7"]/select',nodename)
        #选择视图
        self.path_click('//*[@id="form"]/div/div/div/span/span[@class="el-cascader__label"]')
        self.path_click('//div/ul/li[text()="自定义"]')
        self.path_click('//div/ul/li[@role="menuitem" and text()="%s"]' % viewname)
        #输入NS记录域名
        self.path_clear('//*[@id="form"]/div/div/div/div/input[@placeholder="NS记录域名"]')
        self.path_send('//*[@id="form"]/div/div/div/div/input[@placeholder="NS记录域名"]',ns_name)
        #输入备注
        self.path_clear('//*[@id="form"]/div/div/textarea[@placeholder="备注"]')
        self.path_send('//*[@id="form"]/div/div/textarea[@placeholder="备注"]',note)
        #点击保存
        self.path_click('//*[@id="zone-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_delete_all_domain(self):
        self.authorization_enter_domain_page()
        #选择每页显示500条
        self.path_select('//*[@id="result_table_length"]/label/select','500')
        sleep(1.5)
        #点击全选
        self.id_click('check-all')
        #点击删除
        self.path_click('//*[@id="app"]/div/div/a[text()=" 删除"]')
        #点击确认
        self.alert()
        self.alert()

    def authorization_enter_domain_page(self):
        # 点击DNS
        self.path_click('//h2/a[text()="DNS"]')
        # 点击授权管理
        self.path_click('//div/nav/ul/li/a[text()="授权管理"]')
        # 点击域管理
        self.path_click('//div/ul/li/a[text()="域管理"]')



    def authorization_find_specific_domain(self,domainname,nodename,viewname="default",note=""):
        self.authorization_enter_domain_page()
        # 选择每页显示500条
        # self.path_select('//*[@id="result_table_length"]/label/select', '500')
        count = self.authorization_get_domain_count()
        a,b = divmod(count,10)
        flag = False
        for i in range(a+1):
            n = 10
            if i == a:
                if b == 0:
                    break
                else:
                    n = b
            for j in range(n):
                print("第%s次" % str(10 * i + j + 1))
                domainname_path = '//*[@id="datarows"]/tr[' + str(j + 1) + ']/td[3]'
                nodename_path = '//*[@id="datarows"]/tr[' + str(j + 1) + ']/td[2]'
                viewname_path = '//*[@id="datarows"]/tr[' + str(j + 1) + ']/td[4]'
                note_path = '//*[@id="datarows"]/tr[' + str(j + 1) + ']/td[7]'
                flag_nodename = self.isMatch(self.getElementText_by_xpath(nodename_path), nodename)
                flag_domainname = self.isMatch(self.getElementText_by_xpath(domainname_path), domainname)
                flag_viewname = self.isMatch(self.getElementText_by_xpath(viewname_path), viewname)
                flag_note = self.isMatch(self.getElementText_by_xpath(note_path), note)
                if flag_nodename and flag_domainname and flag_viewname and flag_note:
                    flag = True
                    break
                else:
                    continue
            if flag:
                break
            if i < a and a > 1:
                    # 点击下一页
                    self.id_click('result_table_next')
                    sleep(1)
        return flag

    def authorization_get_domain_count(self,nodename=None):
        if nodename is not None:
            self.path_select('//*[@id="app"]/div[3]/div/form/div[1]/select',nodename)
        count = 0
        text = self.getElementText_by_id('result_table_info')
        pattern = re.compile(r'共 (\d+) 项')
        match = pattern.search(text)
        if match:
            count = int(match.group(1))
        return count

    def authorization_add_a_record(self,nodename,domain,host,res,view="default",ttl=3600,weight=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        #点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select',nodename)
        #选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select',domain + "-" + view )
        #选择A记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select',"A")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入解析结果
        self.path_clear('//*[@id="form"]/div[6]/div/div/div/div[1]/input')
        self.path_send('//*[@id="form"]/div[6]/div/div/div/div[1]/input',res)
        #输入TTL
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="0-8640000"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="0-8640000"]',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]',weight)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_add_aaaa_record(self,nodename,domain,host,res,view="default",ttl=3600,weight=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择AAAA记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "AAAA")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入解析结果
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="IPV6"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="IPV6"]',res)
        #输入TTL
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="0-8640000"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="0-8640000"]',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]',weight)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_add_cname_record(self,nodename,domain,host,res,view="default",ttl=3600,weight=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择CNAME记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "CNAME")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入解析结果
        self.path_clear('//div/div/div/div/input[@placeholder="请输入解析结果"]')
        self.path_send('//div/div/div/div/input[@placeholder="请输入解析结果"]',res)
        #输入TTL
        self.path_clear('//div/div/div/div/input[@placeholder="0-8640000"]')
        self.path_send('//div/div/div/div/input[@placeholder="0-8640000"]',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]',weight)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_add_ns_record(self,nodename,domain,host,res,view="default",ttl=3600,weight=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择NS记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "NS")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入解析结果
        self.path_clear('//div/div/div/div/input[@placeholder="请输入解析结果"]')
        self.path_send('//div/div/div/div/input[@placeholder="请输入解析结果"]',res)
        #输入TTL
        self.path_clear('//div/div/div/div/input[@placeholder="0-8640000"]')
        self.path_send('//div/div/div/div/input[@placeholder="0-8640000"]',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]',weight)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()


    def authorization_add_mx_record(self,nodename,domain,host,res,ttl=3600,view="default",weight=1,preference=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择MX记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "MX")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入TTL
        self.path_clear('//*[@id="form"]/div[5]/div[1]/input')
        self.path_send('//*[@id="form"]/div[5]/div[1]/input',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div[6]/div[1]/input')
        self.path_send('//*[@id="form"]/div[6]/div[1]/input',weight)
        # 输入Preference
        self.path_clear('//*[@id="form"]/div[7]/div[1]/input')
        self.path_send('//*[@id="form"]/div[7]/div[1]/input', preference)
        #输入结果
        self.id_clear('recordDomain')
        self.id_send('recordDomain', res)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_add_txt_record(self,nodename,domain,host,res,view="default",ttl=3600,weight=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择AAAA记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "TXT")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入解析结果
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="请输入解析结果"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="请输入解析结果"]',res)
        #输入TTL
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="0-8640000"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="0-8640000"]',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]',weight)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()


    def authorization_add_srv_record(self, nodename, domain, host, target, ttl=3600, qz=1,view="default", priority=1,weight=1,port=1):
        # 进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择SRV记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "SRV")
        # 输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]', host)
        # 输入TTL
        self.path_clear('//*[@id="form"]/div[5]/div[1]/input')
        self.path_send('//*[@id="form"]/div[5]/div[1]/input', ttl)
        # 输入权重
        self.path_clear('//*[@id="form"]/div[6]/div[1]/input')
        self.path_send('//*[@id="form"]/div[6]/div[1]/input', qz)
        # 输入Priority
        self.path_clear('//*[@id="form"]/div[7]/div[1]/input')
        self.path_send('//*[@id="form"]/div[7]/div[1]/input', priority)
        # 输入Weight
        self.path_clear('//*[@id="form"]/div[8]/div[1]/input')
        self.path_send('//*[@id="form"]/div[8]/div[1]/input', weight)
        # 输入Port
        self.path_clear('//*[@id="form"]/div[9]/div[1]/input')
        self.path_send('//*[@id="form"]/div[9]/div[1]/input', port)
        # 输入Target:
        self.path_clear('//*[@id="form"]/div[10]/div[1]/input')
        self.path_send('//*[@id="form"]/div[10]/div[1]/input', target)
        # 点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()


    def authorization_add_ptr_record(self,nodename,domain,host,res,view="default",ttl=3600,weight=1):
        #进入记录管理界面
        self.authorization_enter_record_page()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择节点
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', nodename)
        # 选择所属域
        self.path_select('//*[@id="form"]/div[2]/div[1]/select', domain + "-" + view)
        # 选择PTR记录
        self.path_select('//*[@id="form"]/div[3]/div[1]/select', "PTR")
        #输入主机名
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入主机名"]',host)
        #输入解析结果
        self.path_clear('//*[@id="form"]/div[5]/div/div/div/div[1]/input')
        self.path_send('//*[@id="form"]/div[5]/div/div/div/div[1]/input',res)
        #输入TTL
        self.path_clear('//div/div/div/div/input[@placeholder="0-8640000"]')
        self.path_send('//div/div/div/div/input[@placeholder="0-8640000"]',ttl)
        #输入权重
        self.path_clear('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]')
        self.path_send('//*[@id="form"]/div/div/div/div/div/input[@placeholder="1-254"]',weight)
        #点击保存
        self.path_click('//*[@id="record-id"]/div/button[text()="保存"]')
        self.alert()

    def authorization_find_specific_record(self,nodename,record,type,res,viewname="default",note=""):

        count = int(self.authorization_get_record_count())
        a, b = divmod(count, 10)
        flag = False
        for i in range(a + 1):
            n = 10
            if i == a:
                if b == 0:
                    break
                else:
                    n = b
            for j in range(n):
                print(str(i * 10 + j + 1))
                nodename_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j + 1) + ']/td[2]/div/span'
                record_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j + 1) + ']/td[3]/div/span/a'
                viewname_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j + 1) + ']/td[5]/div'
                type_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j + 1) + ']/td[6]/div/span'
                res_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j + 1) + ']/td[7]/div/span'
                note_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j + 1) + ']/td[10]/div/span'

                flag_nodename = self.isMatch(self.getElementText_by_xpath(nodename_path), nodename)
                flag_record = self.isMatch(self.getElementText_by_xpath(record_path), record)
                vname = self.getElementText_by_xpath(viewname_path).strip()
                #print("vname: %s" % vname)
                flag_viewname = self.isMatch(vname, viewname)
                flag_type = self.isMatch(self.getElementText_by_xpath(type_path), type)
                flag_res = self.isMatch(self.getElementText_by_xpath(res_path), res)
                flag_note = self.isMatch(self.getElementText_by_xpath(note_path), note)

                print(flag_nodename, flag_record, flag_viewname, flag_type, flag_res,flag_note)
                if flag_nodename and flag_record and flag_viewname and flag_type and flag_res and flag_note:
                    flag = True
                    break
                else:
                    continue
            if flag:
                break
            if i < a and a > 1:
                # 点击下一页
                self.path_click('//*[@id="app"]/div[3]/div/div/div/button[@class="btn-next"]')
                sleep(1)
        return flag

        # n = page_num + 1
        # flag = False
        #
        # for i in range(n):
        #     for j in range(1,11):
        #         print(str(i*10 + j))
        #         nodename_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j) + ']/td[2]/div/span'
        #         record_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j) + ']/td[3]/div/span/a'
        #         viewname_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j) + ']/td[5]/div'
        #         type_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j) + ']/td[6]/div/span'
        #         res_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[3]/table/tbody/tr[' + str(j) + ']/td[7]/div/span'
        #         flag_nodename = self.isMatch(self.getElementText_by_xpath(nodename_path),nodename)
        #         flag_record = self.isMatch(self.getElementText_by_xpath(record_path),record)
        #         vname = self.getElementText_by_xpath(viewname_path).strip()
        #         #print("vname: %s" % vname)
        #         flag_viewname = self.isMatch(vname,viewname)
        #         flag_type = self.isMatch(self.getElementText_by_xpath(type_path), type)
        #         flag_res = self.isMatch(self.getElementText_by_xpath(res_path), res)
        #         print(flag_nodename,flag_record,flag_viewname,flag_type,flag_res)
        #         if flag_nodename and flag_record and flag_viewname and flag_type and flag_res:
        #             flag = True
        #             break
        #         else:
        #             continue
        #     if flag:
        #         break
        #     if i < n-1:
        #         self.path_click('//*[@id="app"]/div[3]/div/div/div/button[@class="btn-next"]')
        # return flag


    def authorization_enter_record_page(self):
        # 点击DNS
        self.path_click('//h2/a[text()="DNS"]')
        # 点击授权管理
        self.path_click('//div/nav/ul/li/a[text()="授权管理"]')
        # 点击域管理
        self.path_click('//div/ul/li/a[text()="记录管理"]')

    def authorization_get_record_count(self):
        self.authorization_enter_record_page()
        sleep(2)
        count = 0
        text = self.getElementText_by_xpath('//*[@id="app"]/div[3]/div/div/div[2]/span[1]')
        pattern = re.compile(r'共 (\d+) 条')
        match = pattern.search(text)
        if match:
            count = match.group(1)
            print("count %s" % count)
        return int(count)





    def view_add_addr_group(self,gname,ip,mask,comment=""):
        #进入地址组管理界面
        self.view_enter_addr_group_manager()
        #点击新增
        self.id_click('add')
        #输入地址组名称
        self.id_clear('addName')
        self.id_send('addName',gname)
        #输入ip
        self.id_clear('addIp')
        self.id_send('addIp',ip)
        #输入掩码
        self.id_clear('addMask')
        self.id_send('addMask',mask)
        #输入备注
        self.id_clear('addComment')
        self.id_send('addComment',comment)
        #点击保存
        self.id_click('addSave')
        self.alert()

    def view_add_view(self,nodename,view,gname,recursion=True,master_4="0.0.0.0",slave_4="0.0.0.0",comment=""):
        #进入视图配置界面
        self.view_enter_view_configure()
        #点击新增
        self.id_click('add')
        #选择节点
        self.id_select('devGrosforchoose',nodename)
        #输入视图名称
        self.id_clear('vnameinput')
        self.id_send('vnameinput',view)
        #选择地址组
        self.path_select('//*[@id="addbox"]/div/form/div/div/select[@class="ipgroup"]',gname)
        if recursion is True:
            #输入递归源主IP
            self.id_clear('SourceMasterIp')
            self.id_send('SourceMasterIp',master_4)
            #输入递归源从IP
            self.id_clear('SourceSlaveIp')
            self.id_send('SourceSlaveIp',slave_4)
        else:
            self.path_click('//*[@id="addbox"]/div/form/div/div/label[@for="recursionEnable"]')
        #输入备注
        self.id_clear('doc-ta-1')
        self.id_send('doc-ta-1',comment)
        #点击保存
        self.id_click('dialog_save')
        self.alert()

    def view_delete_all_view(self):
        #进入视图配置界面
        self.view_enter_view_configure()
        #点击全选
        self.id_click('checkAll')
        #点击删除
        self.id_click('batchDelete')
        #点击确认
        self.alert()
        self.alert()

    def view_delete_all_addr_group(self):
        #进入地址组管理界面
        self.view_enter_addr_group_manager()
        #点击全选
        self.id_click('checkAll')
        #点击删除
        self.id_click('batchDelete')
        #点击确认
        self.alert()
        self.alert()



    def view_enter_addr_group_manager(self):
        # 点击DNS
        self.path_click('//h2/a[text()="DNS"]')
        # 点击视图管理
        self.path_click('//div/nav/ul/li/a[text()="视图管理"]')
        # 点击地址组管理
        self.path_click('//div/ul/li/a[text()="地址组管理"]')

    def view_enter_view_configure(self):
        # 点击DNS
        self.path_click('//h2/a[text()="DNS"]')
        #点击视图管理
        self.path_click('//div/nav/ul/li/a[text()="视图管理"]')
        # 点击地址组管理
        self.path_click('//div/ul/li/a[text()="视图配置"]')

















