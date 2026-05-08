## About
-----------
This is a simple CLI-based program that acts as a graphing calculator in the terminal. The default behavior is to take a python-formatted function as input which is then output as a graph in the terminal.  There is also functionality for a .csv file input which is formatted as pairs of (x,y) points which is then graphed in the terminal.  The program  can plot any of the usual real, piecewise continuous functions available in Python's `math` module.

## Plotting Functions:
-----------
In order to plot functions one runs something along the lines of:
```
termgraph -x -3 3 -y -1.2 1.2 -s 1.4 "sin(x)/x"
```
or for a polynomial with no optional settings:
```
termgraph "x**3"
```
If you would like the range to be auto-set you can use the `-a` flag:
```
termgraph "x**3 + 2*x" -a
```
## Plotting Data
-----------
In order to plot data you must set the `-l` flag and provide a path to a `.csv`.  For example:
```
termgraph -l test/test_data.csv
```
The `-a` flag is also available for lists of data.