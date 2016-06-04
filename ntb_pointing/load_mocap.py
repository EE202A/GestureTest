import os
import numpy as np
from global_var_config import DATA_TYPE


def get_mocap_data(global_mocap_data):
    re_mocap = []

    if len(global_mocap_data) != 0:
        re_mocap = global_mocap_data
    else:
        print '[load_mocap]: ' + 'No Mocap data!!!'

    return re_mocap
