import numpy as np
import pickle as pkl
import os
from global_var_config import DATA_TYPE
from calc_ranging import calc_ranging
from find_slot import get_slot
from mov_avg_filter import smooth_filter


offset = [0.656404984046231,
          0.544461924111784,
          0.471641501845964,
          0.532032426364947,
          0.473179630062969,
          0.574526533721972,
          0.515944162706270,
          1.345990857037977]


def read_ntb_data_test(anchor_node, global_ntb_data):
    re_ntb = []
    re_posix_t = []
    if len(global_ntb_data) != 0:
        # ntb = np.genfromtxt(filename, delimiter=',', dtype=DATA_TYPE)
        ntb = global_ntb_data
        timestamps = ntb[:, 0]
        recv_ids = ntb[:, 2]

        logic = (recv_ids == anchor_node)
        missing_bool = False
        for iLogic in np.nditer(logic):
            if iLogic:
                missing_bool = True
                break

        if not missing_bool:
            pass
            # print '[ntb_data_from_others]: ' + 'Missing Anchor node: ', anchor_node, ' data!!!'

        else:
            times = ntb[logic, 4:10]
            ntb_range, mask = calc_ranging(times)
            ntb_range = ntb_range[mask]

            ntb_range = ntb_range - offset[anchor_node]

            posix_t = timestamps[logic]
            posix_t = posix_t[mask]

            re_ntb = ntb_range
            re_posix_t = posix_t

    else:
        print '[ntb_data_from_others]: ' + 'No Anchor node: ', anchor_node, ' data!!!'

    return re_ntb, re_posix_t


def get_ntb_from_others(base_time_span, global_ntb_data):
    # currently read from the cache
    # TODO: fetch interpolated smoothed strokes from other nodes base on time span

    ntb_ranges_data = []
    ntb_times_data = []
    idx = []

    for iNode in range(8):
        ntb_range, ntb_time = read_ntb_data_test(iNode, global_ntb_data)
        begin_idx, end_idx = get_slot(base_time_span, ntb_time)

        if begin_idx == -1:
            print '[ntb_data_from_others]: ' + 'No time corresponding data at anchor node: ', iNode
            ntb_ranges_data.append([])
            ntb_times_data.append([])
            idx.append(iNode)
        else:
            # smooth the stroke and dump into a pkl file
            rr = smooth_filter(ntb_range)

            ntb_ranges_data.append(rr[begin_idx:end_idx+1])
            ntb_times_data.append(ntb_time[begin_idx:end_idx+1])
            idx.append(iNode)

    pkl_data = {'idx': idx,
                'time_span': ntb_times_data,
                'range_data': ntb_ranges_data}

    return pkl_data


def get_localization_data(global_ntb_data):
    re = []
    for iNode in range(8):
        ntb, time = read_ntb_data_test(iNode, global_ntb_data)
        re.append(np.array(ntb, dtype=np.float64))

    re = np.asarray(re)
    return re
























