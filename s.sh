#!/bin/bash
##################################################################
##								##
##								##
#Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

#a=($(sed '1,7d' param | awk '{print $1}'))
a=($(awk '{print $1}' param))
./test.py "${a[@]}"
