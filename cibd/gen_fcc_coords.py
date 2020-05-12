#!/home/Documents/local/anaconda3/bin/python
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

r=1.5

#for i in range(1,5):
#	if i%2==0: siz=3
#	else: siz=4
#	for j in range(1,siz):
#		for k
#			x=x+4*r
#			y=y+4*r

a=np.zeros((68,3))	# 8x5 + 7x4

for A in range(1,2):
	y=r
	ind=0
	if A==2:
		x=x+r
		y=y+((5/3)*r)

	for i in range(1,10):
		for l1 in range(0,2):
			x=r
			if i%2==0:
				if l1==1:
					siz=4-l1
				ix=1
				x=x+r
			else:
				siz=4
				ix=0
			if l1==1: x=x+2*r

			for cnt in range(0,siz):
#				ind=(i-1)+siz*(cnt-1)
				a[ind,0]=2*ix+l1+1
#				print(a[ind,0])
				a[ind,1]=x
				a[ind,2]=y
				x=x+4*r
				print(str(i)+','+str(ind)+','+str(a[ind,0]))
				ind+=1
		y=y+(math.sqrt(3)*r)

#rint(a)#

	matrix=np.matrix(a)
	#rint(matrix)
	with open('outfile.txt','wb') as f:
		for line in matrix:
			np.savetxt(f, line, fmt='%.2f')

