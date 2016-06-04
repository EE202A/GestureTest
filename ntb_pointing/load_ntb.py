import numpy as np
import os
from global_var_config import DATA_TYPE
from calc_ranging import calc_ranging


def get_ntb_data(anchor_node, offset, local_ntb_data):

    re_ntb = []
    re_posix_t = []
    if len(local_ntb_data) != 0:
        ntb = local_ntb_data
        timestamps = ntb[:, 0]
        recv_ids = ntb[:, 2]

        logic = (recv_ids == anchor_node)
        missing_bool = False
        for iLogic in np.nditer(logic):
            if iLogic:
                missing_bool = True
                break

        if not missing_bool:
            print '[load_ntb]: ' + 'Missing Anchor node: ', anchor_node, ' data!!!'
        else:
            times = ntb[logic, 4:10]
            ntb_range, mask = calc_ranging(times)
            ntb_range = ntb_range[mask]

            ntb_range = ntb_range - offset

            posix_t = timestamps[logic]
            posix_t = posix_t[mask]

            re_ntb = ntb_range
            re_posix_t = posix_t
    else:
        print '[load_ntb]: ' + 'No Anchor node: ', anchor_node, ' data!!!'

    return re_ntb, re_posix_t


