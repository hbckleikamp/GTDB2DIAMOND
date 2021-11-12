# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 14:31:53 2021

@author: hbckleikamp
"""
#%% change directory to script directory (should work on windows and mac)
import os
from pathlib import Path
from inspect import getsourcefile
os.chdir(str(Path(os.path.abspath(getsourcefile(lambda:0))).parents[0]))
script_dir=os.getcwd()
print(os.getcwd())

basedir=os.getcwd()

#%% parameters


input_path = str(Path(basedir,"GTDB","renamed"))     #folder in which GTDB files are located
output_path= str(Path(basedir,"GTDB","GTDB_merged")) #folder which output is written to
output_file= "GTDB_merged.fasta"                     #filename of merged database


#%% modules

import shutil



#%% functions
def merge(outpath,files):
    with open(outpath,'wb') as wfd:
        for f in files:
            print(f)
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, wfd)
    return

#%% script

if not os.path.exists(output_path): os.mkdir(output_path)
files=[]
[files.append(str(Path(input_path,i))) for i in os.listdir(input_path)]
merge(str(Path(output_path,output_file)),files)
