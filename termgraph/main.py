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
    parser.add_argument('-l', action='store_true',help='Indicates that a list is to be graphed rather than a polynomial')
    parser.add_argument('data', type=str, help='This defines what is to be graphed. By default it should be a polynomial in x using python formatting i.e. "x**3 + 2*x**2 + 3". If -l is set it should be a path to an'\
                        'appropriately formatted .csv file containing (x,y) values on each line.  Leading negative signs must be written as multiplication by (-1) or placed in parentheses e.g. (-1)*x**3 or (-x**3). Between terms in a function this is not necessary.  '\
                        'If spaces are not included in your function it is not necessary to enter it in quotes but it is recommended to always do so.  Use of ^ for exponents is included but the entire term must be placed in '\
                        'parentheses or whatever follows will be included in the exponent i.e. "(x^2) - 3" != "x^2 - 3" = "x^-1".')
    parser.add_argument('-x', '--xrange', nargs=2, metavar=('XMIN','XMAX'), type=float, default=XRANGE, help=f'Two-entry option that defines the domain of the graph. Default is {XRANGE[0]}, {XRANGE[1]}.')
    parser.add_argument('-y', '--yrange', nargs=2, metavar=('YMIN','YMAX'), type=float, default=YRANGE, help=f'Two-entry option that defines the range of the graph. Default is {YRANGE[0]}, {YRANGE[1]}.')
    parser.add_argument('-s', '--scale', type=float, default=SCALE, help='Scale multiplier for the size of the graph to be plotted in terminal. 1.0 by default.')
    parser.add_argument('-a', action='store_true', help='Flag indicating the range should be auto-adjusted to match max and min values of f(x) (assuming they arent infinite); for a function or the maximum datapoint '\
                        'values for a list.  If the flag is not set the plot will use the default range.')
    parser.add_argument('-o', nargs='*',type=float, default=False, help='Turns on lines through the origin.  If no argument is given the origin is set to (0,0).')


    args = parser.parse_args()
    
    if (args.xrange[0] >= args.xrange[1]) or (args.yrange[0] >= args.yrange[1]):
        parser.error("Range and domain must be ordered tuples where the first entry is strictly less than the second")
    
    if not args.l:
        gen_fdata(args.data, args.xrange[0], args.xrange[1], args.scale)
    else:
        try:
            shutil.copyfile(args.data, os.path.join(script_dir,"data.csv"))
        except:
            parser.error("An error has occured.  Perhaps you tried to graph a function with -l on?")
    
    if args.a:
        data = []
        with open(os.path.join(script_dir,"data.csv"),'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if ((isfinite(float(row[1])) and isfinite(float(row[0])))):
                    data.append([float(row[0]),float(row[1])])
        if args.l:
            args.xrange = (min(data,key=lambda x:x[0])[0], max(data,key=lambda x:x[0])[0])
        args.yrange = (min(data,key=lambda x:x[1])[1], max(data,key=lambda x:x[1])[1])
        if (args.xrange[0]  == args.xrange[1]):
            args.xrange = (args.xrange[0] - .1, args.xrange[1] + .1)
        if (args.yrange[0]  == args.yrange[1]):
            args.yrange = (args.yrange[0] - .1, args.yrange[1] + .1)
    fig = Figure(xrange=args.xrange, yrange=args.yrange, scale=args.scale)
    fig.build_axes()
    if args.o is not False:
        if len(args.o) != 2 and len(args.o) != 0:
            parser.error("-o only takes 0 or 2 arguments.")
        elif len(args.o) == 2:
            fig.origin = args.o
            fig.build_origin()
        else:
            fig.build_origin()
    
    if not args.l:
        fig.load_function(os.path.join(script_dir,"data.csv"))
        print("\n")
        print(f'{" "*(NUMCHAR)}f(x)={str(args.data).replace(' ', '')}') 
        print(fig)
        
    elif args.l:
        data_align(os.path.join(script_dir,"data.csv"), *args.xrange, *args.yrange, args.scale)
        fig.load_list(os.path.join(script_dir,"data.csv"))
        print("\n")
        print(f'Data from {args.data}')
        print(fig)
        
if __name__ == "__main__":
    main()
