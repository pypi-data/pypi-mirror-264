# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm 
@Date    ：2024/3/25 18:03 
# @File    : Abs.py
@Author  ：夜黎
"""


class Abs:
    def __init__(self):
        self.ZERO = 0
        self.ONE = 1
        self.TWO = 2

    @staticmethod
    def _is_num(n: int) -> bool:
        """判断是否为整数"""
        if n > 0:
            return True
        else:
            return False
