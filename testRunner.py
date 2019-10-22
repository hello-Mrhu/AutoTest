import unittest
import os
import BeautifulReport
from configuration import global_v

current_path = os.getcwd()
case_path = os.path.join(current_path, 'testSuite')
# case_path = os.path.join(current_path, 'practice')
report_path = os.path.join(current_path, 'report')

def case_suites():
    # discover = unittest.defaultTestLoader.discover(case_path, pattern = '*test*.py')
    discover = unittest.defaultTestLoader.discover(case_path, pattern = 'singleTransfer.py')
    # discover = unittest.defaultTestLoader.discover(case_path, pattern='practice1.py')
    return discover
if __name__=='__main__':
    case_sum = case_suites().countTestCases()
    run = BeautifulReport.BeautifulReport(case_suites())
    global_v._init()
    global_v.set_value('result_dict', run.__dict__)
    global_v.set_value('case_sum', case_sum)
    run.report(filename='test', description='测试用例', log_path=report_path)

    # result_path = report_path = os.path.join(report_path, 'report.html')
    # fp = open(result_path, 'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(stream = fp, title ='测试报告', description='用例执行情况')
    # runner.run(all_case())
    # fp.close()

    # testSuite = unittest.TestSuite()
    # testSuite.addTest(unittest.makeSuite(transfer))
    # run = BeautifulReport.BeautifulReport(testSuite)
    # run.report(filename='test', description='测试用例', log_path=report_path)

    # r = unittest.TestResult()
    # all_case().run(result=r)
    # print(r.__dict__)


