!/bin/sh

echo "Change file name according to size of system!"

sed '1,4d' ../data/rdf_0GPa_6nm.rdf > tmp.rdf_0GPa
sed '1,4d' ../data/rdf_6GPa_6nm.rdf > tmp.rdf_6GPa
sed '1,4d' ../data/rdf_500K_6nm.rdf > tmp.rdf_500K
#sed '1,4d' ../data/rdf_50K_6nm.rdf > tmp.rdf_50K

sed '1,9d' ../data/dump.voronoi_0GPa_6nm | awk '{print $7}' > tmp.voronoi_0GPa
sed '1,9d' ../data/dump.voronoi_6GPa_6nm | awk '{print $7}' > tmp.voronoi_6GPa
sed '1,9d' ../data/dump.voronoi_500K_6nm | awk '{print $7}' > tmp.voronoi_500K
#sed '1,9d' ../data/dump.voronoi_50K_6nm | awk '{print $7}' > tmp.voronoi_50K

chmod u+x plot_log.py post.py

./post.py
/usr/local/pizza-9Oct15/src/pizza.py -f plot_log.py #-q

