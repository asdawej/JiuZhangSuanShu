from __future__ import annotations

from functools import total_ordering
from typing import Literal

d_汉字数字 = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}


def 汉字数字(数字: int) -> str:
    return ''.join([d_汉字数字[int(x)] for x in str(数字)])


def 约分术(分子: int, 分母: int) -> tuple[int, int]:
    if 分子 == 0:
        return 0, 1
    if 分子 % 2 == 0 and 分母 % 2 == 0:
        分子, 分母 = int(分子 / 2), int(分母 / 2)
    M, m = max(分子, 分母), min(分子, 分母)
    while not M == m:
        M, m = max(M - m, m), min(M - m, m)
    return int(分子 / m), int(分母 / m)


@total_ordering
class 分数:
    def __init__(self, 分子: int, 分母: int = 1) -> None:
        self.分子, self.分母 = 约分术(分子, 分母)

    def __str__(self) -> str:
        return f'{汉字数字(self.分母)}分之{汉字数字(self.分子)}'

    def __mul__(self, x: 分数 | int) -> 分数:
        if isinstance(x, int):
            return 分数(self.分子 * x, self.分母)
        s = 分数(self.分子 * x.分子, self.分母 * x.分母)
        return s

    def __add__(self, x: 分数 | int) -> 分数:
        if isinstance(x, int):
            return 分数(self.分子 + self.分母 * x, self.分母)
        return 分数(self.分子 * x.分母 + self.分母 * x.分子, self.分母 * x.分母)

    def __sub__(self, x: 分数 | int) -> 分数:
        if isinstance(x, int):
            x = 分数(x)
        return 分数(abs(self.分子 * x.分母 - self.分母 * x.分子), self.分母 * x.分母)

    def __truediv__(self, x: 分数 | int) -> 分数:
        if isinstance(x, int):
            x = 分数(x)
        if x.分子 == 0:
            raise ZeroDivisionError
        return self * 分数(x.分母, x.分子)

    def __floordiv__(self, x: 分数 | int) -> 分数:
        if isinstance(x, int):
            x = 分数(x)
        if x.分子 == 0:
            raise ZeroDivisionError
        return 分数((self.分子 * x.分母) // (self.分母 * x.分子), 1)

    def __mod__(self, x: 分数 | int) -> 分数:
        return self - self // x * x

    def __divmod__(self, x: 分数 | int) -> tuple[分数, 分数]:
        return self // x, self % x

    def __lt__(self, x: 分数 | int) -> bool:
        if isinstance(x, int):
            x = 分数(x)
        return self.分子 * x.分母 - self.分母 * x.分子 < 0

    def __eq__(self, x: 分数 | int) -> bool:
        if isinstance(x, int):
            x = 分数(x)
        return self.分子 * x.分母 - self.分母 * x.分子 == 0


@total_ordering
class 面积:
    def __init__(self, 顷: 分数, 积里: 分数, 亩: 分数, 积步: 分数) -> None:
        self.顷 = 顷
        self.积里 = 积里
        self.亩 = 亩
        self.积步 = 积步

    def __str__(self) -> str:
        return f'{self.顷}顷{self.积里}里{self.亩}亩{self.积步}步'

    def 换算(self, base: Literal['步'] | None = None) -> None:
        self.积步 += self.顷 * 100 * 240 + self.亩 * 240 + self.积里 * 90000
        if base == '积步':
            self.顷 = 分数(0)
            self.积里 = 分数(0)
            self.顷 = 分数(0)
        else:
            self.亩, self.积步 = divmod(self.积步, 240)
            self.顷, self.亩 = divmod(self.亩, 100)
            self.积里 = 分数(0)

    def __mul__(self, x: 分数) -> 面积:
        s = 面积(顷=self.顷 * x, 积里=self.积里 * x, 亩=self.亩 * x, 积步=self.积步 * x)
        s.换算()
        return s

    def __add__(self, x: 面积) -> 面积:
        s = 面积(顷=self.顷 + x.顷, 积里=self.积里 + x.积里, 亩=self.亩 + x.亩, 积步=self.积步 + x.积步)
        s.换算()
        return s

    def __sub__(self, x: 面积) -> 面积:
        s = 面积(顷=self.顷 - x.顷, 积里=self.积里 - x.积里, 亩=self.亩 - x.亩, 积步=self.积步 - x.积步)
        s.换算()
        return s

    def __lt__(self, x: 面积) -> bool:
        self.换算(base='积步')
        x.换算(base='积步')
        return self.积步 < x.积步

    def __eq__(self, x: 面积) -> bool:
        self.换算(base='积步')
        x.换算(base='积步')
        return self.积步 == x.积步


@total_ordering
class 长度:
    def __init__(self, 里: 分数, 步: 分数) -> None:
        self.里 = 里
        self.步 = 步

    def 换算(self, base: Literal['步'] | None = None) -> None:
        if base == '步':
            self.里, self.步 = 分数(0), self.里 * 300 + self.步
        else:
            self.里, self.步 = divmod(self.里 * 300 + self.步, 300)

    def __str__(self) -> str:
        return f'{self.里}里{self.步}步'

    def __mul__(self, x: 分数 | 长度) -> 长度:
        if isinstance(x, 分数):
            s = 长度(里=self.里 * x, 步=self.步 * x)
            s.换算()
            return s
        if self.步 == 分数(0) and x.步 == 分数(0):
            s = 面积(顷=分数(0), 积里=分数(0), 亩=self.里 * x.里 * 375, 积步=分数(0))
            s.换算()
            return s
        self.换算(base='步')
        x.换算(base='步')
        s = 面积(顷=分数(0), 积里=分数(0), 亩=分数(0), 积步=self.步 * x.步)
        s.换算()
        return s

    def __add__(self, x: 长度) -> 长度:
        s = 长度(里=self.里 + x.里, 步=self.步 + x.步)
        s.换算()
        return s

    def __sub__(self, x: 长度) -> 长度:
        s = 长度(里=self.里 - x.里, 步=self.步 - x.步)
        s.换算()
        return s

    def __lt__(self, x: 长度) -> bool:
        self.换算(base='步')
        x.换算(base='步')
        return self.步 < x.步

    def __eq__(self, x: 长度) -> bool:
        self.换算(base='步')
        x.换算(base='步')
        return self.步 == x.步


def 平分术(l: list[分数]) -> tuple[list[tuple[str, 分数]], 分数]:
    平实 = 0
    未并者: list[int] = []
    for i, x in enumerate(l):
        _l = l[:]
        _l.pop(i)
        _s = x.分子
        for y in _l:
            _s = _s * y.分母
        未并者.append(_s)
        平实 += _s
    法 = 1
    for x in l:
        法 = 法 * x.分母
    列数 = len(l)
    列实 = [x * 列数 for x in 未并者]
    新分母 = 列数 * 法
    余 = [('减' if 平实 < x else '益', abs(平实 - x)) for x in 列实]
    减益 = [(x[0], 分数(x[1], 新分母)) for x in 余]
    平 = 分数(平实, 法)
    return 减益, 平
