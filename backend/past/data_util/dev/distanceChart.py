import numpy as np

DistMatrix = np.array([[0, 0.3, 0.4, 0.7],
                       [0.3,    0,      0.9,    0.2],
                       [0.4,    0.9,    0,      0.1],
                       [0.7,    0.2,    0.1,    0]])

import networkx as nx
G = nx.from_numpy_matrix(DistMatrix)
nx.draw(G)