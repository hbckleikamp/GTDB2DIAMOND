# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 15:15:10 2021

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

input_filepath = "diamond_output.tsv" #placeholder filepath for input file  
output_filepath= "diamond_lca.tsv"    #placeholder filepath for output file

#diamond output columns (only "sseqid","qseqid","bitscore" are required for the script)
diamond_output_columns=["qseqid", "sseqid","pident", "length", "mismatch", "gapopen" , "qstart","qend","sstart","send", "evalue","bitscore"] #default diamond output collumns
#metadata files used for taxonomic annotation
metadata_filepaths=[str(Path(basedir,"GTDB-metadata",i)) for i in ["bac120_taxonomy.tsv","ar122_taxonomy.tsv"]]
#what percentage of top bitscore used for LCA
topx_bitscore=0.9 


#%% modules

import numpy as np
import pandas as pd

#%% Functions

ranks=["superkingdom_name","phylum_name","class_name","order_name","family_name","genus_name","species_name"]   

def read_to_gen(cdf):
    sc=[] #dummy
    for ix,c in enumerate(cdf):

        print(ix)
        c=c.reset_index()
        c=c.loc[:,["qeqid","sseqid","bitscore"]]
        c.loc[:,"sseqid"]=c.loc[:,"sseqid"].apply(lambda x: "_".join(x.split("_")[-3:])) #split off taxa information in header 
        c=c.values
        
        if ix>0:
            c=np.vstack([sc[-1],c]) #add last group
        
        #find split inds based on protein index
        ix=np.unique(cdf["qseqid"].to_numpy(),return_index=True)[1]
        ix.sort()
        sc=np.split(c,ix)
        
        
        for group in sc[:-1]:            
            
            yield group
    yield sc[-1]


#%% Script

#make taxonomy dataframe
tdf=pd.concat([pd.read_csv(f,sep="\t",header=None,names=["Accession","taxonomy"]) for f in metadata_filepaths]).set_index("Accession")
tdf[ranks]=tdf["taxonomy"].str.rsplit(";",expand=True)
tdf=tdf[ranks]

# batched filedreading
names=diamond_output_columns
cdf=pd.read_csv(input_filepath, sep='\t', names=names,  lineterminator='\n', chunksize=3000000) 
groups=read_to_gen(cdf)


#best bitscore lca
blcas=[] 
for ix,b in enumerate(groups):

    lin=tdf.loc[b[:,1]] #GTDB
    d=[b[0,0]]+[str(b[0,2])] #node and bitscore
    blca=[]
    if len(lin)>1:
        lin=pd.DataFrame(lin,columns=ranks)
        blin=lin[b[:,2]>=b[0,2]*topx_bitscore] #top bitscore cutoff
        ix=0
        for r in ranks:
            if blin[r].nunique()!=1:
                break
            else:
                ix+=1
        blca=blin.iloc[0,0:ix].tolist()
        blcas.append(d+blca+[""]*(len(ranks)-len(blca))) 
    elif len(lin)==1:
        blca= d+lin.iloc[0].tolist()+[""]*(len(ranks)-len(blca)) #pad
        blcas.append(blca) 
    
    #final writes
    with open(output_filepath, 'a+') as protein:
        if len(blcas):
            protein.writelines("\n".join(['\t'.join(i) for i in blcas])+"\n") #write proteins










