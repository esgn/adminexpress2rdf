#!/usr/bin/env python
# -*- coding: utf-8 -*-

from all_uris import *
from osgeo import ogr
import chef_lieu
import os
import sys
import utils

def write_attributes(feature,ttlfile):

    insee_region = feature.GetField("INSEE_REG")
    nom_region = feature.GetField("NOM_REG")

    ign_uri = ign_region_data_uri.replace("$",insee_region)
    
    output = ign_uri + ' a ' + ign_region_data_type + ' ;\n'
    output += '\t' + 'owl:sameAs ' + insee_region_data_uri.replace("$",insee_region) +  ' ;\n'
    output += '\t' + 'rdfs:label "' + nom_region +  '"@fr ;\n'
    output += '\t' + ign_geometry_predicate + ' ' + ign_multipolygon_region_uri.replace("$",insee_region) +  ' ;\n'
    output += '\t' + ign_coderegion_predicate + ' "' + insee_region  +  '" .\n'
    output += '\n'

    ttlfile.write(output)
        
def write_geometry(feature,ttlfile):

    insee_region = feature.GetField("INSEE_REG")
    polygon_uri = ign_multipolygon_region_uri.replace("$",insee_region)
    
    geom = feature.GetGeometryRef()
    geom.Transform(utils.get_transform(2154,4326))
    geom_string = '"' + crs84_uri + ' ' + geom.ExportToWkt() + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

    output = polygon_uri + ' a ' + ign_multipolygon_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' .\n'
    output += '\n'

    ttlfile.write(output)

def tottl(path):
    ttlfile = utils.init_ttl_file(__name__)
    shpfile = ogr.Open(path)
    layer = shpfile.GetLayer()
    for feature in layer:
        write_attributes(feature,ttlfile)
        write_geometry(feature,ttlfile)
    ttlfile.close()
