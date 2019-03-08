# AdminExpress2RDF

Petit script de transformation en RDF/TTL de l'archive [AdminExpress](http://professionnels.ign.fr/adminexpress) de l'IGN la plus récente en utilisant les vocabulaires disponibles sur data.ign.fr. Une mise à jour du vocabulaire geofla intégrant les EPCI est proposée dans le dossier `vocabularies/`.

Lancement de la transformation via l'éxecution du script `adminExpress2RDF.py` à la racine du dossier.

Des sorties d'erreurs indiquent les éventuels éléments manquants ou erronés dans AdminExpress.

## Pré-requis

* Python 2+ 
* GDAL/OGR Python
* Nécessite l'installation préalable de la commande 7z. Pour une autre plateforme que GNU/Linux, il faut adapter la ligne de commande 7z présente dans `adminExpress2RDF.py`.

## Reste à faire

* Mettre à jour l'ontologie suite à la disparition des cantons
* Rajouter les chefs lieu de région et les centroides des régions

A noter : Pour assurer la compatibilité du jeu de donnée avec l'extension GeoSparql de GraphDB on utilise `<http://www.opengis.net/def/crs/OGC/1.3/CRS84>` en lieu et place de `<http://data.ign.fr/id/ignf/crs/WGS84GDD>` dans les chaines WKT.

## Utilisation dans GraphDB

* Installer GraphDB. Une facon simple est d'utiliser le projet suivant :  https://github.com/Ontotext-AD/graphdb-docker
* Créer un nouveau dépot dans GraphDB et y importer les jeux de données produits
* Activer le plugin Geosparql de GraphDB et indexer les données : http://graphdb.ontotext.com/documentation/standard/geosparql-support.html
* Exemple de requête fonctionnelle après import:

```
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX ign: <http://data.ign.fr/def/geometrie#>

SELECT *
WHERE {
    ?obj ign:geometry ?fGeom .
    ?fGeom geo:asWKT ?fWKT .
    FILTER (geof:sfContains(?fWKT,
            '''<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT(2 47)'''^^geo:wktLiteral))
}

```
