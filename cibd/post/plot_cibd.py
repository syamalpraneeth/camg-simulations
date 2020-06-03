#!/usr/bin/env python2.7

##################################################################
##PLOT.PY							##                               
##just playing around with matlplotlib features			##
##Dependencies	:						##
##Influences	:						##
##################################################################
## ver.	: 2019--, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com			##
##################################################################

import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt

x = np.random.rayleigh(50, size=342)
y = np.random.rayleigh(50, size=342)
z = np.random.rayleigh(50, size=342)

m = np.genfromtxt('outfile.txt', delimiter=' ')

#print(m)

#print(x,y,z)

print(m.shape)
c = np.array(m)

print(c)

#plt.hist2d(c[:,0],y[:,1], bins=[np.arange(0,400,5),np.arange(0,300,5)])


x=c[:,0]
y=c[:,1]

#print(type(y))
print(x.shape)
print(y.shape)
plt.hexbin(c[:,0],c[:,1],C=c[:,4])
#plt.hexbin(x,y,C=c[:,[2]])

plt.show()
