from basic.method import Comply
from .common import common
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import re

class resource(Comply,common):

    def dhs_node_add_dns_node(self,nodename,device=None,note=None):
        #点击资源管理
        self.path_click('//h2/a[text()="资源管理"]')
        #点击DNS节点
        self.path_click('//nav/ul/li/a[text()="DNS节点"]')
        #点击新增
        self.id_click('add')
        #输入节点名称
        self.id_clear('name')
        self.id_send('name',nodename)
        if device is not None:
            self.path_click('//div[@id="addbox"]/div/form/div/div/div/button')
            sleep(2)
            for dev in device:
                try:
                    self.driver.find_element_by_xpath('//div[@id="addbox"]/div/form/div/div/div/div/ul/li/span[text()="%s"]' % dev).click()
                except BaseException:
                    pass
        self.id_click('dialog_save')
        sleep(2)
        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        if "节点名称重复" in alert_text:
            alert.accept()
            self.path_click('//*[@id="addbox"]/div/button[text()="取消"]')
        else:
            alert.accept()
        sleep(1.5)


    def dns_node_delete_all_node(self):
        # 点击资源管理
        self.path_click('//h2/a[text()="资源管理"]')
        # 点击DNS节点
        self.path_click('//nav/ul/li/a[text()="DNS节点"]')
        count = self.dns_node_get_node_count()
        sleep(1.5)
        for i in range(count):
            self.path_click('//*[@id="datarows"]/tr[1]/td[4]/div/a[text()=" 删除"]')
            sleep(1)
            self.alert()
            sleep(1)
        sleep(8)


    def dns_node_get_node_count(self):
        # 点击资源管理
        self.path_click('//h2/a[text()="资源管理"]')
        # 点击DNS节点
        self.path_click('//nav/ul/li/a[text()="DNS节点"]')
        count = 0
        text = self.getElementText_by_id('result_table_info')
        pattern = re.compile(r'共 (\d+) 项')
        match = pattern.search(text)
        if match:
            count = match.group(1)
            print("count %s" % count)
        return int(count)



    def dhcp_node_add_dhcp_single_node(self,name,device,note=""):
        # 点击资源管理
        self.path_click('//h2/a[text()="资源管理"]')
        # 点击DNS节点
        self.path_click('//nav/ul/li/a[text()="DHCP节点"]')
        #点击新增
        self.id_click('add')
        #输入节点名称
        self.id_clear('inputNodeName')
        self.id_send('inputNodeName',name)
        #选择节点类型为单节点
        self.id_select('nodeType','单设备节点')
        #选择设备
        for i in range(6):
            try:
                s = self.driver.find_element_by_id('deviceSelect1')
                Select(s).select_by_visible_text(device)
                sleep(1)
            except NoSuchElementException:
                self.driver.find_element_by_xpath('//*[@id="newNodeDialog"]/div/div/div/button[text()="取消"]').click()
                break
            except BaseException as error:
                self.error = error
                print(self.error)
            else:
                self.id_clear('inputTaskNote')
                self.id_send('inputTaskNote', note)
                # 点击完成
                self.path_click('//*[@id="newNodeDialog"]/div/div/div/button[text()="完成"]')
                self.alert()
                self.alert()
                sleep(1.5)
                break
        else:
            self.exception.add(str(self.error))


    def dhcp_node_delete_all_node(self):
        # 点击资源管理
        self.path_click('//h2/a[text()="资源管理"]')
        # 点击DHCP节点
        self.path_click('//nav/ul/li/a[text()="DHCP节点"]')
        sleep(1.5)
        count = self.dhcp_node_get_node_count()
        sleep(1.5)
        for i in range(count):
            self.path_click('//*[@id="datarows"]/tr[1]/td[6]/div/a[2]')
            self.alert()
            self.alert()
            sleep(1.5)


    def dhcp_node_get_node_count(self):
        # 点击资源管理
        self.path_click('//h2/a[text()="资源管理"]')
        # 点击DHCP节点
        self.path_click('//nav/ul/li/a[text()="DHCP节点"]')
        count = 0
        text = self.getElementText_by_id('result_table_info')
        pattern = re.compile(r'共 (\d+) 项')
        match = pattern.search(text)
        if match:
            count = match.group(1)
            print("count %s" % count)
        return int(count)


