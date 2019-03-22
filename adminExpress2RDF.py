#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Emmanuel Séguin"

from ftplib import FTP
import os
import sys
import shutil
from os import listdir
from osgeo import ogr
import chef_lieu
import commune
import epci
import arrondissement_departemental
import departement
import region

# CLEANUP
for f in listdir('.'):
    if f.lower().endswith('.ttl'):
        os.remove(f)

# ADMINEXPRESS FTP PARAMETERS
host = 'ftp3.ign.fr'
user = 'Admin_Express_ext'
password = 'Dahnoh0eigheeFok'

# GET LATEST ADMINEXPRESS FILE
dirlist = []
ftp = FTP(host)
ftp.login(user,password)
ftp.dir('-t',dirlist.append) # '-t' supported by this FTP but not standard
# Check filename
i=0
for item in list(dirlist):
    if "ADMIN-EXPRESS" not in item:
        del dirlist[i]
    i+=1
filename = dirlist[0].split(" ")[-1]
size = int(dirlist[0].split(" ")[-5])
# If file has already been downloaded
if os.path.isfile(filename) and os.stat(filename).st_size == size:
    pass
else:
    print("> Downloading newest AdminExpress archive from FTP ("+filename+")")
    ftp.retrbinary("RETR " + filename, open(filename,"wb").write)

# UNZIP FILE
dirname = filename.split(".")[0]
if os.path.isdir(dirname): shutil.rmtree(dirname) # delete before extraction
print("> Extracting data from AdminExpress archive")
os.system("7z x " + filename + " > /dev/null") # dirty but simpliest way to extract 7z

# GET LIST OF SHAPEFILES IN FOLDERS
shplist = []
for dirpath, dirnames, files in os.walk(dirname):
    for name in files:
        if name.lower().endswith(".shp"):
            shplist.append(os.path.join(dirpath,name))

# DEAL WITH CHEF LIEU FIRST
print("> Loading chefs lieu")
for path in shplist:
    name = os.path.splitext(os.path.basename(path))[0].lower()
    if name == "chef_lieu":
        module = __import__(name)
        method = getattr(module, "load_chef_lieu")
        status = method(path)

# DEAL WITH REMAINING SHAPEFILES
print("> Shapefiles to TTL transformation")
for path in shplist:
    name = os.path.splitext(os.path.basename(path))[0].lower()
    if name!="chef_lieu":
        module = __import__(name)
        method = getattr(module, 'tottl')
        status = method(path)

# FINAL CLEANUP
shutil.rmtree(dirname)
