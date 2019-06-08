# -*- coding: utf-8 -*-

class KMP:
    def __init__(self, pattern):
        self.pattern = pattern
        self._next = self._get_next()

    def _get_next(self):
        # j是后缀的最后一个字符
        # k是前缀的最后一个字符
        # 当前要计算的是next[j+1]，失配位置为j+1
        # 当next[x]=-1时，代表i向前移动1位，j回溯至0
        next = [-1, 0]
        j, k = 1, 0

        while j < len(self.pattern) - 1: # 因为计算的是next[j+1]，所以直行至len(t)-1
            if k == -1 or self.pattern[j] == self.pattern[k]: # k=-1表示没找到相同的前缀；t[i]=t[k]表示在之前的基础上，前缀的下一位和后缀的下一位都相同
                j += 1 # 此后需要计算的是next[j]，但是注释中仍写为next[j+1]
                k += 1 # k=-1时为k自增一下，t[i]=t[k]时表示前缀和后缀都向后走一步
                if self.pattern[j] == self.pattern[k]: # 失配位置的字符与前缀的下一个字符相同，那么就算移动到前缀的下一个字符，也必定失配，所以找更小的前缀
                    next.append(next[k])
                else: # 失配位置的字符与前缀的下一个字符不同，那么下次匹配将从前缀的下一个字符开始
                    next.append(k)
            else: # 前缀的下一位与后缀的下一位不同，那么就从前缀(或后缀)中找到新的前缀和后缀，把新前缀的最后一个字符位置赋给k
                k = next[k]
        return next

    def find(self, primary_string):
        i, j = 0, 0 # 主串和模式串的位置均为0

        while i < len(primary_string) and j < len(self.pattern):
            if primary_string[i] == self.pattern[j] or j == -1: # 主串和模式串都向后走
                i += 1
                j += 1
            else: # 回溯
                j = self._next[j]

        if j == len(self.pattern): # 匹配上了
            return i - j # 返回匹配到的位置
        else:
            return -1

class BM:
    def __init__(self, pattern):
        self.pattern = pattern
        self._BMbc = self._get_BMbc()
        self._BMgs = self._get_BMgs()

    def _get_suffix(self):
        length = len(self.pattern)
        suffix = [length, ]

        for i in range(length-2, -1, -1):
            j = i
            while j >= 0 and self.pattern[j] == self.pattern[(length-1)-(i-j)]:
                j -= 1
            suffix.insert(0, i-j)
        return suffix

    def _get_BMgs(self):
        length = len(self.pattern)
        suffix = self._get_suffix()
        BMgs = [length for i in range(0, length)]

        j = 0
        for i in range(length-1, -1, -1):
            if suffix[i] == i+1:
                while j < length-1-i:
                    if BMgs[j] == length:
                        BMgs[j] = length-1-i
                    j += 1
        for i in range(0, length-1):
            BMgs[length-1-suffix[i]] = length-i-1
        return BMgs

    def _get_BMbc(self):
        length = len(self.pattern)
        BMbc = {}
        for i in range(0, length):
            BMbc[self.pattern[i]] = length - 1 - i
        return BMbc

    def find(self, primary_string):
        primary_length, pattern_length = len(primary_string), len(self.pattern)

        j = 0
        while j <= primary_length-pattern_length:
            i = pattern_length-1
            while i >= 0 and self.pattern[i] == primary_string[i+j]:
                i -= 1
            if i < 0:
                return j
            else:
                j += max(self._BMgs[i], self._BMbc.get(primary_string[i+j],pattern_length)-(pattern_length-1-i))
        return -1

class AC_node:
    def __init__(self):
        self.goto = {}
        self.fail = None
        self.output = []

class AC:
    def __init__(self, patterns):
        self.patterns = patterns
        self.root = AC_node()
        # 建立goto表
        for pattern in self.patterns:
            cur = self.root
            for c in pattern:
                if cur.goto.get(c) is None:
                    child_node = AC_node()
                    cur.goto[c] = child_node
                    cur = child_node
                else:
                    cur = cur.goto[c]
            cur.output.append(pattern)

        # 建立fail表
        node_one_floor = self.root.goto.values()
        for child in node_one_floor:  # 第一层的失败节点都是root
            child.fail = self.root
        while node_one_floor:
            node_next_floor = []  # 一层一层迭代建立fail表
            for node in node_one_floor:
                node_next_floor.extend(node.goto.values())  # 获得下一层节点

                # 为下层节点建立fail表
                for c, child in node.goto.items():
                    fs = node.fail
                    while fs is not None and fs.goto.get(c) is None:
                        fs = fs.fail
                    if fs is not None: # 表示fs.goto[c] is not None
                        child.fail = fs.goto[c]
                    else:
                        child.fail = self.root
                    child.output.extend(child.fail.output)
            node_one_floor = node_next_floor

    def find(self, primary_string):
        # result = []
        cur = self.root

        i = 0
        for c in primary_string:
            while cur is not None and cur.goto.get(c) is None:
                cur = cur.fail
            if cur is not None:
                cur = cur.goto[c]
            else:
                cur = self.root
            if len(cur.output) != 0:
                return i-(len(cur.output[0])-1)
            # for item in cur.output:
            #     result.append((i-(len(item)-1), item))
            i += 1

        return -1

if __name__ == '__main__':
    test = AC(['mother', 'father'])
    print(test.find('father mother'))