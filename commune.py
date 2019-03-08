#!/usr/bin/env python
# -*- coding: utf-8 -*-

from all_uris import *
from osgeo import ogr
import chef_lieu
import os
import sys
import utils

def get_statut_uri(statut):
    statut = statut.lower()
    if "simple" in statut:
        return ign_commune_simple
    if "sous" in statut:
        return ign_commune_sous_prefecture
    if "région" in statut:
        return ign_commune_prefecture_region
    if "capitale" in statut:
        return ign_commune_capitale
    if "préfecture" in statut:
        return ign_commune_prefecture_departement
    if "arrondissement" in statut:
        return ign_commune_simple

def write_attributes(feature,ttlfile):

    statut_commune = feature.GetField("STATUT")
    nom_commune = feature.GetField("NOM_COM_M")
    insee_commune = feature.GetField("INSEE_COM")
    nom_region = feature.GetField("NOM_REG")
    insee_region = feature.GetField("INSEE_REG")
    nom_dept = feature.GetField("NOM_DEP")
    insee_dept = feature.GetField("INSEE_DEP")
    insee_arr = feature.GetField("INSEE_ARR")
    code_epci = feature.GetField("CODE_EPCI")
    population_commune = float(int(feature.GetField("POPULATION"))/1000.0)
    geom = feature.GetGeometryRef()
    superficie_commune_ha = int(geom.GetArea()/10000)
    ign_uri = ign_commune_data_uri.replace("$",insee_commune)
    
    output = ign_uri + ' a ' + ign_commune_data_type + ' ;\n'
    output += '\t' + 'owl:sameAs ' + insee_commune_data_uri.replace("$",insee_commune) + ' ;\n'
    output += '\t' + 'rdfs:label "' + nom_commune + '"@fr ;\n'
    output += '\t' + ign_geometry_predicate + ' ' + ign_multipolygon_commune_uri.replace("$",insee_commune) + ' ;\n'
    output += '\t' + ign_insee_predicate + ' "'  + str(insee_commune) + '" ;\n'
    output += '\t' + ign_codecommune_predicate + ' "'  + str(insee_commune)[-3:] + '" ;\n'
    
    if statut_commune is not None: # Should never happen but actually does
        output += '\t' + ign_statut_predicate + ' '  + get_statut_uri(statut_commune) + ' ;\n'
    else:
        print (" ! Missing status for commune " + str(insee_commune) + " ("+nom_commune + ")")
        
    output += '\t' + ign_superficie_predicate + ' "'  + str(superficie_commune_ha) + '"^^xsd:integer ;\n'
    output += '\t' + ign_population_predicate + ' "' + str(population_commune) + '"^^xsd:double ;\n'
    output += '\t' + ign_region_predicate + ' '  + ign_region_data_uri.replace("$",insee_region) +' ;\n'
    output += '\t' + ign_departement_predicate + ' '  + ign_departement_data_uri.replace("$",insee_dept) + ' ;\n'
    output += '\t' + ign_epci_predicate + ' '  + ign_epci_data_uri.replace("$",str(code_epci)) + ' ;\n'
    
    if chef_lieu.check_cl_commune_exists(insee_commune):
        output += '\t' + ign_siegecheflieu_predicate + ' '  + ign_cheflieu_commune_uri.replace("$",insee_commune) + ' ;\n'
    else:
        print (" ! Missing chef lieu for commune " + str(insee_commune) + " ("+nom_commune + ")")
        
    if insee_dept != '976': # Mayotte has no arrondissement
        code_arr = insee_commune[2:] + str(insee_arr)
        output += '\t' + ign_arrondissement_predicate + ' '  + ign_arrondissement_data_uri.replace("$",code_arr) + ' .\n'
    output += '\n'

    ttlfile.write(output)

def write_geometry(feature,ttlfile):

    insee_commune = feature.GetField("INSEE_COM")

    # Write Multipolygon
    geom = feature.GetGeometryRef()
    geom.Transform(utils.get_transform(2154,4326))
    geom_string = '"' + crs84_uri + ' ' + geom.ExportToWkt() + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'
    polygon_uri = ign_multipolygon_commune_uri.replace("$",insee_commune)

    output = polygon_uri + ' a ' + ign_multipolygon_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#centroid> ' + ign_centroid_commune_uri.replace("$",insee_commune) + ' .\n'
    output += '\n'

    # Write Centroid
    centroid = geom.Centroid()
    wkt = 'POINT(' + str(centroid.GetX()) + ' ' + str(centroid.GetY()) + ')'
    geom_string = '"' + crs84_uri + ' ' + wkt + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

    output += ign_centroid_commune_uri.replace("$",insee_commune) + ' a ' + ign_point_data_type + ' ;\n'
    output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#coordX> "'+ str(centroid.GetX()) +'"^^xsd:double ;\n'
    output += '\t' + ' <http://data.ign.fr/def/geometrie#coordY> "'+ str(centroid.GetY()) +'"^^xsd:double .\n'
    output += '\n'

    # Write Chef lieu
    if chef_lieu.check_cl_commune_exists(insee_commune):
        lon,lat,wkt = chef_lieu.get_cl_commune_coords_and_wkt(insee_commune)
        chef_lieu_uri = ign_cheflieu_commune_uri.replace("$",insee_commune)
        geom_string = '"' + crs84_uri + ' ' + wkt + '"^^<http://www.opengis.net/ont/geosparql#wktLiteral>'

        output += chef_lieu_uri + ' a ' + ign_point_data_type + ' ;\n'
        output += '\t' + ' <http://www.opengis.net/ont/geosparql#asWKT> ' + geom_string + ' ;\n'
        output += '\t' + ' <http://data.ign.fr/def/geometrie#crs> ' + '<http://data.ign.fr/id/ignf/crs/WGS84GDD>' + ' ;\n'
        output += '\t' + ' <http://data.ign.fr/def/geometrie#coordX> "'+ lon +'"^^xsd:double ;\n'
        output += '\t' + ' <http://data.ign.fr/def/geometrie#coordY> "'+ lat +'"^^xsd:double .\n'
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
