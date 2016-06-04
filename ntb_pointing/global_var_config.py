import numpy as np


DATA_TYPE = np.float64

anchor_coor = np.array([
    [-3.817, 2.416, 2.296],
    [1.062, 2.381, 2.308],
    [0.986, 2.434, -3.173],
    [-3.852, 2.434, -3.163],
    [-1.368, 2.402, 0.486],
    [-1.349, 2.431, -1.323],
    [-2.413, 0.796, -1.366],
    [-3.282, 0.738, 4.009]
], dtype=DATA_TYPE)

anchor_count = len(anchor_coor)

calc_ranging_threshold = 10

th = -0.33
th_min = -0
th_t = 5

start_count = 10

