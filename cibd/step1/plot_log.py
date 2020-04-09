import os #, sys
# simple test of log tool

lg = log("log.lammps")

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'comp.png'")
#g.aspect(1.3)				#aspect ratio
g("set ylabel 'Composition'")
g("set xlabel 'Radius (Angstroms)'")
g("set title 'Composition (radial)'")	#title text
g("plot 'tmp.log.comp' using 1:2 title 'Cu', 'tmp.log.comp' using 1:3 title 'Zr'")
g.stop()


#os.remove("tmp.log.two")
#os.remove("tmp.log.count")
#os.remove("tmp.log.temp")
#os.remove("tmp.log.radius")
os.remove("tmp.log.comp")
#os.remove("tmp.log.pe")
#os.remove("molfil.txt")

#sys.command("sys.exit()")
#print "all done ... type CTRL-D to exit Pizza.py"
#sys.exit() ===> raises exception. So I used below line from link: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei
os._exit(1)


