# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 14:38:10 2021

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


input_path = str(Path(basedir,"GTDB"))           #folder in which GTDB was downloaded
output_path= str(Path(basedir,"GTDB","renamed")) #folder which output is written to

#%% modules

import Bio
from Bio import SeqIO
   

#%% script

if not os.path.exists(output_path): os.mkdir(output_path)

files=[]
for d in ["bacteria","archaea"]:
    [       files.append(str(Path(input_path,"protein_faa_reps",d,i))) 
     for i in os.listdir(str(Path(input_path,"protein_faa_reps",d  )))]

for file in files:
    print(file)
    rs=[]
    for record in SeqIO.parse(file,format="fasta"):
        org=Path(file).stem.split("_protein")[0]
        record.id=record.id+"_"+org
        record.name=record.name+"_"+org
        rs.append(record)
    SeqIO.write(rs,
                str(Path(output_path,Path(file).stem+".fasta")),
                "fasta")
