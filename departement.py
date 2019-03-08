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
    nom_dept = feature.GetField("NOM_DEP")
    insee_dept = feature.GetField("INSEE_DEP")
    ign_uri = ign_departement_data_uri.replace("$",insee_dept)
    insee_commune = chef_lieu.get_cl_dept_commune(insee_dept)

    output = ign_uri + ' a ' + ign_departement_data_type + ' ;\n'
    output += '\t' + 'owl:sameAs ' + insee_departement_data_uri.replace("$",insee_dept) + ' ;\n'
    output += '\t' + 'rdfs:label "' + nom_dept + '"@fr ;\n'
    output += '\t' + ign_geometry_predicate + ' ' + ign_multipolygon_dept_uri.replace("$",insee_dept) + ' ;\n'
    output += '\t' + ign_codedept_predicate + ' "' + insee_dept  + '" ;\n'
    
    if insee_commune is not None:
        output += '\t' + ign_cheflieu_predicate + ' ' + ign_commune_data_uri.replace("$",insee_commune) + ' ;\n'
        output += '\t' + ign_siegecheflieu_predicate + ' ' + ign_cheflieu_dept_uri.replace("$",insee_commune) + ' ;\n'
    else:
        print (" ! Missing chef lieu for departement " + str(insee_dept))
    
    output += '\t' + ign_region_predicate + ' ' + ign_region_data_uri.replace("$",insee_region)  + ' .\n'
    output += '\n'

    ttlfile.write(output)
        
def write_geometry(feature,ttlfile):

    insee_dept = feature.GetField("INSEE_DEP")
        
    polygon_uri = ign_multipolygon_dept_uri.replace("$",insee_dept)
    geom = feature.GetGeometryRef()
    geom.Transform(utils.get_transform(2154,4326))
    geom_string = '"' + crs84_uri + ' ' + geom.ExportToWkt() + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'
    
    # Write polygon
    output = polygon_uri + ' a ' + ign_multipolygon_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#centroid> ' + ign_centroid_dept_uri.replace("$",insee_dept) + ' .\n'
    output += '\n'

    # Write centroid
    centroid = geom.Centroid()
    wkt = 'POINT(' + str(centroid.GetX()) + ' ' + str(centroid.GetY()) + ')'
    geom_string = '"' + crs84_uri + ' ' + wkt + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

    output += ign_centroid_dept_uri.replace("$",insee_dept) + ' a ' + ign_point_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#coordX> "'+ str(centroid.GetX()) +'"^^xsd:double ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#coordY> "'+ str(centroid.GetY()) +'"^^xsd:double .\n'
    output += '\n'

    # Write chef lieu
    insee_commune = chef_lieu.get_cl_dept_commune(insee_dept)
    if insee_commune is not None:
        lon,lat,wkt = chef_lieu.get_cl_dept_coords_and_wkt(insee_commune)
        geom_string = '"' + crs84_uri + ' ' + wkt + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

        output += ign_cheflieu_dept_uri.replace("$",insee_commune) + ' a ' + ign_point_data_type + ' ;\n'
        output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
        output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
        output += '\t' + ' <http://data.ign.fr/def/geometrie#coordX> "'+ str(lon) + '"^^xsd:double ;\n'
        output += '\t' + ' <http://data.ign.fr/def/geometrie#coordY> "'+ str(lat) + '"^^xsd:double .\n'
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
