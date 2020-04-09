#!/usr/bin/env python

# uncomment the following block when run with mpi4py
from canal import analysis  # uncomment for a parallel run with mpi4py
from lammps import lammps
from molefile import molfil
import sys
from mpi4py import MPI
comm = MPI.COMM_WORLD
me = comm.Get_rank()
nprocs = comm.Get_size()

# from canal_ser import analysis		#uncomment for a serial run
l = lammps()

num1 = 0  # counts the cycles
num2 = 0
n1 = int(sys.argv[8])
n2 = int(sys.argv[9])
siz = int(sys.argv[10])
t1 = int(sys.argv[11])
t2 = int(sys.argv[11])
T = int(sys.argv[12])
th = T//50
df = th//100

l.command("variable	ini1 equal "+str(sys.argv[6]))
l.command("variable	ini2 equal "+str(sys.argv[7]))
l.command("variable	pot string "+str(sys.argv[1]))
l.command("variable	e1 string "+str(sys.argv[2]))
l.command("variable	e2 string "+str(sys.argv[3]))

l.file("in.run1")  # initialize

# these variables store computes
l.command("variable	cndep equal count(dep)")
l.command("variable	ckeep equal count(keep)")
l.command("variable	call equal count(all)")
l.command("variable	rad equal 0")
# iters = 10					#number of "flush and repeat" cycles to make
# l.command("variable	l equal "+str(iters))		#number of iterations
l.command("variable	v equal 10")  # deposition velocity variable
l.command("variable	l equal 1")  # number of iterations
l.command("variable	t1 equal "+str(t1))  # gas equilibriation duration
l.command("variable	T equal "+str(T))  # growth run duration
l.command("variable	t equal (v_T)/(v_l)")  # interval for analysis in looping
l.command("variable	t2 equal "+str(t2))  # cluster equilibriation duration
# idea: define total time duration as 400000 or so. t2 is 400000-$(step)
l.command("variable	th equal "+str(th))
l.command("variable	n1 equal "+str(n1))
l.command("variable	n2 equal "+str(n2))
l.command("variable	r1 equal (v_t)/(v_n1)")
l.command("variable	r2 equal (v_t)/(v_n2)")
l.command("variable	sr equal (v_r1)/2")
l.command("variable	dr equal "+str(df))

l.file("in.run2")  # computes, thermo, gas equilibriation, dump

# for i in range(0,nprocs):
m = l.extract_global("nlocal", 0)
# print(me,m)

# for num1 in range(0,l1-1):
# while ((num2 < siz) and (num1 < iters)):
while (num2 < siz):
    l.command("variable	a equal "+str(num1+1))
    l.file("in.run3")  # modify region, deposit, allow for analysis

    # for i in range(0,nprocs):
    m = l.extract_global("nlocal", 0)
#	print(me,m)

    # analysis
    analysis(l, comm, me, nprocs)  # idenitifies 'good' atoms here
    l.file("in.run4")  # centre cluster, delete bad atoms

    num2 = l.extract_variable("ckeep", "all", 0)
    num1 = num1+1
    l.command("write_restart data/restart.growth")  # needs mpiio
    if me == 0:
        f = open("data/success.log", "a+")
        f.write("Run worked. Iter %d Clus size %d \n" % ((num1), (num2)))
        f.close

# equilibriation and finalise cluster
l.file("in.run5")  # equilibriate cluster, output for molecule
molfil(l, comm, me, nprocs, sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
