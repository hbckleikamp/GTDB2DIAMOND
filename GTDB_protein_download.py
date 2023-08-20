#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 12:47:42 2023

@author: hugokleikamp
"""

#%% change directory to script directory (should work on windows and mac)
import os
from pathlib import Path
from inspect import getsourcefile
os.chdir(str(Path(os.path.abspath(getsourcefile(lambda:0))).parents[0]))
script_dir=os.getcwd()
print(os.getcwd())

basedir=os.getcwd()

#%% modules
import urllib.request, gzip, zipfile, shutil, tarfile, requests, re, time
from tqdm import tqdm 

#%% parameters

#url for GTDB protein representative database
db_url="https://data.gtdb.ecogenomic.org/releases/latest/genomic_files_reps/gtdb_proteins_aa_reps.tar.gz" 
db_path=str(Path(basedir,"GTDB"))

#url for metadata for GTDB taxonomy
url="https://data.gtdb.ecogenomic.org/releases/latest/"
meta_path=str(Path(basedir,"GTDB-Metadata"))

gtdb_files=requests.get(url).text
meta_urls=[url+i for i in re.split('<|>',gtdb_files) if i.endswith("taxonomy.tsv.gz")]


#%% Functions
def download_with_progress(url, filename):
    def show_progress(block_num, block_size, total_size):
        pbar.update(block_size)  # Increment the progress bar by block_size bytes

    with tqdm(total=0, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        urllib.request.urlretrieve(url, filename, show_progress)


def download(urls,path):
    
    if type(urls)==str:
        urls=[urls]
    
    for url in urls:
        print(url)
        
        if not os.path.exists(path): os.makedirs(path)
        filename  = str(Path(path,url.split("/")[-1]))
    
        
        #download
        if not os.path.exists(filename): #check if file is already downloaded
            c=0

        
            while True:
                try:
                    download_with_progress(url, filename)
                    break
                except Exception as e:
                    print("Error:", e)
                    c+=1
                    time.sleep(2)
                    print("retry")
                    if c>5: #max of 5 retries
                        break
        
        
        
        return filename
        
        

def extract(path): #path to folder

    #recursive extraction            
    while any([f.endswith((".zip",".gz",".tar")) for f in os.listdir(path)]):
        
        for f in os.listdir(path):
            
            i=str(Path(path,Path(f)))
            o=str(Path(path,Path(f).stem))
            
            if f[0].isalnum() and f.endswith(".zip"):
                print("extracting "+f)
                with zipfile.ZipFile(i, 'r') as zip_ref:
                    zip_ref.extractall(path)
                if os.path.exists(i): os.remove(i)

            if f[0].isalnum() and f.endswith(".gz"):
                print("extracting "+f)
                with gzip.open(i,'rb') as f_in:
                    with open(o,'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                if os.path.exists(i): os.remove(i)
                
            if f[0].isalnum() and f.endswith(".tar"):
                print("extracting "+f)
                tar = tarfile.open(i, "r:")
                tar.extractall(path)
                tar.close()
                if os.path.exists(i): os.remove(i)
                    
        
def extract_subfolders(folder):

    for subdir, dirs, files in os.walk(folder):
        for d in dirs:
            if os.path.isdir(d):
                extract(d)

        if os.path.isdir(subdir):
            extract(subdir)

def download_extract(urls,path):
    
    download(urls,path)
    extract_subfolders(path)




#%% Script
download_extract(db_url,db_path)
download_extract(meta_urls,meta_path)
