#!/bin/bash
##################################################################
##                                                              ##
##                                                              ##
##Dependencies  :                                               ##
##Influences    :                                               ##
##################################################################
## ver. : 2019--, Syamal Praneeth Chilakalapudi, KIT, INT       ##
##Author Email    :syamalpraneeth@gmail.com                     ##
##################################################################

v=3	#size of cluster diameter
sub=24	#size of substrate edge
sbatch --job-name="cibd_cuzr_"$v"nm" --output="cibd_multi_"$v"nm_%ameV".out --export=ALL,v=$v,sub=$sub job.arr.cibd 

