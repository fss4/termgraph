## About
-----------
This is a simple CLI-based program that acts as a graphing calculator in the terminal. The default behavior is to take a python-formatted function as input which is then output as a graph in the terminal.  There is also functionality for a `.csv` file input formatted as pairs of (x,y) points which is then graphed in the terminal.  The program  can plot any of the usual real, piecewise continuous functions available in Python's `math` module.

## Installation
-----------
To install the program you can either clone the repo and then work inside of it once you set up the venv.

Alternatively, there is an installation script available here that uses [pipx](https://pipx.pypa.io/stable/) to install it (without cluttering up your python install) in a way that makes the `termgraph` command available anywhere in your terminal.  All this does is pipe the `install.sh` script into bash and you can check it here if you want to make sure its safe.
```
curl -fSL https://raw.githubusercontent.com/fss4/termgraph/main/install.sh | bash
```
be sure to run this command in whatever directory you want the repo installed.  Probably a downloads folder or something

## Plotting Functions:
-----------
In order to plot functions one runs something along the lines of:
```
termgraph -x -5 10 -y -.3 1.1 -s 1.4 "sin(x)/x"
```
![img](img/sinc.png)

Here the `-x` and `-y` flags are for setting the domain and range of the graph.  The scale multiplier is set by `-s`, this makes the graph larger on your screen.

Alternatively, for a polynomial with no optional settings the default would just be:
```
termgraph "x**3"
```
![img](img/xcubed.png)

If you would like the range to be auto-set you can use the `-a` flag:
```
termgraph "x**3 - 2*x" -a
```
![img](img/autoscale.png)

Parametric functions can be plotted using the `-p` flag:
```
termgraph "(2*cos(t)+5*cos((2/3)*t)),(2*sin(t)-5*sin((2/3)*t))" -p 0 100 -s 2.5 -a -o
```
![img](img/parametric.png)

## Plotting Data
-----------
In order to plot data you must set the `-l` flag and provide a path to a `.csv`.  For example:
```
termgraph -l test/test_data.csv
```
![img](img/scatter.png)

The test data here is created by running the test.py program available in the test directory; its just some gaussian data centered at 0.  
If you dont have two column csv data readily available this would be an easy way to play with the 
scatter plot functionality.  To generate the data, inside the main directory simply run
```
python3 test/test.py [NUM DATA PTS TO GENERATE]
```

The `-a` flag is also available for lists of data in which case it scales the x and y axes to fit all points.  This is very useful if you do not know the scale of the data you want to plot

## Available Flags
-----------
- `-l` Indicates the input is a filepath to a dataset.
- `-p` \[TMIN\] \[TMAX\] Indicates the input is a parametric function "x(t),y(t)".
- `-x` \[XMIN\] \[XMAX\] Customize the domain of the graph.
- `-y` \[YMIN\] \[YMAX\] Customize the range of the graph.
- `-o` \[XPOS\] \[YPOS\] Customize the origin of the graph and place lines going through it.  No argument defaults to (0,0).
- `-s` \[SCALE\] Scale factor to resize the graph.
- `-a` Indicates the graph should have its range set automatically.  Lists and parametric functions will have the domain changed as well.