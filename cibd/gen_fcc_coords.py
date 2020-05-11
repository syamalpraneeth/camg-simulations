#!/home/ws/mj0054/local/anaconda3/bin/python
from __future__ import division
import math
import numpy as np

##################################################################
##								##                               
##								##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

r=3

#for i in range(1,5):
#	if i%2==0: siz=3
#	else: siz=4
#	for j in range(1,siz):
#		for k
#			x=x+4*r
#			y=y+4*r

a=np.zeros((4,64))

y=r
for i in range(1,9):
	x=r
	y=y+(math.sqrt(3)*r)
	for l1 in range(0,2):
		if i%2==0:
			siz=4-l1
			ix=2
			x=x+r
		else:
			siz=4
			ix=1
		for cnt in range(0,siz):
			x=x+4*r
#			ind=(i-1)+siz*(cnt-1)
			a[ind,1]=ix+l1
			a[ind,2]=x
			a[ind,3]=y
			ind+=1

print(a)
