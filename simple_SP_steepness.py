from __future__ import print_function

from landlab.components import FlowRouter, FastscapeEroder, SteepnessFinder

import numpy as np
from landlab import RasterModelGrid, CLOSED_BOUNDARY
from landlab.plot.imshow import imshow_grid_at_node
import matplotlib.pyplot as plt

mg = RasterModelGrid((200, 200), 100.)

z = mg.add_zeros('node', 'topographic__elevation')
z += np.random.rand(mg.number_of_nodes)

mg.status_at_node[mg.nodes_at_left_edge] = CLOSED_BOUNDARY
mg.status_at_node[mg.nodes_at_right_edge] = CLOSED_BOUNDARY

fr = FlowRouter(mg)
sp = FastscapeEroder(mg, K_sp=1.e-5)
sf = SteepnessFinder(mg, min_drainage_area=1.e5)

dt = 20000.

for i in xrange(100):
    print(i)
    fr.route_flow()
    sp.run_one_timestep(dt)
    mg.at_node['topographic__elevation'][mg.core_nodes] += 1.

sf.calculate_steepnesses()
edges = mg.ones('node', dtype=bool)
edges.reshape(mg.shape)[2:-2, 2:-2] = False
steepness_mask = np.logical_or(sf.hillslope_mask, edges)
steepnesses = np.ma.array(mg.at_node['channel__steepness_index'],
                          mask=steepness_mask)
imshow_grid_at_node(mg, 'topographic__elevation')
imshow_grid_at_node(mg, steepnesses, color_for_closed=None,
                    cmap='winter')
plt.show()

dt=10000.
for i in xrange(100):
    print(i)
    fr.route_flow()
    sp.run_one_timestep(dt)
    mg.at_node['topographic__elevation'][mg.core_nodes] += 10.
    if i%5 == 0:
        sf.calculate_steepnesses()
        edges = mg.ones('node', dtype=bool)
        edges.reshape(mg.shape)[2:-2, 2:-2] = False
        steepness_mask = np.logical_or(sf.hillslope_mask, edges)
        steepnesses = np.ma.array(mg.at_node['channel__steepness_index'],
                                  mask=steepness_mask)
        imshow_grid_at_node(mg, 'topographic__elevation')
        imshow_grid_at_node(mg, steepnesses, color_for_closed=None,
                            cmap='winter', limits=(0., 50.))
        if i < 10:
            plt.savefig('frame_0' + str(i) + '.jpeg')
        else:
            plt.savefig('frame_' + str(i) + '.jpeg')
        plt.close('all')
