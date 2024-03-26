# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm 
@Date    ：2024/3/24 10:55 
# @File    : NumThe.py
@Author  ：夜黎
"""
from Abs import Abs


class NumThe(Abs):

    def digits(self, n: int) -> list:
        """分解位数"""
        digits = len(str(n))
        li = [n // 10 ** i % 10 for i in range(digits - 1, -1, -1)]
        return li

    def is_nar(self, n: int) -> bool:
        """判断水仙花数"""
        if self._is_num(n):
            li = self.digits(n)
            Sum = self.ZERO
            for i in range(self.ZERO, len(li)):
                Sum += li[i] ** 3
            if Sum == n:
                return True
            else:
                return False
        else:
            return False

    def is_prime(self, n: int) -> bool:
        """判断素数"""
        isNum = True
        for j in range(self.TWO, n):
            if n % j == 0:
                isNum = False
        return isNum

    def is_perfect(self, n: int) -> bool:
        """判断完数"""
        factors_sum = sum([i for i in range(self.ONE, n) if n % i == 0])
        return factors_sum == n

    def is_pal(self, n: int) -> bool:
        """判断回文数"""
        n_str = str(n)
        return n_str == n_str[::-1]

    def total_pal(self, head: int, tail: int) -> list:
        """head~tail之间的所有回文数"""
        li = []
        if 10 < head < tail:
            for i in range(head, tail):
                if self.is_pal(i):
                    li.append(i)
            return li
        return []

    def total_perfect(self, head: int, tail: int) -> list:
        """head~tail之间的所有完数"""
        li = []
        if head < tail:
            for i in range(head, tail):
                if self.is_perfect(i):
                    li.append(i)
        return li

    def total_prime(self, head: int, tail: int) -> list:
        """head~tail之间的所有素数"""
        li = []
        if head < tail:
            for i in range(head, tail):
                if self.is_prime(i):
                    li.append(i)
        return li

    def total_nar(self, head: int, tail: int) -> list:
        """head~tail之间的所有水仙花数"""
        li = []
        if self._is_num(head):
            for i in range(head, tail):
                if self.is_nar(i):
                    li.append(i)
        return li
