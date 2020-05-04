#!/bin/bash
##################################################################
##POST.SH							##
##Run scripts to post process data files of cluster dep sims 	##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2020-04-23, Syamal Praneeth Chilakalapudi, KIT, INT	##
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################


#z=55
for z in 03 23 27 55 83 113

do

	#DATA_FIL=~/Documents/work/simulations/projects/cibd_cuzr_mutli_fh2/uci_cibd/data/data.cibd_film_z-55_new
	DATA_FIL=~/Documents/work/simulations/projects/cibd_cuzr_mutli_fh2/uci_cibd/data/data.cibd_film_z-$z
	OUTPUT_DIR=~/Documents/work/simulations/projects/cibd_cuzr_mutli_fh2/uci_cibd/data

	#xlo=-109 #-109.7488709	#bound values taken manually from $DATA_FIL
	#xhi=109  #109.7488709
	#ylo=-109 #-109.7488709
	#yhi=109 #109.7488709
	#zlo=51 #-22 #-22.1725197
	#zhi=59 #193 #193.7332764
	i=$(sed -n 4p $DATA_FIL | awk '{print $1}')
	xlo=${i%.*}
	i=$(sed -n 4p $DATA_FIL | awk '{print $2}')
	xhi=${i%.*}
	i=$(sed -n 5p $DATA_FIL | awk '{print $1}')
	ylo=${i%.*}
	i=$(sed -n 5p $DATA_FIL | awk '{print $2}')
	yhi=${i%.*}
	i=$(sed -n 6p $DATA_FIL | awk '{print $1}')
	zlo=${i%.*}
	i=$(sed -n 6p $DATA_FIL | awk '{print $2}')
	zhi=${i%.*}

	#nat=2793	#number of atoms taken from $DATA_FIL manually
	#nat=10733
	nat=$(echo "$a" | sed -n 2p $DATA_FIL | awk '{print $1}')
	#echo $nat

	dt=4			#6 Angstroms search cube dimension
	#xl0=0
	#xhi=13
	xh=`echo "var=$xhi - $xlo;var=var- $xhi - var % $dt ;var" | bc`
	yh=`echo "var=$yhi - $ylo;var=var- $yhi - var % $dt ;var" | bc`
	
	sed '1,9d' $DATA_FIL | awk '{print $2 " "  $3 " " $4 " " $5}' > tmp
	#sed '1,2793!d' tmp > $OUTPUT_DIR/tmp.coords	#atom type and coords
	#sed '1,10733!d' tmp > $OUTPUT_DIR/tmp.coords	#atom type and coords
	sed "1,${nat}!d" tmp > $OUTPUT_DIR/tmp.coords	#atom type and coords
	rm -rf tmp

	python map_eval.py $xlo $xh $ylo $yh $dt $z $OUTPUT_DIR

done
