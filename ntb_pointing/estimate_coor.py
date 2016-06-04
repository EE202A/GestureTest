import numpy as np
from global_var_config import anchor_coor
from numpy import linalg as la


def get_estimate_coors(anchor_node, delta_rin, start):
    anchor_node_coor = anchor_coor[anchor_node]

    vec = anchor_node_coor - start
    dist = la.norm(vec)

    delta_rin = dist - delta_rin
    vec /= dist

    N = len(delta_rin)

    y = np.tile(delta_rin[:, np.newaxis], (1, 3)) * np.tile(vec, (N, 1)) \
        + np.tile(start, (N, 1))

    return y



