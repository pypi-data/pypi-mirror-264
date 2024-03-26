# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm 
@Date    ：2024/3/25 17:32 
# @File    : OtherNumThe.py
@Author  ：夜黎
"""

from itertools import permutations
from Abs import Abs


class OtherNumThe(Abs):

    def fib(self, n: int) -> list:
        """斐波拉契数列"""
        if n == self.ONE:
            return [self.ZERO, self.ONE]
        elif n == self.ZERO:
            return [self.ZERO]
        fib = [self.ZERO, self.ONE]
        for i in range(self.ONE, n):
            fib.append(fib[-1] + fib[-2])
        return fib

    def per_num(self, n: int) -> list:
        """组合数"""
        if self._is_num(n) and 100 <= n < 1000:
            num_str = str(n)
            new = set(int(''.join(p)) for p in permutations(num_str))
            new.discard(n)
            return list(new)
        return []

    def dis_num(self, n: int) -> list:
        """分解质因数"""
        li = []
        if n > self.TWO:
            for i in range(self.TWO, n):
                while n % i == 0:
                    li.append(i)
                    n //= i
            return li
        return []

    def max_divisor(self, a: int, b: int):
        """最大公约数"""
        if a < b:
            a, b = b, a
        common = a % b
        if common == 0:
            return b
        else:
            return self.max_divisor(b, common)

    def min_multiple(self, a: int, b: int):
        """最小公倍数"""
        if a < b:
            a, b = b, a
        common = a * b / self.max_divisor(a, b)
        return common
