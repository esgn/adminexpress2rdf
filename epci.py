#!/usr/bin/env python
# -*- coding: utf-8 -*-

from all_uris import *
from osgeo import ogr
import chef_lieu
import os
import sys
import utils

def get_statut_uri(type_epci):
    if type_epci=="CC":
        return ign_epci_cc
    elif type_epci=="CU":
        return ign_epci_cu
    elif type_epci=="CA":
        return ign_epci_cu
    elif type_epci=="METRO" or type_epci=="MET69":
        return ign_epci_metro

def write_attributes(feature,ttlfile):

    code_epci = feature.GetField("CODE_EPCI")
    nom_epci = feature.GetField("NOM_EPCI")
    type_epci = feature.GetField("TYPE_EPCI")
    ign_uri = ign_epci_data_uri.replace("$",str(code_epci))

    output = ign_uri + ' a ' + ign_epci_data_type + ' ;\n'
    output += '\t' + 'owl:sameAs ' + insee_epci_data_uri.replace("$",str(code_epci)) + ' ;\n'
    output += '\t' + 'rdfs:label "' + nom_epci + '"@fr ;\n'
    output += '\t' + ign_statut_predicate + ' '  + get_statut_uri(type_epci) + ' ;\n'
    output += '\t' + ign_codeepci_predicate + ' "'  + str(code_epci) + '" ;\n'
    output += '\t' + ign_geometry_predicate + ' ' + ign_multipolygon_epci_uri.replace("$",str(code_epci)) + ' .\n'
    output += '\n'

    ttlfile.write(output)

def write_geometry(feature,ttlfile):

    code_epci = feature.GetField("CODE_EPCI")
    polygon_uri = ign_multipolygon_epci_uri.replace("$",str(code_epci))

    geom = feature.GetGeometryRef()
    geom.Transform(utils.get_transform(2154,4326))
    geom_string = '"' + crs84_uri + ' ' + geom.ExportToWkt() + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

    # Write polygon
    output = polygon_uri + ' a ' + ign_multipolygon_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#centroid> ' + ign_centroid_epci_uri.replace("$",str(code_epci)) + ' .\n'
    output += '\n'

    # Write centroid
    centroid = geom.Centroid()
    wkt = 'POINT(' + str(centroid.GetX()) + ' ' + str(centroid.GetY()) + ')'
    geom_string = '"' + crs84_uri + ' ' + wkt + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

    output += ign_centroid_epci_uri.replace("$",str(code_epci)) + ' a ' + ign_point_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#coordX> "'+ str(centroid.GetX()) +'"^^xsd:double ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#coordY> "'+ str(centroid.GetY()) +'"^^xsd:double .\n'
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
