#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:21:42 2016

@author: lukas
"""
import numpy as np
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import axes3d
import csv
import re

# read in directly the .wrl file and convert the desired lines to an obj file

def get_boundary_lines(iso_string):
    
    boundary_lines = []

    with open('isosurface.wrl', 'r') as fin:
        reader=csv.reader(fin,delimiter=' ')         
        
        coords_offset = 17 # lines
        for num, row in enumerate(reader):
            # find the beginning of the isosurface mesh entry
            if iso_string in row:
                coord_lines_start =  num + 1 + coords_offset
                break
    fin.close()
    boundary_lines.append(coord_lines_start)
    
    with open('isosurface.wrl', 'r') as fin:
        reader=csv.reader(fin,delimiter=' ') 

        for num, row in enumerate(reader):        
            if num > coord_lines_start:
                if ['\t\t\t\t\t\t\t\t\t\t\t\t\t\tcoordIndex', '['] == row:
                    coord_lines_end =  num - 2
                    break
    fin.close()                
    boundary_lines.append(coord_lines_end)
    
    with open('isosurface.wrl', 'r') as fin:
        reader=csv.reader(fin,delimiter=' ') 
        
        coord_lines_end = 0
        for num, row in enumerate(reader):        
            if num > coord_lines_end:
                if ['\t\t\t\t\t\t\t\t\t\t\t\t\t\tcoordIndex', '['] == row:
                    index_lines_start =  num + 2
                    break
    fin.close()   
    boundary_lines.append(index_lines_start)      
    
    with open('isosurface.wrl', 'r') as fin:
        reader=csv.reader(fin,delimiter=' ') 
        
        coord_lines_end = 0
        for num, row in enumerate(reader):
            if num > index_lines_start:
                if ['\t\t\t\t\t\t\t\t\t\t\t\t\t\tnormal', 'Normal', '{'] == row:
                    index_lines_end =  num - 1
                    break

    fin.close()       
    boundary_lines.append(index_lines_end)  
    
    return boundary_lines

def convert_vrml_to_obj(boundary_lines, filename):
    
    coord_lines_start = boundary_lines[0]
    coord_lines_end = boundary_lines[1]
    index_lines_start = boundary_lines[2]
    index_lines_end = boundary_lines[3]
    
    coord_lines = np.arange(coord_lines_start,coord_lines_end+1)
    index_lines = np.arange(index_lines_start,index_lines_end+1)
    
    with open('isosurface.wrl', 'r') as fin:
        reader=csv.reader(fin,delimiter=' ')
        coords_strings=[row for i,row in enumerate(reader) if i+1 in coord_lines]
    fin.close()
    mesh_coords = []
    
    for x,c in enumerate(coords_strings):
            
        for j,ci in enumerate(c):
            if j == 0:
                ci = re.sub('\t+', '', ci)
                c[j] = ci
            c[j] = c[j].replace(",",".")
    
        current_coord_array = np.array([float(c[0]),float(c[1]),float(c[2])])
    
        mesh_coords.append(current_coord_array)
    
    mesh_coords = np.array(mesh_coords)
    
    with open('isosurface.txt', 'r') as fin:
        reader=csv.reader(fin,delimiter=' ')
        coords_strings=[row for i,row in enumerate(reader) if i+1 in index_lines]
    fin.close()
    
    indices = []
    
    for x,c in enumerate(coords_strings):
            
        for j,ci in enumerate(c):
            if j == 0:
                ci = re.sub('\t+', '', ci)
                c[j] = ci
            c[j] = c[j].replace(",",".")
    
        current_indices_array = np.array([int(c[0]),int(c[1]),int(c[2])])
    
        indices.append(current_indices_array)
    
    indices = np.array(indices)
    
    f = open(str(filename +'.obj'),'w')
    for i in range(len(mesh_coords)):
        f.write('v ' + str(mesh_coords[i,0]) + ' ' + str(mesh_coords[i,1]) + ' ' +str(mesh_coords[i,2]) + '\n')
    
    for i in range(len(indices)):
        f.write('f ' + str(indices[i,0]+1) + ' ' + str(indices[i,1]+1) + ' '+ str(indices[i,2]+1) + '\n')        
    f.close()
    return mesh_coords, indices
    
iso_strings = ['ISO0_ISO']
for i,is in enumerate(iso_strings):
    boundary_lines = []
    boundary_lines = get_boundary_lines(iso_strings[i])
    mesh_coords = []
    indices = []
    filename = iso_strings[i] + ' extracted_from_vrml'
    mesh_coords, indices = convert_vrml_to_obj(boundary_lines, filename)

# test case is isosurface.wrl with boundary lines to be [132148, 132459, 132463, 133082]
# and iso_string = 'ISO0_ISO'
