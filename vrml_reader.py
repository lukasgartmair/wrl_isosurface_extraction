#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:21:42 2016

@author: lukas
"""
import numpy as np
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import axes3d

coords = np.genfromtxt('iso_coords_formatted.txt')

indices = np.genfromtxt('iso_indices_formatted.txt',dtype=np.int64)

fig = pl.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(coords[:,0],coords[:,1],coords[:,2])

f = open('isosurface.obj','w')
for i in range(len(coords)):
    f.write('v ' + str(coords[i,0]) + ' ' + str(coords[i,1]) + ' ' +str(coords[i,2]) + '\n') # python will convert \n to os.linesep

for i in range(len(indices)):
    f.write('f ' + str(indices[i,0]+1) + ' ' + str(indices[i,1]+1) + ' '+ str(indices[i,2]+1) + '\n') # python will convert \n to os.linesep

                       
f.close() # you can omit in most cases as the destructor will call it
    
