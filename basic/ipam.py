from .method import Comply
from .common import common
import re
from time import sleep

class ipam(Comply,common):

    def ipSegment_management_enter_management(self):
        #点击IPAM
        self.path_click('//h2/a[text()="IPAM"]')
        #点击IP段管理
        self.path_click('//div/nav/ul/li/a[text()="IP段管理"]')

    def ipSegment_configure_enter_configure(self):
        #点击IPAM
        self.path_click('//h2/a[text()="IPAM"]')
        #点击IP段配置
        self.path_click('//div/nav/ul/li/a[text()="IP段配置"]')

    def ipSegment_configure_enter_ipsegment_configure(self):
        #进入IP段配置界面
        self.ipSegment_configure_enter_configure()
        #点击IP段配置
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="IP段配置"]')

    def ipSegment_configure_enter_static_ip(self):
        #进入IP段配置界面
        self.ipSegment_configure_enter_configure()
        #点击静态IP
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="静态IP"]')

    def ipSegment_configure_enter_dynamic_ip(self):
        #进入IP段配置界面
        self.ipSegment_configure_enter_configure()
        #点击动态IP
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="动态IP"]')

    def ipSegment_configure_enter_reserved_ip(self):
        #进入IP段配置界面
        self.ipSegment_configure_enter_configure()
        #点击预留IP
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="预留IP"]')

    def ipSegment_management_add_ip_segment(self,ip,type,mask,share_network=None,note=""):
        #进入IP段管理
        self.ipSegment_management_enter_management()
        #点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #输入IP段
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入IP地址"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入IP地址"]',ip)
        #选择IP类型
        self.path_select('//*[@id="form"]/div[2]/div[1]/select',type)
        #输入掩码
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入掩码"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入掩码"]',mask)
        if share_network:
            self.path_select('//*[@id="form"]/div[4]/div[1]/select',share_network)
        #输入备注
        self.path_clear('//*[@id="form"]/div/div/textarea[@placeholder="备注"]')
        self.path_send('//*[@id="form"]/div/div/textarea[@placeholder="备注"]',note)
        #点击保存
        self.path_click('//*[@id="sysNetwork-id"]/div/button[text()="保存"]')
        self.alert()

    def ipSegment_configure_configrure_ip_segment(self,ipsegment,gateway,dns):
        #进入IP段配置界面
        self.ipSegment_configure_enter_ipsegment_configure()
        #点击配置按钮
        sleep(5)
        self.ipSegment_configure_click_configure_button(ipsegment)
        #输入网关
        self.id_clear('gateway')
        self.id_send('gateway',gateway)
        #输入DNS
        self.id_clear('dns')
        self.id_send('dns',dns)
        #点击保存
        self.path_click('//*[@id="segment-id"]/div/button[text()="保存"]')
        self.alert()



    def ipSegment_configure_add_static_ip_segment(self,segment,ip,gateway,dns):
        #进入静态IP配置界面
        self.ipSegment_configure_enter_static_ip()
        #点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #选择IP段
        self.path_select('//*[@id="form"]/div[1]/div[1]/select',segment)
        #输入IP地址
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请输入IP地址"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请输入IP地址"]',ip)
        #输入网关
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请填写网关地址"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请填写网关地址"]',gateway)
        #输入DNS
        self.path_clear('//*[@id="form"]/div/div/input[@placeholder="请填写DNS服务器地址，多个地址以英文逗号分隔"]')
        self.path_send('//*[@id="form"]/div/div/input[@placeholder="请填写DNS服务器地址，多个地址以英文逗号分隔"]',dns)
        #点击保存
        self.path_click('//*[@id="static-id"]/div/button[text()="保存"]')
        self.alert()

    def ipSegment_configure_add_static_dynamic_segment(self, segment, start, end, gateway, dns):
        #进入动态IP段界面
        self.ipSegment_configure_enter_dynamic_ip()
        #点击新增
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        # 选择IP段
        self.path_select('//*[@id="form"]/div[1]/div[1]/select', segment)
        #输入起始IP段
        self.path_clear('//*[@id="form"]/div/div/input[text()="请输入起始IP地址"]')
        self.path_send('//*[@id="form"]/div/div/input[text()="请输入起始IP地址"]', start)
        # 输入结束IP段
        self.path_clear('//*[@id="form"]/div/div/input[text()="请输入结束IP地址"]')
        self.path_send('//*[@id="form"]/div/div/input[text()="请输入结束IP地址"]', end)
        #输入网关
        self.path_clear('//*[@id="form"]/div/div/input[text()="请填写网关地址"]')
        self.path_send('//*[@id="form"]/div/div/input[text()="请填写网关地址"]', gateway)
        #输入DNS
        self.path_clear('//*[@id="form"]/div/div/input[text()="请填写DNS服务器地址，多个地址以英文逗号分隔"]')
        self.path_send('//*[@id="form"]/div/div/input[text()="请填写DNS服务器地址，多个地址以英文逗号分隔"]', dns)
        #点击保存
        self.path_click('//*[@id="dynamic-id"]/div/button[text()="保存"]')
        self.alert()

    def ipSegment_configure_add_static_reserved_segment(self, segment, start, end, note=""):
        #进入预留IP段界面
        self.ipSegment_configure_enter_reserved_ip()
        # 点击新增
        self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #选择IP段
        self.path_select('//*[@id="form-add-dlg-id"]/div[1]/div[1]/select',segment)
        #输入起始地址
        self.path_clear('//*[@id="form-add-dlg-id"]/div/div/input[text()="起始地址"]')
        self.path_send('//*[@id="form-add-dlg-id"]/div/div/input[text()="起始地址"]', start)
        # 输入结束地址
        self.path_clear('//*[@id="form-add-dlg-id"]/div/div/input[text()="结束地址"]')
        self.path_send('//*[@id="form-add-dlg-id"]/div/div/input[text()="结束地址"]', end)
        #输入备注
        self.path_clear('//*[@id="form-add-dlg-id"]/div/div/textarea[@placeholder="备注"]')
        self.path_send('//*[@id="form-add-dlg-id"]/div/div/textarea[@placeholder="备注"]', note)
        #点击保存
        self.path_click('//*[@id="add-dlg-id"]/div/button[text()="保存"]')
        self.alert()

    def ipSegment_configure_click_configure_button(self,segment):
        count = self.ipSegment_configure_get_segment_count()
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
                segment_path = '//*[@id="datarows"]/tr[' + str(j+1) + ']/td[1]'
                if count == 1:
                    segment_path = '//*[@id="datarows"]/tr/td[1]'
                    self.path_click('//*[@id="datarows"]/tr/td[8]/div/a[text()="配置"]')
                    flag = True
                    break
                #print("path:",segment_path)
                segment_name = self.getElementText_by_xpath(segment_path)
                #print("name:",segment_name)
                if segment_name == segment:
                    self.path_click('//*[@id="datarows"]/tr[' + str(j+1) + ']/td[8]/div/a[text()="配置"]')
                    flag = True
                    break
            else:
                if i < a and a > 1:
                    # 点击下一页
                    self.id_click('result_table_next')
                    sleep(1)

            if flag:
                break
        if not flag:
            print("点击指定IP段配置按钮失败")
            self.exception.add('点击指定IP段配置按钮失败')





    def ipSegment_configure_get_segment_count(self):
        #进入IP段配置页面
        self.ipSegment_configure_enter_ipsegment_configure()
        sleep(1)
        count = 0
        text = self.getElementText_by_id('result_table_info')
        #print("text: %s" % text)
        pattern = re.compile(r'共 (\d+) 项')
        match = pattern.search(text)
        if match:
            count = match.group(1)
            #print("count: %s" % count)
        return int(count)


    def ipSegment_management_delete_all_ipSegment(self):
        self.ipSegment_management_enter_management()
        #点击全选
        self.id_click('check-all')
        #点击删除
        self.path_click('//*[@id="app"]/div/div/a[text()=" 删除"]')
        self.alert()
        self.alert()


    def addr_status_enter_addr_status(self):
        # 点击IPAM
        self.path_click('//h2/a[text()="IPAM"]')
        # 点击地址状态
        self.path_click('//nav/ul/li/a[text()="地址状态"]')

    def addr_status_configure_addr_switch_information(self,ipsegment,ip):
        #进入地址状态
        self.addr_status_enter_addr_status()
        #点击ip图形
        self.path_click('//div/ul/li/a[text()="IP图形"]')
        #选择IP段
        self.id_select('sysNetwork1',ipsegment)
        #点击刷新
        self.path_click('//*[@id="ipgrid"]/div/a/span[@class="am-icon am-icon-refresh"]')
        #print('选中IP地址192.168.16.1')
        self.path_click('//*[@id="ipgrid"]/div[@class="grid"]/div[%s]' % (int(ip.split(".")[-1]) + 2,))
        #print('点击编辑')
        self.id_click('onEdit')
        #print("输入交换机名称")
        self.path_clear('//*[@id="ipstatus_page1"]/div/div/p/input[@class="switchsNameHi"]')
        self.path_send('//*[@id="ipstatus_page1"]/div/div/p/input[@class="switchsNameHi"]', 'swname')
        #print('输入交换机地址')
        self.path_clear('//*[@id="ipstatus_page1"]/div/div/p/input[@class="hostIpHi"]')
        self.path_send('//*[@id="ipstatus_page1"]/div/div/p/input[@class="hostIpHi"]', "192.168.1.1")
        #print('输入交换机端口')
        self.path_clear('//*[@id="ipstatus_page1"]/div/div/p/input[@class="hostInterfaceHi"]')
        self.path_send('//*[@id="ipstatus_page1"]/div/div/p/input[@class="hostInterfaceHi"]', 'seo-ers-d/:df:ds')
        #print('输入备注')
        self.path_clear('//*[@id="ipstatus_page1"]/div/div/p/input[@class="commentHi"]')
        self.path_send('//*[@id="ipstatus_page1"]/div/div/p/input[@class="commentHi"]', "aaa")
        #print('点击保存')
        self.id_click('onSave')
        self.alert()



