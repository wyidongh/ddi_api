环境:
1.SmartddiA(设备名为master),SmartddiB(设备名为slave),A为主设备,B为从设备,B加入A的集群
2.与自己浏览器版本相对应的chromedriver.exe
3.SmartddiA 和 SmartddiB 后台配置ssh允许root用户登录(修改/etc/ssh/sshd_config文件,修改PermitRootLogin yes)
4.本地机器网卡配置两个同网段的Ip
步骤:
1.进入ddi_api_automation文件夹所在目录
2.将chromedriver.exe文件放到\venv\Scripts目录下
3.修改ddi_api_automation文件夹下的testinfo.json文件
(1)ddiaddrs: 修改为主设备的url
(2)devices: 如果主设备和从设备名分别为master和slave,则不用改,如果是别的则对应改
(3)serverip: 分别改为主从设备的Ip
(4)sourceip: 填写本地网卡配置的两个ip
(5)sshaddr: 分别改为主从设备的Ip
(6)sshusername,sshpassword分别填写主从设备的用户名密码
4.cd \venv\Scripts进入Scripts目录 python.exe ../../runtest.py 开始测试