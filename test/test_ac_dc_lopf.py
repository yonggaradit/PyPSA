from __future__ import print_function, division
from __future__ import absolute_import

import pypsa

import datetime
import pandas as pd

import networkx as nx

import numpy as np

from itertools import chain, product

import os



from distutils.spawn import find_executable



def test_lopf():


    csv_folder_name = "../examples/ac-dc-meshed/ac-dc-data"

    network = pypsa.Network(csv_folder_name=csv_folder_name)

    results_folder_name = os.path.join(csv_folder_name,"results-lopf")

    network_r = pypsa.Network(csv_folder_name=results_folder_name)


    #test results were generated with GLPK and other solvers may differ
    solver_name = "glpk"

    snapshots = network.snapshots

    for formulation, free_memory in product(["angles", "cycles", "kirchhoff", "ptdf", "angles-flows", "cycles-flows", "ptdf-flows"],
                                            [{}, {"pypsa"}, {"pypsa", "pyomo-hack"}]):
        network = pypsa.Network(csv_folder_name=csv_folder_name)
        network.lopf(snapshots=snapshots,solver_name=solver_name,formulation=formulation, free_memory=free_memory)
        print(network.generators_t.p.loc[:,network.generators.index])
        print(network_r.generators_t.p.loc[:,network.generators.index])

        np.testing.assert_array_almost_equal(network.generators_t.p.loc[:,network.generators.index],network_r.generators_t.p.loc[:,network.generators.index])
        np.testing.assert_array_almost_equal(network.buses_t.v_ang, network_r.buses_t.v_ang)
        if not formulation.endswith('-flows'):
            np.testing.assert_array_almost_equal(network.lines_t.p0.loc[:,network.lines.index],network_r.lines_t.p0.loc[:,network.lines.index])


if __name__ == "__main__":
    test_lopf()
