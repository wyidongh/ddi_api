from .common import common
from .method import Comply
import re
from time import sleep

class dhcp(Comply, common):



    def business_configure_enter_ipSegment_configure(self):
        #点击DHCP
        self.path_click('//h2/a[text()="DHCP"]')
        #点击业务配置
        self.path_click('//nav/ul/li/a[text()="业务配置"]')
        #点击IP段管理
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="IP段管理"]')
        #点击IP段配置
        self.path_click('//*[@id="app"]/div/div/a[text()="IP段配置"]')

    def business_configure_enter_static_ip_configure(self):
        #点击DHCP
        self.path_click('//h2/a[text()="DHCP"]')
        #点击业务配置
        self.path_click('//nav/ul/li/a[text()="业务配置"]')
        #点击IP段管理
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="IP段管理"]')
        #点击静态IP
        self.path_click('//*[@id="app"]/div/div/a[text()="静态IP"]')

    def business_configure_enter_dynamic_ip_configure(self):
        #点击DHCP
        self.path_click('//h2/a[text()="DHCP"]')
        #点击业务配置
        self.path_click('//nav/ul/li/a[text()="业务配置"]')
        #点击IP段管理
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="IP段管理"]')
        #点击动态IP
        self.path_click('//*[@id="app"]/div/div/a[text()="动态IP"]')

    def business_configure_enter_reserved_ip_configure(self):
        #点击DHCP
        self.path_click('//h2/a[text()="DHCP"]')
        #点击业务配置
        self.path_click('//nav/ul/li/a[text()="业务配置"]')
        #点击IP段管理
        self.path_click('//*[@id="app"]/div/ul/li/a[text()="IP段管理"]')
        #点击预留IP
        self.path_click('//*[@id="app"]/div/div/a[text()="预留IP"]')

    def business_configure_bind_segment(self,node,segment):
        #进入IP段配置
        self.business_configure_enter_ipSegment_configure()
        sleep(1.5)
        #选择节点
        self.path_click('//*[@id="node-select-id"]/a')
        sleep(1.5)
        if node == 1:
            self.path_click('//*[@id="node-select-id"]/ul[@class="am-dropdown-content"]/li[2]/a/[@name="0"]')
        if node == 2:
            self.path_click('//*[@id="node-select-id"]/ul[@class="am-dropdown-content"]/li[3]/a[@name="1"]')

        sleep(2)
        #self.path_click('//*[@id="node-select-id"]/ul/li[3]/a')

        # 点击新增
        self.path_click('//*[@id="app"]/div[4]/div[2]/a[3]')
        #self.path_click('//*[@id="app"]/div/div/a[text()=" 新增"]')
        #选择IP段
        self.path_select('//*[@id="form-add-dlg-id"]/div/div[1]/select', segment)
        #点击保存
        self.path_click('//*[@id="add-dlg-id"]/div/button[@name = "eOnAddNodeSegmentSave"]')
        self.alert()








