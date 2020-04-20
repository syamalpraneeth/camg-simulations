##################################################################
##PLOT_LOG.PY							##                               
##Pizza.py based Script to post-process RDFs, voronoi		##
##histograms, temperature, pressure, and density evolution	##
##of nanoglass.							##
##Depends upon	: ../log.lammps					##
##Influences	: *.png, *.log.*				##
##################################################################
## ver. : 2019-05-06, Syamal Praneeth Chilakalapudi, KIT, INT	##                            
##Author Email    :syamalpraneeth@gmail.com                     ##
##################################################################

import os, numpy as np #, sys

print("From plot_log.py: Did you change the name of the log file?")
lg = log("../log.nanoglass_6nm")
lg.write("tmp.log.all","Step","Temp","Density","Press","Enthalpy","Volume","PotEng", "KinEng",)
lg.write("tmp.log.dtp","Step","Temp","Density","Press")
mat = np.loadtxt('tmp.voronoi')
x01 = mat[:,0]
x02 = mat[:,2]
x03 = mat[:,4]
y01 = mat[:,1]
y02 = mat[:,3]
y03 = mat[:,5]

#END OF LOGGING, START OF PLOTTING
g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_temp.png'")
#g.aspect(1.3)					#aspect ratio
g("set ylabel 'Temperature'")
g("set xlabel 'Timestep'")
g("set title 'Temperature vs timestep'")	#title text
g("plot 'tmp.log.dtp' using 1:2 with lines linetype 4 title 'Nanoglass'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_pres.png'")
#g.aspect(1.3)                                  #aspect ratio
g("set ylabel 'Pressure'")
g("set xlabel 'Timestep'")
g("set title 'Pressure vs timestep'")        #title text
g("plot 'tmp.log.dtp' using 1:4 with lines linetype 4 title 'Nanoglass'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_density.png'")
#g.aspect(1.3)                                  #aspect ratio
g("set ylabel 'Density'")
g("set xlabel 'Timestep'")
g("set title 'Density vs timestep'")        #title text
g("plot 'tmp.log.dtp' using 1:3 with lines linetype 4 title 'Nanoglass'")
g.stop()

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_voronoi_0GPa.png'")
#g.aspect(1.3)				#aspect ratio
g("set style histogram")
g("set xtics 2")
g("set xlabel 'Number of Faces'")
g("set ylabel 'Count'")
g("set title 'Histogram of Voronoi Cell Faces: 0 GPa (before compaction)'")	#title text
#g("plot 'tmp.log.comp' using 1:2 title 'Cu', 'tmp.log.comp' using 1:3 title 'Zr'")
#g.plot(x01,y01)
g("plot 'tmp.voronoi' using 1:2 w boxes fs solid 0.75 linetype 4 title 'Count'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_voronoi_6GPa.png'")
#g.aspect(1.3)                          #aspect ratio
g("set style histogram")
g("set xtics 2")
g("set xlabel 'Number of Faces'")
g("set ylabel 'Count'")
g("set title 'Histogram of Voronoi Cell Faces: 6 GPa'")        #title text
g("plot 'tmp.voronoi' using 3:4 w boxes fs solid 0.75 linetype 4 title 'Count'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_voronoi_500K.png'")
#g.aspect(1.3)                          #aspect ratio
g("set style histogram")
g("set xtics 2")
g("set xlabel 'Number of Faces'")
g("set ylabel 'Count'")
g("set title 'Histogram of Voronoi Cell Faces: 500 K'")        #title text
g("plot 'tmp.voronoi' using 5:6 w boxes fs solid 0.75 linetype 4 title 'Count'")
g.stop()

#g = gnu()
#g.erase()                               #reset all attributes to default values
#g("set terminal png size 600,400 enhanced font 'Verdana,10'")
#g("set output 'ng_voronoi_50K.png'")
#g.aspect(1.3)                          #aspect ratio
#g("set style histogram")
#g("set xtics 2")
#g("set xlabel 'Number of Faces'")
#g("set ylabel 'Count'")
#g("set title 'Histogram of Voronoi Cell Faces: 50 K (after cooling))'")        #title text
#g("plot 'tmp.voronoi' using 7:8 w boxes fs solid 0.75 linetype 4 title 'Count'")
#g.stop()

g = gnu()
g.erase()
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_rdf_0GPa.png'")
g("set xlabel 'r'")
g("set ylabel 'g(r)'")
g("set title 'RDF plots CuZr Nanoglass: 0 GPa (before compaction)'")        #title text
g("plot 'tmp.rdf_0GPa' using 2:3 title '1-1' with linespoints, 'tmp.rdf_0GPa' using 2:6 title '2-2' with linespoints,'tmp.rdf_0GPa' using 2:9 title '1-2' with linespoints")

g = gnu()
g.erase()
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_rdf_6GPa.png'")
g("set xlabel 'r (Angstroms)'")
g("set ylabel 'g(r)'")
g("set title 'RDF plots CuZr Nanoglass: 6 GPa'")        #title text
g("plot 'tmp.rdf_6GPa' using 2:3 title '1-1' with linespoints, 'tmp.rdf_6GPa' using 2:6 title '2-2' with linespoints,'tmp.rdf_6GPa' using 2:9 title '1-2' with linespoints")

g = gnu()
g.erase()
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'ng_rdf_500K.png'")
g("set xlabel 'r (Angstroms)'")
g("set ylabel 'r (Angstroms)'")
g("set title 'RDF plots CuZr Nanoglass: 500 K'")        #title text
g("plot 'tmp.rdf_500K' using 2:3 title '1-1' with linespoints, 'tmp.rdf_500K' using 2:6 title '2-2' with linespoints,'tmp.rdf_500K' using 2:9 title '1-2' with linespoints")

#g = gnu()
#g.erase()
#g("set terminal png size 600,400 enhanced font 'Verdana,10'")
#g("set output 'ng_rdf_50K.png'")
#g("set xlabel 'r'")
#g("set ylabel 'g(r)'")
#g("set title 'RDF plots CuZr Nanoglass: 50 K (after cooling)'")        #title text
#g("plot 'tmp.rdf_50K' using 2:3 title '1-1' with linespoints, 'tmp.rdf_50K' using 2:6 title '2-2' with linespoints,'tmp.rdf_50K' using 2:9 title '1-2' with linespoints")

g.stop()


#os.remove("tmp.log.dtp")

#sys.command("sys.exit()")
#print "all done ... type CTRL-D to exit Pizza.py"
#sys.exit() ===> raises exception. So I used below line from link: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei
os._exit(1)
