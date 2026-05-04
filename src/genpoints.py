import ast
import os

from simpleeval import SimpleEval, BASIC_ALLOWED_ATTRS, safe_power
from math import *
from numpy import linspace

def gen_fdata(f_str, xmin, xmax, scale):
    def f(x):
        s = SimpleEval(allowed_attrs=BASIC_ALLOWED_ATTRS)
        s.operators[ast.BitXor] = safe_power
        s.names = {"x" : x}
        return s.eval(f_str)
    
    size = floor(40 * scale)
    x_grid = linspace(xmin,xmax,size)
    res = []
    for x in x_grid:
        res.append([float(x),float(f(x))])
        
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, "data.csv")
    with open(filepath, "w") as file:
        for pt in res:
            file.write(f"{pt[0]},{pt[1]}\n")


    
    
