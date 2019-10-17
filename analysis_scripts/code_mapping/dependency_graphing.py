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
plt.ioff() # stops figures plotting automatically in the console - use plt.show() instead
import re
import os
import toposort
from networkx.drawing.nx_agraph import graphviz_layout


#%% create the regular expression library

module_pr  = re.compile("^\s*module\s+(\w+)",re.IGNORECASE|re.MULTILINE)
program_pr  = re.compile("^\s*program\s+(\w+)",re.IGNORECASE|re.MULTILINE)
use_mod_pr   = re.compile("^\s*use\s+(\w+)",re.IGNORECASE|re.MULTILINE)

fortran_pr = re.compile("\w+\.f90",re.IGNORECASE)




#%% list the fortran source files

process_directory = "/Users/mbessdl2/work/manchester/EMEP/emep-ctm/"

fortran_files = [f for f in os.listdir(process_directory) if os.path.isfile(process_directory+f) and fortran_pr.match(f)]


#%% build a list of modules, and use statements from said modules

chunk_dep_list = []
chunk_dep_dict = {}

for filename in fortran_files:
    with open(process_directory+filename) as file:
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
                chunk = chunk.casefold()
                re_string = '^\s*'+sect_name+'\s+'+chunk+'(.+)^\s*end\s*'+sect_name+'\s+'+chunk
                chunk_code_pr = re.compile(re_string,re.IGNORECASE|re.MULTILINE|re.DOTALL)
                chunk_code = chunk_code_pr.findall(code)
                if chunk_code:
                    use_modules = use_mod_pr.findall(chunk_code[0])
                    mod_set = set()
                    for mod in use_modules:
                        mod = mod.casefold()
                        #chunk_dep_list.append((mod,chunk))
                        chunk_dep_list.append((chunk,mod))
                        mod_set.add(mod)
                    chunk_dep_dict[chunk] = mod_set



#%% create the call graph, as a directional graph

call_graph = nx.DiGraph(chunk_dep_list)

chemspecs_list = ["chemspecs","chemspecs_adv_ml","chemspecs_shl_ml","chemspecs_tot_ml","chemchemicals_ml"]
sys_support_list = ["netcdf","netcdf_mod","mpi_groups_mod","checkstop_mod",\
                    "precision_mod","numberconstants","allocinits","mpi"]
extra_config_list = ["debug_module"]
io_support_list = ["io_progs_mod","io_nums_mod","io_mod"] # wrapped by io_mod
ops_support_list = ["smallutils_mod","timedate_mod","timedate_extrautil_mod",\
                    "keyvaluetypes","my_timing_mod","interpolationroutines_mod"]
fastj_support_list = ["fjx_init_mod","fjx_cmn_mod","fjx_sub_mod"] # used by fastj_mod
utilities_list = ["units_mod","country_mod","tabulations_mod"]
assim_support_list = ["da_mod","da_3dvar_mod"]
subdom_support_list = ["par_mod"]
output_support_list = ["sites_mod","trajectory_mod","outputchem_mod"]
input_support_list = ["readfield_mod"]
nesting_list = ["nest_mod","boundaryconditions_mod","externalbics_mod"] 
derived_types_list = ["owndatatypes_mod","my_derived_mod","derivedfields_mod"]
future_list = ["bidir_emep","bidir_module"]
domain_grid_list = ["gridallocate_mod","gridvalues_mod"]

meteorology_list = ["cellmet_mod","submet_mod","met_mod","blphysics_mod"]


data_arrays_list = ["localvariables_mod","emisdef_mod"]

deposition_list = ["rb_mod"]

met_support_list = ["metfields_mod","micromet_mod"]

genchem_list = ["chemdims_mod","chemgroups_mod","chemrates_mod","chemspecs_mod"]

emissions_list = ["emissions_mod","uemep_mod"]
emiss_anthro_list = ["emisget_mod","timefactors_mod"]
emissions_support_list = ["forestfire_mod","pointsource_mod","columnsource_mod","plumerise_mod"]



remove_list = chemspecs_list + sys_support_list + extra_config_list  \
                + io_support_list + ops_support_list + fastj_support_list \
                + utilities_list + assim_support_list + subdom_support_list \
                + output_support_list + input_support_list + nesting_list \
                + derived_types_list + future_list + domain_grid_list \
                + meteorology_list

call_graph.remove_nodes_from(remove_list)


#%% run some toposort analysis

# remove modules we don't want from the dependency dictionary
reduced_dep_dict = {}
for chunk in chunk_dep_dict.keys():
    if chunk not in remove_list:
        mod_set = set()
        for mod in chunk_dep_dict[chunk]:
            if mod not in remove_list:
                mod_set.add(mod)
        reduced_dep_dict[chunk] = mod_set
        


dependency_ladder = list(toposort.toposort(reduced_dep_dict))
dependency_ladder.reverse()

print(dependency_ladder[0])



#%% create diagram structure - this is a dictionary of the format:
#  key = 'module name'
#  value = tuple (X,Y) (where the values are positions in the diagram space)

use_custom_structures = True


if use_custom_structures:

    dep_layer_counts = []
    for layer in dependency_ladder:
       dep_layer_counts.append(len(layer)) 
    
    top = 800
    bottom = -800
    left = -400
    right = 400
    vert_gran = (top-bottom)/len(dep_layer_counts)
    
    pos = {}
    
    count_vert = 1
    for layer in dependency_ladder:
        vert_pos = top - vert_gran * count_vert
        horz_gran = (right-left)/(len(layer)+1)
        count_horz = 1
        for itm in layer:
            pos[itm] = ( right-(horz_gran*count_horz) , top-(vert_gran*count_vert)+(vert_gran/len(layer)*count_horz) )
            count_horz += 1
        count_vert += 1

else:
    
    pos = graphviz_layout(call_graph, prog='neato', root='emep_main')
    
    
    


#%% draw the data


nplot = plt.figure(figsize=(32, 64))
nx.draw(call_graph, pos, node_size=20, edge_color="grey", node_color="blue", \
        with_labels=True, font_size=16, font_weight='bold')
nplot.savefig("test.pdf",format="pdf")
