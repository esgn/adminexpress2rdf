#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr
import utils
import os

os.environ['SHAPE_ENCODING'] = "utf-8"

# Data structure
chefs_lieu_commune = {}
chefs_lieu_arrdt = {}
chefs_lieu_dept = {}
chefs_lieu_region = {}
chefs_lieu_capitale = {}

def get_cl_coords_and_wkt(insee_commune, chef_lieu_dict):
    geom = chef_lieu_dict.get(insee_commune).split('|')
    wkt = 'POINT('+geom[0]+' '+geom[1]+')'
    return geom[0], geom[1], wkt

def get_cl_commune(insee_dept, chef_lieu_dict):
    for key, value in chef_lieu_dict.items():
        if key.startswith(insee_dept):
            return key

def check_cl_commune_exists(insee_commune):
    if insee_commune in chefs_lieu_commune: 
        return True
    return False

def get_cl_commune_coords_and_wkt(insee_commune):
    return get_cl_coords_and_wkt(insee_commune, chefs_lieu_commune)

def get_cl_arrdt_coords_and_wkt(insee_commune):
    return get_cl_coords_and_wkt(insee_commune, chefs_lieu_arrdt)

def get_cl_dept_coords_and_wkt(insee_commune):
    return get_cl_coords_and_wkt(insee_commune, chefs_lieu_dept)

def get_cl_arrdt_commune(insee_dept):
    return get_cl_commune(insee_dept,chefs_lieu_arrdt)

def get_cl_dept_commune(insee_dept):
    return get_cl_commune(insee_dept,chefs_lieu_dept)
    
def store_chef_lieu(feature):
    statut_chef_lieu = feature.GetFieldAsString("STATUT")
    insee_commune = feature.GetFieldAsString("INSEE_COM")
    geom = feature.GetGeometryRef()
    geom.Transform(utils.get_transform(2154,4326))
    geom_string = str(geom.GetX())+'|'+str(geom.GetY())
    if statut_chef_lieu == "Commune simple":
        chefs_lieu_commune.update({insee_commune:geom_string})
    elif statut_chef_lieu == "Arrondissement municipal":
        chefs_lieu_commune.update({insee_commune:geom_string})
    elif statut_chef_lieu == "Sous-préfecture":
        chefs_lieu_arrdt.update({insee_commune:geom_string})
        chefs_lieu_commune.update({insee_commune:geom_string})
    elif statut_chef_lieu == "Préfecture":
        chefs_lieu_dept.update({insee_commune:geom_string})
        chefs_lieu_commune.update({insee_commune:geom_string})
    elif statut_chef_lieu == "Préfecture de région":
        chefs_lieu_region.update({insee_commune:geom_string})
        chefs_lieu_dept.update({insee_commune:geom_string})
        chefs_lieu_commune.update({insee_commune:geom_string})
    elif statut_chef_lieu == "Capitale d'état":
        chefs_lieu_capitale.update({insee_commune:geom_string})
        chefs_lieu_arrdt.update({insee_commune:geom_string})
        chefs_lieu_dept.update({insee_commune:geom_string})
        chefs_lieu_commune.update({insee_commune:geom_string})
        
def load_chef_lieu(path):
    shpfile = ogr.Open(path)
    layer = shpfile.GetLayer()
    for feature in layer:
        store_chef_lieu(feature)
