from pykeyboard import PyKeyboard
from fractions import Fraction

import threading

key = PyKeyboard()  # 键盘  k.tap_key('a')  k.press_key()  k.release_key()

ad_ = 0
bpm_ = 60
ver_ = 1


def ad(x):
    global ad_
    ad_ = int(x)


def bpm(x):
    global bpm_
    bpm_ = x


def ver(x):
    global ver_
    ver_ = x


num = ['1--', '2--', '3--', '4--', '5--', '6--', '7--',
       '1-', '2-', '3-', '4-', '5-', '6-', '7-',
       '1', '2', '3', '4', '5', '6', '7',
       '1+', '2+', '3+', '4+', '5+', '6+', '7+',
       '1++', '2++', '3++', '4++', '5++', '6++', '7++']
note = ['z', 'z', 'z', 'z', 'z', 'z', 'z',
        'z', 'x', 'c', 'v', 'b', 'n', 'm',
        'a', 's', 'd', 'f', 'g', 'h', 'j',
        'q', 'w', 'e', 'r', 't', 'y', 'u',
        'u', 'u', 'u', 'u', 'u', 'u', 'u']


def kk(x):
    lip = num.index(x) + ad_
    if lip > 34:
        lip = 34
    if lip < 0:
        lip = 0
    return note[lip]


def pau(t):
    return Fraction(Fraction(60, int(bpm_)), Fraction(str(ver_))) * t


# 一行转化为keys(字母), times(累加,现实sec)
def line(x):
    a = x[1:] + '('
    keys, times = [], []

    def word(y):
        k = ''
        while y.index(')') > 0:
            if y[0] == '0':
                k = ''
                y = y[1:]
            elif y[1:3] == '++' or y[1:3] == '--':
                k += kk(y[0:3])
                y = y[3:]
            elif y[1:2] == '+' or y[1:2] == '-':
                k += kk(y[0:2])
                y = y[2:]
            else:
                k += kk(y[0])
                y = y[1:]
        t = pau(Fraction(y[1:]))
        return k, t

    while len(a) > 1:
        k1, t1 = word(a[:a.index('(')])
        keys.append(k1)
        if len(times) > 0:
            times.append(t1 + times[-1])
        else:
            times.append(t1)
        a = a[a.index('(') + 1:]
    return keys, times

# mix 2条音轨，time（输入：累加）
def mix(k1, t1, k2, t2):
    tm = max(t1[-1], t2[-1])
    t1 = [Fraction(0)] + t1[:-1]
    t2 = [Fraction(0)] + t2[:-1]
    while len(t2) > 0:
        if t2[0] in t1:
            ix = t1.index(t2[0])
            k1[ix] += k2[0]
        elif t2[0] > max(t1):
            t1.append(t2[0])
            k1.append(k2[0])
        else:
            for i in range(len(t1)):
                if t2[0] < t1[i]:
                    k1.insert(i, k2[0])
                    t1.insert(i, t2[0])
                    break
        t2.pop(0), k2.pop(0)
    t1.pop(0), t1.append(tm)
    for i in range(len(k1)):
        text = ''
        for j in k1[i]:
            if j not in text:
                text += j
        k1[i] = text
    return k1, t1


def read_txt(dress):
    data = []
    for line1 in open(dress, "r",encoding='utf-8'):
        if line1[-1] != '\n':
            data.append(line1)
        else:
            data.append(line1[:-1])
    return data


def txt_kt_mixed(dress, p=True):
    txt = read_txt(dress)
    if p is False and 's' not in txt:
        p = True
    k0, t0 = [], []
    k1, t1 = [''], [Fraction(0)]
    for i in range(len(txt)):
        if txt[i][0:2] == 'ad':
            ad(txt[i][3:-1])
            # print('ad set: ', txt[i][3:-1])
        if txt[i][0:3] == 'bpm':
            bpm(txt[i][4:-1])
            # print('bpm set: ', txt[i][4:-1])
        if txt[i][0:3] == 'ver':
            ver(txt[i][4:-1])
            # print('ver set: ', txt[i][4:-1])
        if txt[i][0:1] == 's':  # 开始位点
            p = True
        if txt[i][0:1] == 'e':  # 结束位点
            p = False
            k0 = k0 + k1
            if not t0:
                t0 = t1
            else:
                t0_m = t0[-1]
                for ts in t1:
                    t0.append(t0_m + ts)
            k1, t1 = [''], [Fraction(0)]
        if p:
            if txt[i][0:1] == '(':
                k2, t2 = line(txt[i])
                k1, t1 = mix(k1, t1, k2, t2)
            if txt[i][0:1] == '#':  # 添加一节
                # print(k1)
                # print(i+1, '=', txt[i])
                k0 = k0 + k1
                if not t0:
                    t0 = t1
                else:
                    t0_m = t0[-1]
                    for ts in t1:
                        t0.append(t0_m+ts)
                k1, t1 = [''], [Fraction(0)]
    return k0, t0


def time_short(s):
    if s < 60:
        if s < 10:
            return '0:0'+str(s)
        else:
            return '0:'+str(s)
    else:
        m = s//60
        s = s - 60 * m
        if s < 10:
            s = '0'+str(s)
        return str(m)+':'+str(s)




import ctypes
import inspect
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_Mythread(thread):
    _async_raise(thread.ident, SystemExit)




class Mythread(threading.Thread):
    def __init__(self, func):
        """
        func: run方法中要调用的函数名
        args: func函数所需参数
        """
        threading.Thread.__init__(self)
        self.func = func
    def run(self):
        self.func()







