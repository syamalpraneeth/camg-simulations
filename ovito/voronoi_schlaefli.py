# Import OVITO modules.
import os
from ovito.io import *
from ovito.modifiers import *

# Import NumPy module.
import numpy
import matplotlib.pyplot as plt
cwd = os.getcwd()
print(cwd)

# Load a simulation snapshot of a Cu-Zr metallic glass.
node = import_file("data.cibd_Cu50Zr50_3nm_250eV-film")

# Set atomic radii (required for polydisperse Voronoi tessellation).
atypes = node.source.particle_properties.particle_type.type_list
atypes[0].radius = 1.40        # Cu atomic radius (atom type 1 in input file)
atypes[1].radius = 1.60        # Zr atomic radius (atom type 2 in input file)
atypes[2].radius = 1.40        # Cu atomic radius (atom type 1 in input file)
atypes[3].radius = 1.60        # Zr atomic radius (atom type 2 in input file)
# Set up the Voronoi analysis modifier.
voro = VoronoiAnalysisModifier(
    compute_indices = True,
    use_radii = True,
    edge_count = 18, # Length after which Voronoi index vectors are truncated
    edge_threshold = 0.1
)
node.modifiers.append(voro)
                      
# Let OVITO compute the results.
node.compute()

# Make sure we did not lose information due to truncated Voronoi index vectors.
if voro.max_face_order > voro.edge_count:
    print("Warning: Maximum face order in Voronoi tessellation is {0}, "
          "but computed Voronoi indices are truncated after {1} entries. "
          "You should consider increasing the 'edge_count' parameter to {0}."
          .format(voro.max_face_order, voro.edge_count))
    # Note that it would be possible to automatically increase the 'edge_count'
    # parameter to 'max_face_order' here and recompute the Voronoi tessellation:
    #   voro.edge_count = voro.max_face_order
    #   node.compute()

# Access computed Voronoi indices as NumPy array.
# This is an (N)x(edge_count) array.
voro_indices = node.output.particle_properties['Voronoi Index'].array

# This helper function takes a two-dimensional array and computes a frequency 
# histogram of the data rows using some NumPy magic. 
# It returns two arrays (of equal length): 
#    1. The list of unique data rows from the input array
#    2. The number of occurences of each unique row
# Both arrays are sorted in descending order such that the most frequent rows 
# are listed first.
def row_histogram(a):
    ca = numpy.ascontiguousarray(a).view([('', a.dtype)] * a.shape[1])
    unique, indices, inverse = numpy.unique(ca, return_index=True, return_inverse=True)
    counts = numpy.bincount(inverse)
    sort_indices = numpy.argsort(counts)[::-1]
    return (a[indices[sort_indices]], counts[sort_indices])

# Compute frequency histogram.
unique_indices, counts = row_histogram(voro_indices)

# Print the ten most frequent histogram entries.
height = numpy.empty((10,1))
ticks = numpy.empty((10,1))
bars =[]

for i in range(10):
    print("%s\t%i\t%.1f" % (tuple(unique_indices[i,2:6]), 
                                 counts[i], 
                                 100.0*float(counts[i])/len(voro_indices)))
	#print(*'<'+str(unique_indices[i,2:6])+'>',sep='')
	#ticks[i] = tuple(unique_indices[i,2:6])
    height[i] = 100.0*float(counts[i])/len(voro_indices)
    bars.append(str(unique_indices[i,2:6]))
	#print(unique_indices[:,2:6])
print(bars)	
#bars= ['1','2','3','4','5','6','7','8','9','10']
y_pos = numpy.arange(len(bars))

#height = [3, 12, 5, 18, 45]
#bars = ('group1', 'group2', 'group3', 'group4', 'group5')
y_pos = numpy.arange(len(bars))+0.5
plt.clf()
ax = plt.gca() #you first need to get the axis handle
ax.set_aspect(1)
plt.bar(y_pos, height, color='black')
plt.xticks(y_pos, bars,rotation=45)
plt.subplots_adjust(bottom=0.3, top=0.8)
plt.ylabel('Atomic Fraction', color = 'black', fontsize='18')
plt.xlabel('Polyhedron Index', color = 'black', fontsize='18')
plt.xlim(0.0, 11)
#plt.subplots_adjust(bottom=0.3, top=0.8)

plt.savefig('250eV.png')
plt.close()

fasd