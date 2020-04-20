#!/usr/bin/env python

#uncomment the following block when run with mpi4py
from mpi4py import MPI
comm = MPI.COMM_WORLD
me = comm.Get_rank()
nprocs = comm.Get_size()

import sys
from molefile import molfil
from lammps import lammps

diam	= int(sys.argv[6])				#convert to Angstroms units

lst=["-log log.cluster"]
l = lammps(name="mpi") #,cmdargs=lst)
logcmd="log log.cluster_"+str(diam)+"nm"
l.command(logcmd)

l.command("variable	lat equal 3.6")
l.command("variable	pot string "+str(sys.argv[1]))
l.command("variable	e1 string "+str(sys.argv[2]))
l.command("variable	e2 string "+str(sys.argv[3]))

frac 	= float(sys.argv[5])/(float(sys.argv[4])+float(sys.argv[5]))
l.command("variable	frac equal "+str(frac));

l.command("variable	dia equal "+str(diam))
l.command("variable	s equal (${dia}/2+1)*10")
l.command("variable	R equal (${dia}/2)*10 #*(${lat})")

t	= int(sys.argv[7])
T	= int(sys.argv[8])
l.command("variable	T1 equal "+str(t))		#cluster equilibriation duration
l.command("variable	T2 equal "+str(T))		#glass quench

th	= t//10
df	= t//20
l.command("variable	th equal "+str(th));
l.command("variable	df equal "+str(df));

l.file("in.cluster")					#grow and equilibriate cluster
molfil(l,comm,me,nprocs,sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]))
