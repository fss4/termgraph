import argparse
import os
import shutil
import csv
from math import *

from termgraph.utils import *
from termgraph.figure import *
from termgraph.config import *


script_dir = os.path.dirname(__file__)

def main():
    parser = argparse.ArgumentParser(prog="termgraph", description="A terminal-based graphing calculator.")
    
    #There are two modes.  The default expectation is the input is simply the RHS of f(x) = polynomial.
    parser.add_argument('data', type=str, help='This defines what is to be graphed. By default it should be a polynomial in x using python formatting i.e. "x**3 + 2*x**2 + 3". If -l is set it should be a path to an'\
                        'appropriately formatted .csv file containing (x,y) values on each line.  '\
                        'If spaces are not included in your function it is not necessary to enter it in quotes but it is recommended to always do so.  For parametric functions -p is set and the main positional argument '\
                        'should be two functions, both in the variable "t", seperated in the input string by a comma e.g. "cos(t),sin(t)".  '\
                        'Leading negative signs must be written as multiplication by (-1) or placed in parentheses e.g. (-1)*x**3 or (-x**3).'\
                        'Between terms in a function this is not necessary.  Use of ^ for exponents is included but the entire term must be placed in '\
                        'parentheses or whatever follows will be included in the exponent i.e. "(x^2) - 3" != "x^2 - 3" = "x^-1".')
    
    parser.add_argument('-l', action='store_true',help='Indicates that a list is to be graphed.')
    parser.add_argument('-p', nargs='*', metavar='TMIN TMAX', type=float, default=False, help='Indicates that a parametric function is to be graphed. The flag takes a range for the parameter "t" as input. '\
                        f'Default is ({TRANGE[0]}, {TRANGE[1]}).')
    
    parser.add_argument('-x', nargs=2, metavar=('XMIN','XMAX'), type=float, default=XRANGE, help=f'Two-entry option that defines the domain of the graph. Default is ({XRANGE[0]}, {XRANGE[1]}).')
    parser.add_argument('-y', nargs=2, metavar=('YMIN','YMAX'), type=float, default=YRANGE, help=f'Two-entry option that defines the range of the graph. Default is ({YRANGE[0]}, {YRANGE[1]}).')
    parser.add_argument('-s', type=float, metavar='SCALE', default=SCALE, help='Scale multiplier for the size of the graph to be plotted in terminal. 1.0 by default.')
    
    parser.add_argument('-a', action='store_true', help='Flag indicating the range should be auto-adjusted to match max and min values of f(x) (assuming they arent infinite); for a function or the maximum datapoint '\
                        'values for a list.  If the flag is not set the plot will use the default range.')
    parser.add_argument('-o', nargs='*',metavar='XPOS YPOS', type=float, default=False, help='Turns on lines through the origin.  If no argument is given the origin is set to (0,0).')


    args = parser.parse_args()

    if (args.x[0] >= args.x[1]) or (args.y[0] >= args.y[1]):
        parser.error("Range and domain must be ordered tuples where the first entry is strictly less than the second")
    
    
    if args.l:
        try:
            shutil.copyfile(args.data, os.path.join(script_dir,"data.csv"))
        except:
            parser.error("An error has occured.  Perhaps you tried to graph a function with -l set?")
    elif args.p is not False:
        if len(args.p) != 2 and len(args.p) != 0:
            parser.error("-p only takes 0 or 2 arguments.")
        elif len(args.p) == 2:
            gen_pdata(args.data, args.p[0], args.p[1])
        else:
            args.p = TRANGE
            gen_pdata(args.data, args.p[0], args.p[1])
    else:
        gen_fdata(args.data, args.x[0], args.x[1], args.s)
        
    
    if args.a:
        data = []
        with open(os.path.join(script_dir,"data.csv"),'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if ((isfinite(float(row[1])) and isfinite(float(row[0])))):
                    data.append([float(row[0]),float(row[1])])
        if args.l or args.p:
            args.x = (min(data,key=lambda x:x[0])[0], max(data,key=lambda x:x[0])[0])
        args.y = (min(data,key=lambda x:x[1])[1], max(data,key=lambda x:x[1])[1])
        if (args.x[0]  == args.x[1]):
            args.x = (args.x[0] - .1, args.x[1] + .1)
        if (args.y[0]  == args.y[1]):
            args.y = (args.y[0] - .1, args.y[1] + .1)
            
    fig = Figure(xrange=args.x, yrange=args.y, scale=args.s)
    fig.build_axes()
    if args.o is not False:
        if len(args.o) != 2 and len(args.o) != 0:
            parser.error("-o only takes 0 or 2 arguments.")
        elif len(args.o) == 2:
            fig.origin = args.o
            fig.build_origin()
        else:
            fig.build_origin()
    
    if args.l:
        data_align(os.path.join(script_dir,"data.csv"), *args.x, *args.y, args.s)
        fig.load_list(os.path.join(script_dir,"data.csv"))
        print("\n")
        print(f'Data from {args.data}')
        print(fig)
    elif args.p is not False:
        data_align(os.path.join(script_dir,"data.csv"), *args.x, *args.y, args.s)
        fig.load_list(os.path.join(script_dir,"data.csv"))
        tmp = args.data.split(",")
        print("\n")
        print(f'x(t) = {tmp[0]}, y(t) = {tmp[1]}')
        print(fig)
    else:
        fig.load_function(os.path.join(script_dir,"data.csv"))
        print("\n")
        print(f'{" "*(NUMCHAR)}f(x)={str(args.data).replace(' ', '')}') 
        print(fig)
        
if __name__ == "__main__":
    main()
