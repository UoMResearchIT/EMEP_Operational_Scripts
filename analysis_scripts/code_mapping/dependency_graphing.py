#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:05:01 2019

Dependency graphing for EMEP.

@author: mbessdl2
"""

#%matplotlib auto

#%%

import networkx as nx
import matplotlib.pyplot as plt
import re
import os


#%% create the regular expression library

module_pr  = re.compile("^\s*module\s+(\w+)",re.IGNORECASE|re.MULTILINE)
program_pr  = re.compile("^\s*program\s+(\w+)",re.IGNORECASE|re.MULTILINE)
use_mod_pr   = re.compile("^\s*use\s+(\w+)",re.IGNORECASE|re.MULTILINE)

fortran_pr = re.compile("\w+\.f90",re.IGNORECASE)




#%% list the fortran source files

process_directory = "."

fortran_files = [f for f in os.listdir(process_directory) if os.path.isfile(f) and fortran_pr.match(f)]


#%% build a list of modules, and use statements from said modules

chunk_dep_list = []

for filename in fortran_files:
    with open(filename) as file:
        code = file.read()
        
        prog_name = program_pr.findall(code)
        module_name = module_pr.findall(code)
 
        if prog_name:
            chunk_name= prog_name
            sect_name = 'program'
        elif module_name:
            chunk_name = module_name
            sect_name = 'module'

        for chunk in chunk_name:
            if chunk != 'procedure':
                re_string = '^\s*'+sect_name+'\s+'+chunk+'(.+)^\s*end\s+'+sect_name+'\s+'+chunk
                chunk_code_pr = re.compile(re_string,re.IGNORECASE|re.MULTILINE|re.DOTALL)
                chunk_code = chunk_code_pr.findall(code)
                if chunk_code:
                    use_modules = use_mod_pr.findall(chunk_code[0])
                    for mod in use_modules: 
                        #chunk_dep_list.append((mod,chunk))
                        chunk_dep_list.append((chunk,mod))
                    


#%% create the call graph, as a directional graph

call_graph = nx.DiGraph(chunk_dep_list)

#%% draw the data

#nx.draw(call_graph)

from networkx.drawing.nx_agraph import graphviz_layout
G = nx.Graph(chunk_dep_list)
pos = graphviz_layout(G, prog='twopi', root='emep_Main', args='')
plt.figure(figsize=(64, 64))
#plt.figure(figsize=(8, 8))
nx.draw(G, pos, node_size=20, edge_color="grey", node_color="blue", with_labels=True, font_size=16, font_weight='bold')
plt.axis('equal')
plt.show()

