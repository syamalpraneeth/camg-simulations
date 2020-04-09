#!/bin/sh

for i in 050 100 200 300 400 500
do
	mkdir $i
	cp in.dep_stg1 restart.sub clusmol_565.txt $i/
	cd $i
	/usr/local/lammps-22Aug18/src/lmp_ubuntu < in.dep_stg1 -log dep.log.lammps -var en $i > cibd.out
	cd ..
done

