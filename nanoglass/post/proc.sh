#!/bin/sh

sed '1,4d' ../data/rdf_0GPa.rdf > tmp.rdf_0GPa
sed '1,4d' ../data/rdf_6GPa.rdf > tmp.rdf_6GPa
sed '1,4d' ../data/rdf_500K.rdf > tmp.rdf_500K

sed '1,9d' ../data/dump.voronoi_0GPa | awk '{print $7}' > tmp.voronoi_0GPa
sed '1,9d' ../data/dump.voronoi_6GPa | awk '{print $7}' > tmp.voronoi_6GPa
sed '1,9d' ../data/dump.voronoi_500K | awk '{print $7}' > tmp.voronoi_500K

chmod u+x plot_log.py post.py

./post.py
/usr/local/pizza-9Oct15/src/pizza.py -f plot_log.py #-q

