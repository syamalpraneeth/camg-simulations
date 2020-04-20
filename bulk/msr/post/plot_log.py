import os #, sys
# simple test of log tool

lg = log("../log.msr_8nm")
lg.write("tmp.log.all","Step","Temp","Enthalpy","Volume","PotEng", "KinEng","Press","Density")

#END OF LOGGING, START OF PLOTTING
g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_enth.png'")
g.aspect(1.3)				#aspect ratio
g("set ylabel 'Enthalpy'")
g("set xlabel 'Temperature'")
g("set title 'Enthalpy vs T'")	#title text
g("plot 'tmp.log.all' using 2:3 with lines linetype 4 title 'Enthalpy'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_vol.png'")
g.aspect(1.3)                           #aspect ratio
g("set ylabel 'Volume'")
g("set xlabel 'Temperature'")
g("set title 'Vol vs T'") #title text
g("plot 'tmp.log.all' using 2:4 with lines linetype 1 title 'Volume'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_temp.png'")
g.aspect(1.3)                           #aspect ratio
g("set ylabel 'Temperature'")
g("set xlabel 'Timestep'")
g("set title 'Temperature vs Timestep'") #title text
g("plot 'tmp.log.all' using 1:2 with lines linetype 1 title 'MSR'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_press.png'")
g.aspect(1.3)                           #aspect ratio
g("set ylabel 'Pressure'")
g("set xlabel 'Timestep'")
g("set title 'Pressure vs Timestep'") #title text
g("plot 'tmp.log.all' using 1:7 with lines linetype 1 title 'Pressure'")
g.stop()

g = gnu()
g.erase()				#reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_voronoi_0GPa.png'")
#g.aspect(1.3)				#aspect ratio
g("set style histogram")
g("set xtics 2")
g("set xlabel 'Number of Faces'")
g("set ylabel 'Count'")
g("set title 'Histogram of Voronoi Cell Faces: 0 GPa (before heating)'")	#title text
#g("plot 'tmp.log.comp' using 1:2 title 'Cu', 'tmp.log.comp' using 1:3 title 'Zr'")
#g.plot(x01,y01)
g("plot 'tmp.voronoi' using 1:2 w boxes fs solid 0.75 linetype 4 title 'Count'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_voronoi_500K.png'")
#g.aspect(1.3)                          #aspect ratio
g("set style histogram")
g("set xtics 2")
g("set xlabel 'Number of Faces'")
g("set ylabel 'Count'")
g("set title 'Histogram of Voronoi Cell Faces: 500 K'")        #title text
g("plot 'tmp.voronoi' using 3:4 w boxes fs solid 0.75 linetype 4 title 'Count'")
g.stop()

g = gnu()
g.erase()                               #reset all attributes to default values
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_voronoi_50K.png'")
#g.aspect(1.3)                          #aspect ratio
g("set style histogram")
g("set xtics 2")
g("set xlabel 'Number of Faces'")
g("set ylabel 'Count'")
g("set title 'Histogram of Voronoi Cell Faces: 50 K (after cooling)'")        #title text
g("plot 'tmp.voronoi' using 5:6 w boxes fs solid 0.75 linetype 4 title 'Count'")
g.stop()

g = gnu()
g.erase()
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_rdf_0GPa.png'")
g("set xlabel 'r (Angstrom)'")
g("set ylabel 'g(r)'")
g("set title 'RDF plots Nanoglass: 0 GPa (before heating)'")        #title text
g("plot 'tmp.rdf_0GPa' using 2:3 title '1-1' with linespoints, 'tmp.rdf_0GPa' using 2:6 title '2-2' with linespoints,'tmp.rdf_0GPa' using 2:9 title '1-2' with linespoints")

g = gnu()
g.erase()
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_rdf_500K.png'")
g("set xlabel 'r (Angstrom)'")
g("set ylabel 'g(r)'")
g("set title 'RDF plots Nanoglass: 500 K'")        #title text
g("plot 'tmp.rdf_500K' using 2:3 title '1-1' with linespoints, 'tmp.rdf_500K' using 2:6 title '2-2' with linespoints,'tmp.rdf_500K' using 2:9 title '1-2' with linespoints")

g = gnu()
g.erase()
g("set terminal png size 600,400 enhanced font 'Verdana,10'")
g("set output 'msr_rdf_50K.png'")
g("set xlabel 'r (Angstrom)'")
g("set ylabel 'g(r)'")
g("set title 'RDF plots Nanoglass: 50 K (after cooling)'")        #title text
g("plot 'tmp.rdf_50K' using 2:3 title '1-1' with linespoints, 'tmp.rdf_50K' using 2:6 title '2-2' with linespoints,'tmp.rdf_50K' using 2:9 title '1-2' with linespoints")
#os.remove("tmp.log.two")
#os.remove("tmp.log.count")
#os.remove("molfil.txt")

#sys.command("sys.exit()")
#print "all done ... type CTRL-D to exit Pizza.py"
#sys.exit() ===> raises exception. So I used below line from link: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei
os._exit(1)


