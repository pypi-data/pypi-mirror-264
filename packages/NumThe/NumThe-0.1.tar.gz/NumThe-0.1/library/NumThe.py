# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm 
@Date    ：2024/3/24 10:55 
# @File    : NumThe.py
@Author  ：夜黎
"""
from itertools import permutations


class NumThe:

    def __init__(self):
        self.ZERO = 0
        self.ONE = 1
        self.TWO = 2

    def digits(self, n: int) -> list:
        """分解位数"""
        digits = len(str(n))
        li = [n // 10 ** i % 10 for i in range(digits - 1, -1, -1)]
        return li

    @staticmethod
    def _is_num(n: int) -> bool:
        """判断是否为整数"""
        if n > 0:
            return True
        else:
            return False

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


class OtherNumThe(NumThe):
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



c = OtherNumThe()
r = c.min_multiple(88, 66)
print(r)
