##!/usr/bin/env python2.7

##################################################################
##MOLEFILE.PY							##                               
##Generate molecule file from 					##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver. : 2019-06-24, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

import numpy as np
import pipes
import os
import time

def molfil(lmp,comm,rnk,num,a,b,x,y):
	n = lmp.get_natoms()
	matrix = np.zeros((1,7))
	for i in range(0,num):
		if i==rnk:						#collect data from each proc
			m = lmp.extract_global("nlocal",0)
			arr1 = np.zeros((m,7))
			mss1 = np.zeros((m,1))
			cvec = lmp.extract_fix("f8",1,2,0,0)
                        ids1 = lmp.extract_atom("id",0)
			mss1 = lmp.extract_atom("mass",0)
                        typ1 = lmp.extract_atom("type",0)
			ind=0
			for x in cvec:
				for y in range(3,7):			#'4' is the number of values/columns in fix f8. dependant on in.cluster
					print("For rank %s index %s value is %s" % (rnk, (y-3), x[y-3]))
					arr1[ind,y] = x[y-3]		#python array indexes from 0
				arr1[ind,0] = ids1[ind] 
				arr1[ind,1] = typ1[ind]
				arr1[ind,2] = mss1[ind]
#	        		print(arr1[ind,2])
		                ind=ind+1
				if ind==m:
					break

			if i>0:
				matrix = comm.recv(source=(rnk-1)%num)
#append data of proc i-1 to proc i
                        matrix = np.append(matrix,arr1,axis=0)
			if i==0:
				matrix = np.delete(matrix,0,0)
			comm.send(matrix,dest=(rnk+1)%num)
			time.sleep(0.02)
#final append at rank 0 proc
	if rnk==0:
		matrix = comm.recv(source=(rnk-1)%num)
#		mass = np.sum(matrix[:,2], axis=0)
#write collected data to file to generate a cluster molecule template for later	
        	name = 'data/clusmol_'+str(a)+str(x)+str(b)+str(y)+'_'+str(n)+'.txt'
	        t2	= open(name,'w')
        	t2.write('LAMMPS molecule file \n \n')
	        t2.write(str(n) + " atoms \n \n")
#		t2.write(str(mass) + " mass \n \n")
#For reference, fix f8 in in.run5: fix f8 all ave/atom 1 1 1 mass x y z c_c5 where, c_c5 is pe/atom compute
#For the following, find help here: https://stackoverflow.com/questions/46789812/printing-accessing-specific-columns-of-a-matrix-as-a-matrix-in-python
        	t2.write('Coords \n \n')
                np.savetxt(t2, matrix[:,[0,3,4,5]], fmt='%3.0f %4.5f %4.5f %4.5f' , delimiter=' \t', newline='\n')
        	t2.write('\n')
	        t2.write('Types \n \n')
        	np.savetxt(t2, matrix[:,[0,1]], fmt='%3.0f %2.0f' , delimiter=' ', newline='\n')
#		t2.write('Masses \n \n')
#       	np.savetxt(t2, matrix[:,[0,2]], fmt='%3.0f %2.0f' , delimiter=' ', newline='\n')
#	        t2.write('\n \n')
        	t2.close()
