#!/usr/bin/env python3
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
metadata_filepaths=[str(Path(basedir,"GTDB-metadata",i)) for i in os.listdir(str(Path(basedir,"GTDB-metadata"))) if i.endswith("_taxonomy.tsv")] #metadata files used for taxonomic annotation


ranks=["superkingdom_name","phylum_name","class_name","order_name","family_name","genus_name","species_name"]   
diamond_output_columns=["qseqid", "sseqid","pident", "length", "mismatch", "gapopen" , "qstart","qend","sstart","send", "evalue","bitscore"]     #default diamond output collumns

#what percentage of top bitscore used for LCA

alg="lca" #lca (standard lca) or CAT or Fb_lca
topx_bitscore=0.9  #(0.9= top 10% bitscore, 0.8= top 20% of highest biscore allowed etc.)
cutoff_freq  =0.5  #fraction for bitscore lca (only used in CAT and Fb_lca)
taxa_freq    =5    #minimum taxa count

#%% modules

import numpy as np
import pandas as pd

#%% Functions



def read_to_gen(cdf): #GTDB
    sc=[] #dummy
    for ix,c in enumerate(cdf):


        print(ix)
        c=c.loc[:,["qseqid","sseqid","bitscore"]]
        c.loc[:,"sseqid"]=c.loc[:,"sseqid"].apply(lambda x: "_".join(x.split("_")[-3:])) 
        c=c.values
       
        if ix>0:
            c=np.vstack([sc[-1],c]) #add last group
       
        #find split inds based on protein index
        idx=np.unique(c[:,0],return_index=True)[1]
        idx.sort()
        sc=np.split(c,idx[1:])

        for group in sc[:-1]:              
            yield group
    yield sc[-1]

def LCA(group):

    for i in range(2,9):
        if len(np.unique(group[:,i]))!=1:
            i-=1
            break

    lca=group[0,2:i+1].tolist()
    return lca+[""]*(len(ranks)-len(lca)) #pad

def CAT_LCA(group,cutoff_freq=0.5):
    
    lca=[]

    sbit=group[:,1].sum()*cutoff_freq
    for i in range(2,9):
        
        
        val,gs=sum_by_group(group[:,1], group[:,i])
        m=val.argmax()
        if val[m]>sbit:
            lca.append(gs[m]) #append most frequent group in case of multiples 
        
        else:
            break
    return lca+[""]*(len(ranks)-len(lca)) #pad


def Fb_LCA(group,cutoff_freq=0.5):
    
    lca=[]

    
    for i in range(2,9):
    
        #Cat modification: nonzero only
        group=group[group[:,i]!=""]
        if not len(group):
            break
        
        #Cat modification, reassign sbit
        sbit=group[:,1].sum()*cutoff_freq
        
        val,gs=sum_by_group(group[:,1], group[:,i])
        m=val.argmax()
        if val[m]>sbit:
            lca.append(gs[m]) 
        else:
            break
        
        #Cat modification: Buildup LCA
        group=group[group[:,i]==gs[m]] 
        if not len(group):
            break
        
    return lca+[""]*(len(ranks)-len(lca)) #pad
        
def sum_by_group(values, groups):
    order = np.argsort(groups)
    groups = groups[order]
    values = values[order]
    values.cumsum(out=values)
    index = np.ones(len(groups), 'bool')
    index[:-1] = groups[1:] != groups[:-1]
    values = values[index]
    groups = groups[index]
    values[1:] = values[1:] - values[:-1]
    return values, groups


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


    d=[b[0,0]]+[str(b[0,2])]                     #node and bitscore  
    b=b[b[:,2]>=b[0,2]*topx_bitscore]            #top bitscore cutoff
    b=np.hstack([b,tdf.loc[b[:,1]].values])      #add GTDB taxonomy
    
    if len(b)>1:
        if alg=="lca":    r=    LCA(b)           #standard LCA
        if alg=="CAT":    r=CAT_LCA(b)           #CAT LCA
        if alg=="Fb_LCA": r= Fb_LCA(b)           #Focusing LCA
        blcas.append(d+r)
        
    elif len(b)==1: blcas.append(b[0,:]) 

df=pd.DataFrame(blcas,columns=["Node","bitscore"]+ranks)

#taxa_filtering
for rank in ranks:
    s=df.groupby(rank).size()
    df.loc[df[rank].isin(s[s<taxa_freq].index),rank]=""


#final write
df.to_tsv(output_filepath,sep="\t")












        
