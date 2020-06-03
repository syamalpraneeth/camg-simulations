#!/usr/bin/env python

##################################################################
##POST.PY							##
##Script to make histogram data from dump voronoi files. The 	##
##data will be later used to plot from plot_log.py		##
##################################################################
##Depends upon  : tmp.voronoi.*, proc.sh			##
##Influences    : plot_log.py, voronoi*.png			##
##################################################################
## ver. : 2019-05-21, Syamal Praneeth Chilakalapudi, KIT, INT	##
##Author Email    :syamalpraneeth@gmail.com                     ##
##################################################################

import numpy as np
import math

a1 = np.loadtxt("tmp.voronoi_0GPa")
r1 = range(0,int(max(a1)+5))
a2 = np.loadtxt("tmp.voronoi_6GPa")
r2 = range(0,int(max(a2)+5))
a3 = np.loadtxt("tmp.voronoi_500K")
r3 = range(0,int(max(a3)+5))
a4 = np.loadtxt("tmp.voronoi_50K")
r4 = range(0,int(max(a4)+5))
r = max(r1,r2,r3,r4)

h1, e1 = np.histogram(a1,bins=r)
h2, e2 = np.histogram(a2,bins=r)
h3, e3 = np.histogram(a3,bins=r)
h4, e4 = np.histogram(a4,bins=r)

mat = np.vstack((e1[:-1],h1,e2[:-1],h2,e3[:-1],h3,e4[:-1],h4))
m = np.transpose(mat)
np.savetxt('tmp.voronoi',m,fmt='%2i')
