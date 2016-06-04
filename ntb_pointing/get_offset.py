import numpy as np
import os
from calc_ranging import calc_ranging
from global_var_config import DATA_TYPE
from theoretical_ranges import theoretical_ranges
from global_var_config import anchor_count


def calc_offset(ntb, mocap):
    recv_ids = ntb[:, 2]
    offsets = []

    for iNode in range(anchor_count):
        logic = (recv_ids == iNode)

        missing_bool = False
        for iLogic in np.nditer(logic):
            if iLogic:
                missing_bool = True
                break

        if not missing_bool:
            print '[get_offset]: ' + 'Offset calc missing node', iNode
            offsets.append(0)
        else:
            times = ntb[logic, 4:10]
            ntb_range, mask = calc_ranging(times)
            ntb_range = ntb_range[mask]

            th_ranges = theoretical_ranges(mocap[:, 2:5], iNode)

            offset = np.mean(ntb_range) - np.mean(th_ranges)

            offset = offset.astype(DATA_TYPE)
            offsets.append(offset)

    return np.asarray(offsets)


def get_offset(anchor_node):

    # re = 0
    # # check if cached offset exist
    # if os.path.exists('./offsets/offset.csv'):
    #     re = np.genfromtxt('./offsets/offset.csv', delimiter=',', dtype=DATA_TYPE)[anchor_node]
    #     # print 'Load offset from cache, offset: ', re
    # elif os.path.exists('./offsets/ntb_offset1.csv') and \
    #      os.path.exists('./offsets/mocap_offset1.csv'):

    #     ntb = np.genfromtxt('./offsets/ntb_offset1.csv', delimiter=',', dtype=DATA_TYPE)
    #     mocap = np.genfromtxt('./offsets/mocap_offset1.csv', delimiter=',', dtype=DATA_TYPE)
    #     offsets = calc_offset(ntb, mocap)

    #     np.savetxt('./offsets/offset.csv', offsets, delimiter=',')

    #     re = offsets[anchor_node]

    #     # print 'Calc offset from data, offset: ', re
    # else:
    #     print '[get_offset]: ' + 'No offset data csv file!'

    offset = [0.656404984046231,
          0.544461924111784,
          0.471641501845964,
          0.532032426364947,
          0.473179630062969,
          0.574526533721972,
          0.515944162706270,
          1.345990857037977]


    return offset[anchor_node]
