import functools
import logging
import BeautifulReport
from configuration import global_v
import inspect
import datetime


class runningRecorder(object):
    def __init__(self, desc=None, logpath='log_testRunner.log'):
        self.desc = desc
        logging.basicConfig(filename='D:/pycharm_workspace/autolog/log_testRunner_{date_now}.log'.format(date_now=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H-%M-%S')), level=logging.INFO)

    def myInfo(self, context):
        style = '%s:%s'%(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'), context)
        print(style)
        logging.info(style)

    def __call__(self, func):  # 接收函数
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            totol = global_v.get_value('case_sum', defValue=1)
            runned_count = global_v.get_value('result_dict', defValue={'testsRun': 1})['testsRun']
            skipped_count = global_v.get_value('result_dict', defValue={'skipped': 0})['skipped']
            if inspect.stack()[1][3] == 'run':
                self.myInfo("{func} :  {desc}".format(desc=self.desc, func=func.__name__))
                self.myInfo("{func}<<<<<<start,用例总数{case_sum},完成数量{runned},跳过数量{skipped}".format(
                    func=func.__name__,
                    case_sum=totol,
                    runned=runned_count-1,
                    skipped=skipped_count
                ))
            else:
                self.myInfo("       Invoke sub function {func} start".format(func=func.__name__))
            funReturn = func(*args, **kwargs)
            if inspect.stack()[1][3] == 'run':
                self.myInfo("{func}>>>>>>end,用例总数{case_sum},完成数量{runned},跳过数量{skipped}".format(
                    func=func.__name__,
                    case_sum=totol,
                    runned=runned_count,
                    skipped=skipped_count
                ))
            else:
                self.myInfo("       Invoke sub function {func} end".format(func=func.__name__))
            # if isinstance(funReturn, dict):
            #     for key, value in funReturn.items():
            #         print("[{key}]:{value}".format(key = key, value = value))
            # else:
            #     print('非字典类型不打印结果')
            return funReturn
        return wrapper  # 返回函数
