import ast
import os
import warnings
import csv

from simpleeval import SimpleEval, BASIC_ALLOWED_ATTRS, safe_power
from math import *
from numpy import linspace

from termgraph.config import *

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
    

def bin_data(data, grid, pos=0):
    '''
    This function bins a sorted dataset (given as a list of lists) into a given grid.
    The grid values are taken to be the middle of the bins.
    The dataset is assumed to lie entirely within the grid.
    Optional value pos is in case you want to bin along a different value than the first one.
    '''
    size = len(grid)
    binsize = grid[1]-grid[0]
    iprev = 0
    data_cpy = data.copy()
    for pt in data_cpy:
        i = iprev
        #print(pt)
        while not ((grid[i] - .5*binsize) <= pt[pos] < (grid[i] + .5*binsize)):
            #print(((grid[i] - .5*binsize) , pt[pos] , (grid[i] + .5*binsize)))    
            i += 1
            if i >= size:
                raise Exception("An error has occurred, binning has left the graph area.")
        pt[pos] = i
        iprev = i
    return data_cpy
        
def data_align(data_path, xmin, xmax, ymin, ymax, scale):
    data = []
    xsize = (floor(XDIFF * scale) * NUMARK) + 1
    ysize = (floor(YDIFF * scale) * NUMARK) + 1

    xgrid = linspace(xmin,xmax,xsize)
    ygrid = linspace(ymin,ymax,ysize)
    
    with open(data_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if isfinite(float(row[0])) and isfinite(float(row[1])):
                    data.append([float(row[0]),float(row[1])])
                else:
                    raise Exception("There appears to be bad points (either NaN or inf) in your data.  Please clean it before trying to plot.")

    tmp = data.copy()
    for pt in tmp:
        if pt[0] < xmin or pt[0] > xmax:
            data.remove(pt)
    tmp = data.copy()
    for pt in tmp:
        if pt[1] < ymin or pt[1] > ymax:
            data.remove(pt)
    data.sort(key = lambda x: x[0])
    data = bin_data(data,xgrid,pos=0)
    data.sort(key = lambda x: x[1])
    graph_data = bin_data(data,ygrid,pos=1)
    
    with open(data_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(graph_data)
        
        
        
        
        

    
    
