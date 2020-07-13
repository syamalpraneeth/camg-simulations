import os , sys
# simple test of log tool

lg = log("../log.cluster_anneal_restart_3nm")
#print "# of vectors =",lg.nvec
#print "length of vectors =",lg.nlen
#print "names of vectors =",lg.names
#time,temp,press = lg.get("Step","Temp","Press")
#print temp,press
#lg.write("tmp.log") #all the thermostuff
lg.write("tmp.log.diffuse","Step","v_ce1", "v_se1", "v_ce2", "v_se2")
lg.write("tmp.log.two","Step","Temp")
#lg.write("tmp.log.count","Step","v_cndep","v_ckeep")
#lg.write("tmp.log.temp","Step","c_tg","c_tk")
#lg.write("tmp.log.radius","Step","v_rad")

print 'all okay 1'

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'comp.png'")
#g.aspect(1.3)				#aspect ratio
g("set ylabel 'Composition'")
g("set xlabel 'Radius (Angstroms)'")
g("set title 'Composition (radial)'")	#title text
g("plot 'tmp.log.comp' using 1:2 title 'Cu' w lp, 'tmp.log.comp' using 1:3 title 'Zr' w lp")
g.stop()

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'comp-cu.png'")
#g.aspect(1.3)				#aspect ratio
g("set ylabel 'Composition (at %)'")
g("set xlabel 'Timesteps'")
g("set title 'Composition Time Evolution: Cu'")	#title text
g("plot 'tmp.log.diffuse' using 1:2 title 'Core' w lp, 'tmp.log.diffuse' using 1:3 title 'Shell' w lp")
g.stop()

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'comp-zr.png'")
#g.aspect(1.3)				#aspect ratio
g("set ylabel 'Composition (at %)'")
g("set xlabel 'Timesteps'")
g("set title 'Composition Time Evolution: Zr'")	#title text
g("plot 'tmp.log.diffuse' using 1:4 title 'Core' w lp, 'tmp.log.diffuse' using 1:5 title 'Shell' w lp")
g.stop()

os._exit(1)
sys.exit()

#END OF LOGGING, START OF PLOTTING
g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'atom_count.png'")
g.aspect(1.3)				#aspect ratio
g("set ylabel 'Atom count'")
g("set xlabel 'Timestep'")
g("set title 'Atom count vs timestep'")	#title text
g("plot 'tmp.log.count' using 1:2 with lines linetype 4 title 'Gas', 'tmp.log.count' using 1:3 with lines linetype 1 title 'Cluster'")
g.stop()

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'temp_profiles.png'")
g.aspect(1.3)				#aspect ratio
g("set ylabel 'Temperature'")
g("set xlabel 'Timestep'")
g("set title 'Temperature profiles'")	#title text
g("plot 'tmp.log.temp' using 1:2 with lines linetype 4 title 'Gas', 'tmp.log.temp' using 1:3 with lines linetype 1 title 'Cluster'")
g.stop()

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'radius.png'")
#g.aspect(1.3)				#aspect ratio
g("set ylabel 'Radius'")
g("set xlabel 'Timestep'")
g("set title 'Growth of cluster'")	#title text
g("plot 'tmp.log.radius' using 1:2 with lines title 'Radius'")
g.stop()

print 'all okay 2'

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'pe.png'")
#g.aspect(1.3)				#aspect ratio
g("set ylabel 'Potential Energy (eV)'")
g("set xlabel 'Radius (Angstroms)'")
g("set title 'Potential Energy (radial)'")	#title text
g("plot 'tmp.log.pe' using 1:2 with lines title 'pe'")
g.stop()


os.remove("tmp.log.two")
os.remove("tmp.log.count")
os.remove("tmp.log.temp")
os.remove("tmp.log.radius")
os.remove("tmp.log.comp")
os.remove("tmp.log.pe")
#os.remove("molfil.txt")

#sys.command("sys.exit()")
#print "all done ... type CTRL-D to exit Pizza.py"
#sys.exit() ===> raises exception. So I used below line from link: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei
os._exit(1)


