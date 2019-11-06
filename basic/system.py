from time import sleep
from selenium import webdriver
from basic.method import Comply
class system(Comply):

    def add_api_user(self,nodename,username,password):
        #print('点击系统管理')
        self.path_click('//h2/a[text()="系统管理"]')
        #print('点击"用户管理"')
        self.path_click('//ul/li/a[text()="用户管理"]')
        #print('点击"用户')
        self.path_click('//div/ul/li/a[text()="API用户"]')
        #print('点击"新增"')
        self.id_click('add')
        #print('选择节点')
        self.id_select('addDevNode', nodename)
        #print('输入登录名')
        self.id_clear('addAdminName')
        self.id_send('addAdminName', username)
        #print('输入密码')
        self.id_clear('addPassword')
        self.id_send('addPassword', password)
        #print('再次输入密码')
        self.id_clear('addPasswordtoo')
        self.id_send('addPasswordtoo', password)
        #print('输入姓名')
        self.id_clear('addName')
        self.id_send('addName', "test_api")
        #print('输入邮箱')
        self.id_clear('addEmail')
        self.id_send('addEmail', 'api@ymtech.com')
        #print('输入地址')
        self.id_clear('addAddr')
        self.id_send('addAddr', 'ymbuilding')
        #print('输入部门')
        self.id_clear('addDepartment')
        self.id_send('addDepartment', 'testing')
        #print('输入联系电话')
        self.id_clear('addPhone')
        self.id_send('addPhone', '13332563654')
        #print('选择权限组')
        self.id_select('addAdminRoleId', 'AdminGroup')
        #print('点击保存')
        self.id_click('addSave')
        sleep(1.5)
        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        if "保存失败" in alert_text:
            alert.accept()
            sleep(1.5)
            self.path_click('//*[@id="addbox"]/div/button[text()="取消"]')
        else:
            alert.accept()

        sleep(1.5)




    def delete_api_user(self):
        # print('点击系统管理')
        self.path_click('//h2/a[text()="系统管理"]')
        # print('点击"用户管理"')
        self.path_click('//ul/li/a[text()="用户管理"]')
        # print('点击"用户')
        self.path_click('//div/ul/li/a[text()="API用户"]')
        #print('点击全选')
        self.id_click('checkAll')
        #print('点击删除')
        self.id_click('batchDelete')
        self.alert()
        self.alert()
        sleep(2)