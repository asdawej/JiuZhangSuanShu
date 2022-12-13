def 汉字数字(数字: int) -> str:
    d_汉字数字={0:'零', 1:'一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六', 7:'七', 8:'八', 9:'九'}
    s=''
    for x in str(数字):
        s+=d_汉字数字[int(x)]
    return s

def 约分术(分子: int, 分母: int) -> tuple[int]:
    if 分子==0:
        return 0, 1
    if 分子%2==0 and 分母%2==0:
        分子, 分母=int(分子/2), int(分母/2)
    M, m=max(分子, 分母), min(分子, 分母)
    while not M==m:
        M, m=max(M-m, m), min(M-m, m)
    return int(分子/m), int(分母/m)

class 分数(object):

    def __init__(self, 分子: int, 分母: int):
        self.分子, self.分母=约分术(分子, 分母)

    def __str__(self) -> str:
        return '{}分之{}'.format(汉字数字(self.分母), 汉字数字(self.分子))

    def __mul__(self, x: '分数' | int) -> '分数':
        'int or 分数 on the right'
        if type(x)==int:
            return 分数(self.分子*x, self.分母)
        s=分数(self.分子*x.分子, self.分母*x.分母)
        return s

    def __add__(self, x: '分数' | int) -> '分数':
        if type(x)==int:
            return 分数(self.分子+self.分母*x, self.分母)
        return 分数(self.分子*x.分母+self.分母*x.分子, self.分母*x.分母)

    def __sub__(self, x: '分数' | int) -> '分数':
        if type(x)==int:
            x=分数(x, 1)
        return 分数(abs(self.分子*x.分母-self.分母*x.分子), self.分母*x.分母)

    def __truediv__(self, x: '分数' | int) -> '分数':
        if type(x)==int:
            x=分数(x, 1)
        if x.分子==0:
            raise ZeroDivisionError
        return self*分数(x.分母, x.分子)

    def __floordiv__(self, x: '分数' | int) -> '分数':
        if type(x)==int:
            x=分数(x, 1)
        if x.分子==0:
            raise ZeroDivisionError
        return 分数((self.分子*x.分母)//(self.分母*x.分子), 1)

    def __mod__(self, x: '分数' | int) -> '分数':
        return self-self//x*x

    def __divmod__(self, x: '分数' | int) -> '分数':
        return self//x, self%x

    def __lt__(self, x: '分数' | int) -> bool:
        if type(x)==int:
            x=分数(x, 1)
        return self.分子*x.分母-self.分母*x.分子<0

    def __gt__(self, x: '分数' | int) -> bool:
        if type(x)==int:
            x=分数(x, 1)
        return self.分子*x.分母-self.分母*x.分子>0

    def __le__(self, x: '分数' | int) -> bool:
        return not self>x

    def __ge__(self, x: '分数' | int) -> bool:
        return not self<x

    def __ne__(self, x: '分数' | int) -> bool:
        return self>x or self<x

    def __eq__(self, x: '分数' | int) -> bool:
        return self>=x and self<=x
    
class 面积(object):

    def __init__(self, 顷: 分数, 积里: 分数, 亩: 分数, 积步: 分数):
        self.顷=顷
        self.积里=积里
        self.亩=亩
        self.积步=积步

    def __str__(self) -> str:
        return '{}顷{}里{}亩{}步'.format(str(self.顷), str(self.积里), str(self.亩), str(self.积步))

    def 换算(self, base=None):
        self.积步+=self.顷*100*240+self.亩*240+self.积里*90000
        if base=='积步':
            self.顷=分数(0, 1)
            self.积里=分数(0, 1)
            self.顷=分数(0, 1)
        else:
            self.亩, self.积步=divmod(self.积步, 240)
            self.顷, self.亩=divmod(self.亩, 100)
            self.积里=分数(0, 1)

    def __mul__(self, x: 分数) -> '面积':
        '分数 on the right'
        if type(x)==分数:
            s=面积(顷=self.顷*x, 积里=self.积里*x, 亩=self.亩*x, 积步=self.积步*x)
            s.换算()
            return s

    def __add__(self, x: '面积') -> '面积':
        s=面积(self.顷+x.顷, self.积里+x.积里, self.亩+x.亩, self.积步+x.积步)
        s.换算()
        return s

    def __sub__(self, x: '面积') -> '面积':
        s=面积(self.顷-x.顷, self.积里-x.积里, self.亩-x.亩, self.积步-x.积步)
        s.换算()
        return s

    def __lt__(self, x: '面积') -> bool:
        self.换算(base='积步')
        x.换算(base='积步')
        return self.积步<x.积步

    def __gt__(self, x: '面积') -> bool:
        self.换算(base='积步')
        x.换算(base='积步')
        return self.积步>x.积步

    def __le__(self, x: '面积') -> bool:
        return not self>x

    def __ge__(self, x: '面积') -> bool:
        return not self<x

    def __ne__(self, x: '面积') -> bool:
        return self>x or self<x

    def __eq__(self, x: '面积') -> bool:
        return self>=x and self<=x
    
class 长度(object):

    def __init__(self, 里: 分数, 步: 分数):
        self.里=里
        self.步=步

    def 换算(self, base=None):
        if base=='步':
            self.里, self.步=分数(0, 1), self.里*300+self.步
        else:
            self.里, self.步=divmod(self.里*300+self.步, 300)

    def __str__(self) -> str:
        return '{}里{}步'.format(str(self.里), str(self.步))

    def __mul__(self, x: 分数 | '长度') -> '长度':
        '分数 or 长度 on the right'
        if type(x)==分数:
            s=长度(里=self.里*x, 步=self.步*x)
            s.换算()
            return s
        if self.步==分数(0, 1) and x.步==分数(0, 1):
            s=面积(顷=分数(0, 1), 积里=分数(0, 1), 亩=self.里*x.里*375, 积步=分数(0, 1))
            s.换算()
            return s
        else:
            self.换算(base='步')
            x.换算(base='步')
            s=面积(顷=分数(0, 1), 积里=分数(0, 1), 亩=分数(0, 1), 积步=self.步*x.步)
            s.换算()
            return s

    def __add__(self, x: '长度') -> '长度':
        s=长度(self.里+x.里, self.步+x.步)
        s.换算()
        return s

    def __sub__(self, x: '长度') -> '长度':
        s=长度(self.里-x.里, self.步-x.步)
        s.换算()
        return s

    def __lt__(self, x: '长度') -> bool:
        self.换算(base='步')
        x.换算(base='步')
        return self.步<x.步

    def __gt__(self, x: '长度') -> bool:
        self.换算(base='步')
        x.换算(base='步')
        return self.步>x.步

    def __le__(self, x: '长度') -> bool:
        return not self>x

    def __ge__(self, x: '长度') -> bool:
        return not self<x

    def __ne__(self, x: '长度') -> bool:
        return self>x or self<x

    def __eq__(self, x: '长度') -> bool:
        return self>=x and self<=x

def 平分术(l: list[分数]) -> tuple[ list[tuple[ str | 分数 ]] | 分数 ]:
    平实=0
    未并者=[]
    for i,x in enumerate(l):
        _l=l[:]
        _l.pop(i)
        _s=x.分子
        for y in _l:
            _s=_s*y.分母
        未并者.append(_s)
        平实+=_s
    法=1
    for x in l:
        法=法*x.分母
    列数=len(l)
    列实=[x*列数 for x in 未并者]
    新分母=列数*法
    d={True:'减', False:'益'}
    余=[(d[平实<x], abs(平实-x)) for x in 列实]
    减益=[(x[0], 分数(x[1], 新分母)) for x in 余]
    平=分数(平实, 法)
    return 减益, 平
