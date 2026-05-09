import csv
from math import *
import numpy as np

from termgraph.config import *
from termgraph.utils import format_digits, bin_data

class Figure():
    def __init__(self, xrange=XRANGE, yrange=YRANGE, scale=SCALE, origin=ORIGIN):

        self.scale = scale
        self.diff = (floor(XDIFF * self.scale), floor(YDIFF * self.scale))
        if 0 in self.diff:
            raise Exception("Your scale multiplier is too small and the graph cannot be rendered.") 
        self.graph_size = ((self.diff[0] * NUMARK) + 1, (self.diff[1] * NUMARK) + 1)
        
        # +2 in first entry is for axis (space needed on left to make markers the correct size),
        # +2 in second entry is for axis + marker label.  The +3 is for the last x-axis marker label.
        self.field_size = (NUMCHAR + 2 + XPAD + self.graph_size[0] + 3, self.graph_size[1] + YPAD + 2)

        
        #These denote list positions in python corresponding to a pixel.  So, the top left corner is (0,0) 
        self.axis_origin = (NUMCHAR + 1, self.field_size[1] - 1 - 1)
        self.graph_origin = (NUMCHAR + 2 + XPAD, self.field_size[1] - 1 - 2 - YPAD)
        
        self.origin = origin
        self.xmin, self.xmax = xrange
        self.ymin, self.ymax = yrange
        self.xgrid = np.vectorize(format_digits)(
            np.linspace(self.xmin,self.xmax,self.graph_size[0])
        )
        self.ygrid = np.vectorize(format_digits)(
            np.linspace(self.ymin,self.ymax,self.graph_size[1])
        )
        
        self.field = [[' ' for _ in range(self.field_size[0])] for _ in range(self.field_size[1])]
        
    def __str__(self):
        fig = ''
        fig += '\n'
        for line in self.field:
               fig += ''.join(line) + '\n'
        return fig
    
    def build_axes(self):
        
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
        
        
        '''x = self.axis_origin[0] - 1
        
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
                #label += 1'''
    
    def build_origin(self):
        ystart = self.graph_origin[1]
        xstart = self.graph_origin[0]
        
        xgrid = np.vectorize(float)(self.xgrid)
        ygrid = np.vectorize(float)(self.ygrid)
        xbin = xgrid[1]-xgrid[0]
        ybin = ygrid[1]-ygrid[0]
        origin_coord = [None,None]
        if self.xmin < self.origin[0] < self.xmax:
            for i in range(self.graph_size[0]):
                if i == 0 and ((xgrid[i] - .5*xbin) <= self.origin[0]  < (xgrid[i] + .5*xbin)):
                    origin_coord[0] = 0
                    break
                if i > 0 and ((xgrid[i-1] + .5*xbin) <= self.origin[0] < (xgrid[i] + .5*xbin)):
                    origin_coord[0] = i
                    break
            x = origin_coord[0]
            for y in range(self.graph_size[1]):
                self.field[ystart - y][xstart + x] = '\u00B7'
                
        if self.ymin < self.origin[1] < self.ymax:
            for i in range(self.graph_size[1]):
                if i == 0 and ((ygrid[i] - .5*ybin) <= self.origin[1]  < (ygrid[i] + .5*ybin)):
                    origin_coord[1] = 0
                    break
                if i > 0 and ((ygrid[i-1] + .5*ybin) <= self.origin[1] < (ygrid[i] + .5*ybin)):
                    origin_coord[1] = i
                    break
            y = origin_coord[1]
            for x in range(self.graph_size[0]):
                self.field[ystart - y][xstart + x] = '\u00B7'
        
        
        
        
            
    def load_function(self, data_path):
        data = []
        with open(data_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not isnan(float(row[1])):
                    data.append([float(row[0]),float(row[1])])
                else:
                    data.append([float(row[0]),nan])

        ystart = self.graph_origin[1]
        xstart = self.graph_origin[0]
        
        data = bin_data(data,np.vectorize(float)(self.xgrid),pos=0)
        binsize = float(self.ygrid[1]) - float(self.ygrid[0])
        for pt in data:
            if (self.ymax + .5*binsize) <= pt[1]:
                pt[1] = self.graph_size[1]
            elif pt[1] < (self.ymin - .5*binsize):
                pt[1] = -1
            else:
                for i in range(self.graph_size[1]):
                    if i == 0 and ((float(self.ygrid[i]) - .5*binsize) <= pt[1] < (float(self.ygrid[i]) + .5*binsize)):
                        pt[1] = i
                        break
                    if i > 0 and ((float(self.ygrid[i-1]) + .5*binsize) <= pt[1] < (float(self.ygrid[i]) + .5*binsize)):
                        pt[1] = i
                        break
        
        for i, pt in enumerate(data):
            if not isfinite(pt[1]):
                continue
            if 0 <= pt[1] < self.graph_size[1]:
                self.field[ystart - pt[1]][xstart + pt[0]] = '\u25CF'
            if (0 <= i < len(data) -1) and pt[1] > data[i+1][1] + 1:
                for j in range(data[i+1][1] + 1, pt[1]):
                    self.field[ystart - j][xstart + data[i][0]] = '\u25CF'
            elif (0 <= i < len(data) -1) and pt[1] + 1 < data[i+1][1]:
                for j in range(pt[1] + 1, data[i+1][1]):
                    self.field[ystart - j][xstart + data[i+1][0]] = '\u25CF'
        
            
    def load_list(self, data_path):
        #this data is pre-processed so that the x-values are already offsets
        data = []
        with open(data_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append([int(row[0]),int(row[1])])

        
        ystart = self.graph_origin[1]
        xstart = self.graph_origin[0]

        for pt in data:
            self.field[ystart - pt[1]][xstart + pt[0]] = '\u25CF'
        
                
