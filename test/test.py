import random as r
import csv
import os
import sys

script_dir = os.path.dirname(__file__)

data = []
for _ in range(int(sys.argv[1])):
    x = r.gauss()
    y = r.gauss()  
    data.append([x,y])
    
with open(os.path.join(script_dir,"test_data.csv"), "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)