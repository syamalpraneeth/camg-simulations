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


DATA_FIL=~/Documents/work/simulations/projects/cibd_cuzr_mutli_fh2/uci_cibd/data/data.cibd_film_z-55_new
OUTPUT_DIR=~/Documents/work/simulations/projects/cibd_cuzr_mutli_fh2/uci_cibd/data

xlo=-109 #-109.7488709	#bound values taken manually from $DATA_FIL
xhi=109  #109.7488709
ylo=-109 #-109.7488709
yhi=109 #109.7488709
zlo=51 #-22 #-22.1725197
zhi=59 #193 #193.7332764

z=55
nat=2793	#number of atoms taken from $DATA_FIL manually
dt=6			#6 angstroms thickness cube
#xl0=0
#xhi=13
xh=`echo "var=$xhi - $xlo;var=var- $xhi - var % $dt ;var" | bc`
yh=`echo "var=$yhi - $ylo;var=var- $yhi - var % $dt ;var" | bc`

sed '1,9d' $DATA_FIL | awk '{print $2 " "  $3 " " $4 " " $5}' > tmp
sed '1,2793!d' tmp > $OUTPUT_DIR/tmp.coords	#atom type and coords
rm -rf tmp

python map_eval.py $xlo $xhi $ylo $yhi $dt $z $OUTPUT_DIR


