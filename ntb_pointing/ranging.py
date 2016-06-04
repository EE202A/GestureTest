import numpy as np
from get_offset import get_offset
from load_ntb import get_ntb_data
from load_mocap import get_mocap_data
from find_first_valley import get_first_valley
from estimate_coor import get_estimate_coors
from theoretical_ranges import theoretical_ranges_with_all
from ntb_data_from_others import get_ntb_from_others, get_localization_data
from compare_ranges import get_score_of_nodes
from localization import localization


class ntb_score:

    local_ntb_data = []
    anchor_node = []
    stroke = []
    ids = []
    posix_time = []

    def __init__(self, anchor_node, local_ntb_data):
        self.local_ntb_data = self.parse(local_ntb_data)
        # print self.local_ntb_data
        self.anchor_node = anchor_node
        pass

    def parse(self, raw_data):
        bigarr = []
        for data in raw_data:
            arr = []
            msgTime = data.header.stamp
            timeFloat = msgTime.secs + msgTime.nsecs*1.0e-9
            arr.append(timeFloat)
            arr.append(data.src)
            arr.append(data.dst)
            arr.append(data.seq)
            arr.append(data.ts1)
            arr.append(data.ts2)
            arr.append(data.ts3)
            arr.append(data.ts4)
            arr.append(data.ts5)
            arr.append(data.ts6)
            arr.append(data.fploss)
            bigarr.append(arr)

        return np.array(bigarr)

    def find_valley(self):
        # print "NTBBBBBBB: ", len(self.local_ntb_data)
        offset = get_offset(self.anchor_node)

        ntb_range, posix_time = get_ntb_data(self.anchor_node, offset, self.local_ntb_data)

        # print "[NTBBBBBBB]: ntb_range=", ntb_range
        if len(ntb_range) == 0:
            print '[ranging]: ' + 'Anchor node: ', self.anchor_node, ' get no data, output score is -1'
            return False

        find_valley, ids, stroke = get_first_valley(ntb_range)

        self.stroke = stroke
        self.ids = ids
        self.posix_time = posix_time

        if not find_valley:
            # print '[ranging]: ' + 'Find no valley at this anchor node! output score is -1'
            return False
        else:
            # print "[ranging]: Yingnan: valley founded"
            return True

    # if find valley then get the global ntb data and then calc score
    # if didn't find valley then score is (-1, -1) and don't need to get the global ntb data.
    # this should be set in ray's function
    def get_score(self, global_ntb_data):
        global_ntb_data = self.parse(global_ntb_data)
        localization_data = get_localization_data(global_ntb_data)
        # localization_data = localization_data.astype(np.float64)
        start = localization(localization_data)
        if len(start) == 0:
            return [-1, -1]

        coors = get_estimate_coors(self.anchor_node, self.stroke, start)
        # calc the theoretical range with all node
        th_ranges = theoretical_ranges_with_all(coors)
        t = self.posix_time[self.ids]

        pkl_data = get_ntb_from_others(t, global_ntb_data)

        scores = []
        for iNode in range(len(pkl_data['idx'])):
            node_idx = pkl_data['idx'][iNode]
            if len(pkl_data['time_span'][node_idx]) == 0:
                scores.append(0)
            else:
                score = get_score_of_nodes(t, th_ranges[:, node_idx], pkl_data['time_span'][node_idx], pkl_data['range_data'][node_idx])
                scores.append(score)

        return np.mean(scores), np.var(scores)