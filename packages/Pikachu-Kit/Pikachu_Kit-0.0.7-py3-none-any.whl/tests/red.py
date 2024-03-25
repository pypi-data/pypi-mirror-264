# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: red.py
@time: 2024/2/5 16:18 
@desc: 

"""
from unittest.mock import Mock
from sdk.temp.temp_supports import IsSolution, DM
from sdk.utils.util_class import URLParser


class Solution(IsSolution):
    """
    Solution
    """

    def __init__(self, **kwargs):
        """
        初始化函数
        :param kwargs: 字典类型的参数字典，包含可选的关键字参数
        """
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})

    def get_date_captured(self,name):
        _time = name.split(".")[0].split("_")[-2]
        y = _time[:4]
        m = _time[4:6]
        d = _time[6:8]
        h = _time[8:10]
        ms = _time[10:12]
        s = _time[12:]
        print("{}-{}-{} {}:{}:{}".format(y, m, d, h, ms, s))
        return "{}-{}-{} {}:{}:{}".format(y, m, d, h, ms, s)


    # @DM.add_project()
    def muti_thread_function(self, *args):
        """
        处理数据函数
        :param args:
        :return:
        """
        arg, save_path, name = args
        for url in self.json.loads(arg["line"][arg["headers"].index("url")]):
            up = URLParser(url)
            try:
                _time = self.get_date_captured(up.name)
                print("_time",_time)
                # _time = e.get_date_captured(up.name)
            except:
                print(arg["num"], url,print(len(self.json.loads(arg["line"][arg["headers"].index("url")]))))
                answer_str = self.get_answer(arg, ["验收答案", "拟合答案", "终审答案", "审核答案", "质检答案"])
                print(answer_str)




        return None

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]
        self.folder.create_folder(save_path)
        for file, name in self.get_file(in_path, status=True):
            print(file, name)  # 打印文件名和名称
            for args in self.read_line(file, _id=2):
                self.muti_thread_function(args, save_path, name)
                # break
        DM.close_pool()
        return None


if __name__ == '__main__':
    in_path = R"D:\Desktop\1"
    save_path = R"D:\Desktop\2"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
