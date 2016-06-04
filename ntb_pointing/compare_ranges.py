import numpy as np
from numpy import linalg as la


def get_score_of_nodes(base_time, th_range, anchor_time, actual_range):

    if anchor_time[0] > base_time[0] or anchor_time[-1] < base_time[-1]:
        print '[compare_ranges]: ' + 'Error interpolate!'
        return -1
    else:
		# print "type of base_time is ", type(base_time[0]), "type of anchor_time is ", type(anchor_time[0]), "type of actual_range is ", type(actual_range[0]), 
		x21 = np.interp(base_time, anchor_time, actual_range)
		x21 = x21 - (x21[0] - th_range[0])

		y = la.norm(x21 - th_range) / len(th_range)
		return y