#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Data Types
ign_commune_data_type = "<http://data.ign.fr/def/geofla#Commune>"
ign_arrondissement_data_type = "<http://data.ign.fr/def/geofla#Arrondissement> "
ign_departement_data_type = "<http://data.ign.fr/def/geofla#Departement>"
ign_region_data_type = "<http://data.ign.fr/def/geofla#Region>"
ign_multipolygon_data_type = "<http://data.ign.fr/def/geometrie#MultiPolygon>"
ign_point_data_type = "<http://data.ign.fr/def/geometrie#Point>"
    # 2019 UPDATE
ign_epci_data_type = "<http://data.ign.fr/def/geofla#Epci>"

# URI model
ign_commune_data_uri = "<http://data.ign.fr/id/geofla/commune/$>"
ign_region_data_uri = "<http://data.ign.fr/id/geofla/region/$>"
ign_departement_data_uri = "<http://data.ign.fr/id/geofla/departement/$>"
ign_arrondissement_data_uri = "<http://data.ign.fr/id/geofla/arrondissement/$>"

ign_multipolygon_commune_uri = "<http://data.ign.fr/id/geofla/commune/Multipolygon_$>"
ign_centroid_commune_uri = "<http://data.ign.fr/id/geofla/commune/PointCtr_$>"
ign_cheflieu_commune_uri = "<http://data.ign.fr/id/geofla/commune/PointChf_$>"

ign_multipolygon_arrondissement_uri = "<http://data.ign.fr/id/geofla/arrondissement/Multipolygon_$>"
ign_centroid_arrondissement_uri = "<http://data.ign.fr/id/geofla/departement/PointCtr_$>"
ign_cheflieu_arrondissement_uri = "<http://data.ign.fr/id/geofla/departement/PointChf_$>"


ign_multipolygon_dept_uri = "<http://data.ign.fr/id/geofla/departement/Multipolygon_$>"
ign_centroid_dept_uri = "<http://data.ign.fr/id/geofla/departement/PointCtr_$>"
ign_cheflieu_dept_uri = "<http://data.ign.fr/id/geofla/departement/PointChf_$>"

ign_multipolygon_region_uri = "<http://data.ign.fr/id/geofla/region/Multipolygon_$>"

insee_commune_data_uri = "<http://id.insee.fr/geo/commune/$>"
insee_arrondissement_data_uri = "<http://id.insee.fr/geo/arrondissement/$>"
insee_departement_data_uri = "<http://id.insee.fr/geo/departement/$>"
insee_region_data_uri = "<http://id.insee.fr/geo/region/$>"
insee_epci_data_uri = "<http://id.insee.fr/geo/epci/$>"

    # 2019 UPDATE
ign_epci_data_uri = "<http://data.ign.fr/id/geofla/epci/$>"
ign_centroid_epci_uri = "<http://data.ign.fr/id/geofla/epci/PointCtr_$>"
ign_multipolygon_epci_uri = "<http://data.ign.fr/id/geofla/commune/Multipolygon_$>"

# Predicates
ign_geometry_predicate = "<http://data.ign.fr/def/geometrie#geometry>"
ign_insee_predicate = "<http://data.ign.fr/def/geofla#numInsee>"
ign_statut_predicate = "<http://data.ign.fr/def/geofla#statut>"
ign_superficie_predicate = "<http://data.ign.fr/def/geofla#superficieHa>"
ign_population_predicate = "<http://data.ign.fr/def/geofla#population>"
ign_codecommune_predicate = "<http://data.ign.fr/def/geofla#codeComm>"
ign_cheflieu_predicate = "<http://data.ign.fr/def/geofla#chefLieu>"
ign_siegecheflieu_predicate = "<http://data.ign.fr/def/geofla#siegeDuChefLieu>"
ign_arrondissement_predicate  = "<http://data.ign.fr/def/geofla#arr>"
ign_codearrdt_predicate = "<http://data.ign.fr/def/geofla#codeArr>"
ign_departement_predicate = "<http://data.ign.fr/def/geofla#dpt>"
ign_codedept_predicate = "<http://data.ign.fr/def/geofla#codeDpt>"
ign_coderegion_predicate = "<http://data.ign.fr/def/geofla#codeReg>"
ign_region_predicate = "<http://data.ign.fr/def/geofla#region>"

    # 2019 UPDATE
ign_epci_predicate = "<http://data.ign.fr/def/geofla#epci>"
ign_codeepci_predicate = "<http://data.ign.fr/def/geofla#codeEpci>"

# Typenames
ign_epci_cc="<http://data.ign.fr/id/codes/geofla/typeepci/CommunauteCommunes>"
ign_epci_cu="<http://data.ign.fr/id/codes/geofla/typeepci/CommunauteUrbaine>"
ign_epci_ca="<http://data.ign.fr/id/codes/geofla/typeepci/CommunauteDAgglomerations>"
ign_epci_metro="<http://data.ign.fr/id/codes/geofla/typeepci/Metropole>"
ign_commune_simple="<http://data.ign.fr/id/codes/geofla/typedecommune/CommuneSimple>"
ign_commune_sous_prefecture="<http://data.ign.fr/id/codes/geofla/typedecommune/SousPrefecture>"
ign_commune_prefecture_region="<http://data.ign.fr/id/codes/geofla/typedecommune/PrefectureDeRegion>"
ign_commune_capitale="<http://data.ign.fr/id/codes/geofla/typedecommune/CapitaleDEtat>"
ign_commune_prefecture_departement="<http://data.ign.fr/id/codes/geofla/typedecommune/PrefectureDeDepartement>"

# CRS
# Original URI for WGS84 in IGN vocabulary
ign_wgs84_uri = "<http://data.ign.fr/id/ignf/crs/WGS84GDD>"
# Necessary for GraphDB : https://stackoverflow.com/questions/49732420/graphdb-geosparql
crs84_uri = "<http://www.opengis.net/def/crs/OGC/1.3/CRS84>"
