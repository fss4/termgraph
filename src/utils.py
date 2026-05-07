import ast
import os
import warnings

from simpleeval import SimpleEval, BASIC_ALLOWED_ATTRS, safe_power
from math import *
from numpy import linspace

from config import *

def gen_fdata(f_str, xmin, xmax, scale):
    def f(x):
        s = SimpleEval(allowed_attrs=BASIC_ALLOWED_ATTRS)
        s.operators[ast.BitXor] = safe_power
        s.functions = {"exp":exp, "ln": log, "log": log, "log2": log2, "log10":log10,
                       "acos": acos, "asin":asin, "atan":atan,"cos":cos,"sin":sin,"tan":tan,
                       "acosh":acosh,"asinh":asinh,"atanh":atanh,"cosh":cosh,"sinh":sinh, "tanh":tanh,
                       "erf": erf, "erfc":erfc, "gamma":gamma, "lgamma":lgamma}
        s.names = {"x" : x}
        return s.eval(f_str)
    
    size = (floor(XDIFF * scale) * NUMARK) + 1
    print(size)
    xgrid = linspace(xmin,xmax,size)
    res = []
    for x in xgrid:
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            try:
                res.append([float(x),float(f(x))])
            except:
                res.append([float(x),float(nan)])
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, "data.csv")
    with open(filepath, "w") as file:
        for pt in res:
            file.write(f"{pt[0]},{pt[1]}\n")

def format_digits(x):
    if ((x >= 1e100 or x <= -1e100) or (-1e-99 < x < 1e-99)) and x != 0:
        raise Exception("Range and domain must be strictly in (-1e100, -1e-99) \u222A (1e-99, 1e100).")
    if x > 0:
        if x >= 100000000 or x < 0.000001:
            return f'{x:.2e}'
        else:
            oom = floor(log10(x))
            if oom >= 6:
                return str(int(x))
            elif oom >= 0:
                return str(round(x,6-oom))
            else:
                return str(round(x,6))
    elif x < 0:
        if x <= -10000000 or x > -0.00001:
            return f'{x:.1e}'
        else:
            oom = floor(log10(abs(x)))
            if oom >= 5:
                return str(int(x))
            elif oom >= 0:
                return str(round(x,5-oom))
            else:
                return str(round(x,5))
    else:
        return str(x)
    
def interpolate(x0, x1):
    pass
    

        
        

    
    
