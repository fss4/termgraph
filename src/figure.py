import csv
from math import *
from numpy import linspace, vectorize

from config import *
from utils import format_digits

class Figure():
    def __init__(self, xrange=XRANGE, yrange=YRANGE, scale=SCALE):
        if scale < 1:
            raise Exception("Scale must be greater than 1.0.")
        self.scale = scale
        self.diff = (floor(XDIFF * self.scale), floor(YDIFF * self.scale))
        self.graph_size = ((self.diff[0] * NUMARK) + 1, (self.diff[1] * NUMARK) + 1)
        
        # +2 in first entry is for axis (space needed on left to make markers the correct size),
        # +2 in second entry is for axis + marker label.  The +3 is for the last x-axis marker label.
        self.field_size = (NUMCHAR + 2 + XPAD + self.graph_size[0] + 3, self.graph_size[1] + YPAD + 2)

        
        #These denote list positions in python corresponding to a pixel.  So, the top left corner is (0,0) 
        self.axis_origin = (NUMCHAR + 1, self.field_size[1] - 1 - 1)
        self.graph_origin = (NUMCHAR + 2 + XPAD, self.field_size[1] - 1 - 2 - YPAD)
        
        self.xmin, self.xmax = xrange
        self.ymin, self.ymax = yrange
        self.xgrid = vectorize(format_digits)(
            linspace(self.xmin,self.xmax,self.graph_size[0])
        )
        self.ygrid = vectorize(format_digits)(
            linspace(self.ymin,self.ymax,self.graph_size[1])
        )
        
        self.field = [[' ' for _ in range(self.field_size[0])] for _ in range(self.field_size[1])]
        
    def __str__(self):
        fig = ''
        fig += '\n'
        for line in self.field:
               fig += ''.join(line) + '\n'
        return fig
    
    def build_axes(self, check_alignment=False):
        
        #These are some odd spots that aren't affected by the loops so we define them by hand
        self.field[self.axis_origin[1]][self.axis_origin[0]] = '\u2514'
        self.field[self.axis_origin[1]][self.field_size[0] - 3] = '\u2574'
        self.field[self.axis_origin[1]][self.axis_origin[0] + 1 : self.axis_origin[0] + 1 + XPAD] = '\u2500'*XPAD
        self.field[self.axis_origin[1] - 1][self.axis_origin[0]] = '\u2502'
        
        
        xmarkers = self.xgrid[::self.diff[0]]
        ymarkers = self.ygrid[::self.diff[1]]
        
        x = self.axis_origin[0]
        ystart = self.graph_origin[1]
        yend = 0
        label = 0
        for yoffset in range(0, yend-ystart - 1, -1):
            y = ystart + yoffset
            if yoffset % self.diff[1] == 0:
                self.field[y][x-1] = '\u2576'
                self.field[y][x] = '\u253C'
                self.field[y][x+1] = '\u2574'
                self.field[y][x-1-len(ymarkers[label]):x-1] = ymarkers[label]
                label += 1 
            else:
                self.field[y][x] = '\u2502'
        
        
        #The +1 here in the beginning of the range is there for the same reason as the < in the above elif: 
        #because the actual origin cell is taken up by the special character connecting the axes \u2514.
        y = self.axis_origin[1]
        xstart = self.graph_origin[0]
        xend = self.field_size[0] - 3
        label = 0
        for xoffset in range(xend - xstart):
            x = xstart + xoffset
            if xoffset % self.diff[0] == 0:
                self.field[y][x] = '\u253C'
                pt = len(xmarkers[label])//2
                self.field[y + 1][x-pt:x-pt+len(xmarkers[label])] = xmarkers[label]
                label += 1
            else:
                self.field[y][x] = '\u2500' 
        
        
        x = self.axis_origin[0] - 1
        
        for y in range(self.field_size[1]):
            if y % self.diff[1] == 0 and y <= self.graph_size[1]:
                #label += 1
                pass
                
        y = self.axis_origin[1] + 1
        label = 0
        for x in range(self.axis_origin[0] + 1, self.field_size[0] - 1):
            if x % self.diff[0] == XPAD:
                pt = len(xmarkers[label])//2
                #self.field[y][x-pt:x-pt+len(xmarkers[label])] = xmarkers[label]
                #label += 1
                
        #If check_alignment is true this puts a dot at each of the four corners of the graph area.
        #primarily useful if tweaking stuff
        if check_alignment:
            self.field[self.graph_origin[1]][self.graph_origin[0]] = '\u25CF'
            self.field[self.graph_origin[1]][self.graph_origin[0]  + self.graph_size[0] - 1] = '\u25CF'
            self.field[self.graph_origin[1] - (self.graph_size[1] - 1)][self.graph_origin[0]] = '\u25CF'
            self.field[self.graph_origin[1] - (self.graph_size[1] - 1)][self.graph_origin[0] + self.graph_size[0] - 1] = '\u25CF'
            
    def load_data(self, data_path):
        data = []
        with open(data_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append([float(row[0]),float(row[1])])
        if len(data) != self.graph_size[0]:
            raise Exception("Something went wrong. The data you are trying to load is not the same size as the graphing space.")
        ystart = self.graph_origin[1]
        xstart = self.graph_origin[0]
        jprev = None
        for i in range(self.graph_size[0]):
            fcur = data[i][1]
            x = xstart + i
            j = 0
            if fcur < float(self.ygrid[0]):
                j = -1
            if fcur > float(self.ygrid[-1]):
                j = self.graph_size[1]
                y = ystart - j
            #find the cell to populate given the function value
            while 0 <= j < self.graph_size[1]:
                if float(self.ygrid[j]) < fcur:
                    j += 1
                    continue
                else:
                    y = ystart - j
                    self.field[y][x] = '\u25CF'
                    break
            #populate all cells vertically between the current and the previous datapoint
            if i != 0 and abs(j-jprev) > 1:
                #if the previous entry is greater than the current
                if j < jprev:
                    print(j, jprev)
                    for k in range(ystart - jprev + 1, y):
                        self.field[k][x] = '\u25CF'
                #if the previous entry less than the current but not from outside the graph and the current entry is inside
                elif jprev >= 0:
                    print(j, jprev)
                    for k in range(y + 1, ystart - jprev):
                        self.field[k][x-1] = '\u25CF'
                #if the previous entry less than the current and from outside the graph
                else:
                    print(j, jprev)
                    for k in range(y + 1, ystart + 1):
                        self.field[k][x-1] = '\u25CF'
            jprev = j
                    
        
        

fig = Figure(xrange=(-2,2), yrange=(-2,4), scale=2)
fig.build_axes()
print(f'field size: {fig.field_size}')
print(f'graph size: {fig.graph_size}')
print(f'graph origin: {fig.graph_origin}')
print(f'axis origin: {fig.axis_origin}')
fig.load_data("data.csv")
print(fig)


