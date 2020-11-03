#!/bin/bash

l="5 50 250 5000"
#l2=[5, 50, 250, 5000]

for i in ${l[@]}
do
/usr/local/pizza-9Oct15/src/pizza.py -f log_cibd_single.py $i
done

./plot_cibd_single.py ${l[@]}
#rm -rf tmp*
