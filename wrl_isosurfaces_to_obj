#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:21:42 2016
@author: lukas
"""
import numpy as np
import csv
import re

def get_boundary_lines(iso_string, filename):
    
    boundary_lines = []
    
    # reading multiple times the same file csv reader
    # http://stackoverflow.com/questions/11150155/why-cant-i-repeat-the-for-loop-for-csv-reader-python

    with open(filename, 'r') as fin:
        reader=csv.reader(fin,delimiter=' ')         
        
        coords_offset = 17 # lines
        for num, row in enumerate(reader):
            # find the beginning of the isosurface mesh entry
            if iso_string in row:
                coord_lines_start =  num + 1 + coords_offset
                break
        boundary_lines.append(coord_lines_start)
        #jumps to the start of the file again
        fin.seek(0)
        
        for num, row in enumerate(reader):        
            if num > coord_lines_start:
                if ['\t\t\t\t\t\t\t\t\t\t\t\t\t\tcoordIndex', '['] == row:
                    coord_lines_end =  num - 2
                    break
        boundary_lines.append(coord_lines_end)
        #jumps to the start of the file again
        fin.seek(0)
    
        coord_lines_end = 0
        for num, row in enumerate(reader):        
            if num > coord_lines_end:
                if ['\t\t\t\t\t\t\t\t\t\t\t\t\t\tcoordIndex', '['] == row:
                    index_lines_start =  num + 2
                    break 
        boundary_lines.append(index_lines_start)      
        #jumps to the start of the file again
        fin.seek(0)
        
        coord_lines_end = 0
        for num, row in enumerate(reader):
            if num > index_lines_start:
                if ['\t\t\t\t\t\t\t\t\t\t\t\t\t\tnormal', 'Normal', '{'] == row:
                    index_lines_end =  num - 1
                    break
        boundary_lines.append(index_lines_end)  
        #jumps to the start of the file again
        fin.seek(0)
    
    fin.close()    
    
    return boundary_lines

def convert_vrml_to_obj(boundary_lines, filename):
    
    coord_lines_start = boundary_lines[0]
    coord_lines_end = boundary_lines[1]
    index_lines_start = boundary_lines[2]
    index_lines_end = boundary_lines[3]
    
    coord_lines = np.arange(coord_lines_start,coord_lines_end+1)
    index_lines = np.arange(index_lines_start,index_lines_end+1)
    
    with open(filename, 'r') as fin:
        reader=csv.reader(fin,delimiter=' ')
        coords_strings=[row for i,row in enumerate(reader) if i+1 in coord_lines]
    
        #jumps to the start of the file again
        fin.seek(0)        
        
        index_strings=[row for i,row in enumerate(reader) if i+1 in index_lines]
        
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
    indices = []
    
    for x,c in enumerate(index_strings):
            
        for j,ci in enumerate(c):
            if j == 0:
                ci = re.sub('\t+', '', ci)
                c[j] = ci
            c[j] = c[j].replace(",",".")
    
        current_indices_array = np.array([int(c[0]),int(c[1]),int(c[2])])
    
        indices.append(current_indices_array)
    
    indices = np.array(indices)

    return mesh_coords, indices
    
def write_obj_file(out_filename, mesh_coords, indices):
    f = open(str(out_filename +'.obj'),'w')
    for i in range(len(mesh_coords)):
        f.write('v ' + str(mesh_coords[i,0]) + ' ' + str(mesh_coords[i,1]) + ' ' +str(mesh_coords[i,2]) + '\n')

    for i in range(len(indices)):
        f.write('f ' + str(indices[i,0]+1) + ' ' + str(indices[i,1]+1) + ' '+ str(indices[i,2]+1) + '\n')        
    f.close()
    
# main    
    
wrl_filename = 'isosurface.wrl'
iso_strings = ['ISO0_ISO']
for i,iso_string in enumerate(iso_strings):
    boundary_lines = []
    boundary_lines = get_boundary_lines(iso_strings[i], wrl_filename)
    
    mesh_coords = []
    indices = []
    mesh_coords, indices = convert_vrml_to_obj(boundary_lines, wrl_filename)    
    
    out_filename = iso_string + ' extracted_from_vrml'
    write_obj_file(out_filename, mesh_coords, indices)

# test case is isosurface.wrl with boundary lines to be [132148, 132459, 132463, 133082]
# and iso_string = 'ISO0_ISO'
