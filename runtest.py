import os, unittest, HTMLReport
from sys import path
import logging
start_dir = os.path.split(os.path.realpath(__file__))[0]
print(start_dir)
path.append(start_dir)
report_path = os.path.join(start_dir,"reports")
discover = unittest.defaultTestLoader.discover(os.path.join(start_dir, 'case'), pattern='*.py')
logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    #runner = HTMLReport.TestRunner(report_file_name='DnsysReport_5.30', output_path= os.path.join(os.environ['HOMEPATH'], 'D:\AutoTest\Report', 'DDIReport'), title='DDI测试报告', description='上海牙木通讯技术有限公司DDI自动化测试报告', thread_count=1, thread_start_wait=3, sequential_execution=True, lang='cn')

    runner = HTMLReport.TestRunner(report_file_name='',
                                 output_path=report_path,
                                   title='DDI测试报告', description='上海牙木通讯技术有限公司DDI自动化测试报告', thread_count=1,
                                   thread_start_wait=3, sequential_execution=True, lang='cn')
    runner.run(discover)
