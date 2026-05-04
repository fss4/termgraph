import argparse
import os
import shutil

from src.genpoints import gen_fdata
from src.config import *

script_dir = os.path.dirname(__file__)

def main():
    parser = argparse.ArgumentParser(prog="termgraph", description="A terminal-based graphing calculator.")
    
    #There are two modes.  The default expectation is the input is simply the RHS of f(x) = polynomial.
    parser.add_argument('-t', '--type', type=str, default='function', choices=['function', 'list'], help='The type of data you are trying to graph. Default is "function"; secondary option is "list".')
    parser.add_argument('data', type=str, help='By default should be a polynomial in x using python formatting i.e. "x**3 + 2*x**2 + 3". If -t is set to "list" it should be a path to an'\
                        'appropriately formatted .csv file containing (x,y) values on each line.')
    parser.add_argument('-x', '--xrange', type=tuple, default=XRANGE, help=f'Two-entry tuple that defines the domain of the graph. Default is {XRANGE}.')
    parser.add_argument('-y', '--yrange', type=tuple, default=YRANGE, help=f'Two-entry tuple that defines the range of the graph. Default is {YRANGE}.')
    parser.add_argument('-s', '--scale', type=float, default=1.0, help='Scale multiplier for the size of the graph to be plotted in terminal. 1.0 by default.')

    args = parser.parse_args()
    if len(args.xrange) != 2 or len(args.yrange) != 2:
        raise Exception("Range and domain must be length-two tuples.")
    for i in range(2):
        if not(str(args.xrange[i]).isnumeric() or str(args.yrange[i]).isnumeric()): 
            raise Exception("Range and domain must contain numbers.")
    if (float(args.xrange[0]) >= float(args.xrange[1])) or (float(args.yrange[0]) >= float(args.yrange[1])):
        raise Exception("Range and domain must be ordered tuples where the first entry is strictly less than the second")

    if args.type == 'function':
        gen_fdata(args.data, float(args.xrange[0]), float(args.xrange[1]), args.scale)
    elif args.type == 'list':
        shutil.copyfile(args.data, os.path.join(script_dir,"src/data.csv"))
            
    
    print(args.type)
    print(args.data)
    print(args.xrange)
    print(args.yrange)
    size = 40
    for i in range(size//2 + 2):
        if i % 5 == 0 and i <= size//2:
            print('\u2015' + '  ' + '\u2731'*(size +1))  
        elif i <= size//2:
            print('\u23d0' + '  ' + '\u2731'*(size +1))
        else:
            print('\u23d0')
    b_str = list('  ' + '\u2015'*(size + 2))
    for i in range(len(b_str)):
        if i % 10 == 3:
            b_str[i] = '|'
    print(''.join(b_str))
if __name__ == "__main__":
    main()
