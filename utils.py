#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr
from osgeo import osr
import os

transform = 0

def get_transform(source_srs, target_srs):
    source = osr.SpatialReference()
    source.ImportFromEPSG(source_srs)
    target = osr.SpatialReference()
    target.ImportFromEPSG(target_srs)
    global transform
    if transform == 0:
        transform = osr.CoordinateTransformation(source, target)
    return transform

def init_ttl_file(name):
    filename = name + ".ttl"
    if os.path.isfile(filename):
        return open(filename, "a")
    else:
        f = open(filename, "a")
        f.write("@prefix wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n")
        f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
        f.write("@prefix gn: <http://www.geonames.org/ontology#> .\n")
        f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        f.write("\n")
        return f
