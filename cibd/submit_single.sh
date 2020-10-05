#!/bin/bash
##################################################################
##								##
##								##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

v=3
sbatch --job-name="cibd_cuzr_"$v"nm" --output="cibd_"$v"nm_%ameV".out --export=ALL,v=$v job.arr.cibd_single
