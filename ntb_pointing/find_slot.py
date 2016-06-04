import numpy as np


def get_slot(target_time, total_time):
    begin_idx = -1
    end_idx = -1

    if len(target_time) == 0 or len(total_time) == 0:
        return begin_idx, end_idx

    if total_time[0] > target_time[0] or \
       total_time[-1] < target_time[-1]:
        return begin_idx, end_idx
    else:
        begin_idx = np.where(total_time <= target_time[0])[0][-1]
        end_idx = np.where(total_time >= target_time[-1])[0][0]
        return begin_idx, end_idx

