#Size in character entries the graph space takes up in the x-direction
#Size in the y-direction is set here to half the x-direction size to make the field approximately square
XSIZE = 40
YSIZE = XSIZE//2
SCALE = 1.0

#Number of axis marks (not including the one at 0)
NUMARK = 4

#Spacing between markers on the x and y axes. y axes is once again set to half the x size.
XDIFF = XSIZE//NUMARK
YDIFF = YSIZE//NUMARK


#Padding for spacinf between axis and graph.  
# Note the x padding is vertical spacing and y is horizontal. The final setting is the size of the labels
XPAD = 3
YPAD = XPAD//2
NUMCHAR = 8

#Default ranges for the graph
XRANGE = (-2,2)
YRANGE = (-2,2)
ORIGIN = (0,0)

#Default range for parametric functions
TRANGE = [0,1]
TSIZE = 1000

