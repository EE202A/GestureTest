import numpy as np
from global_var_config import th, th_min, th_t, start_count
from mov_avg_filter import smooth_filter

def get_first_valley(signal):

    find_valley = False
    ids = []
    stroke = []

    n = signal.shape[0]

    if n < 20:
        return find_valley, ids, stroke

    offset = np.mean(signal[0:start_count])

    y = smooth_filter(signal)

    shift = 2
    delta_y = y[shift:n] - offset
    n -= shift

    idx = np.where(delta_y < th)[0]
    if len(idx) == 0:
        return find_valley, ids, stroke
    else:
        idx = idx[0]

    left = idx - 1
    while (left > 0 and delta_y[left] > delta_y[left+1] and delta_y[left] < th_min):
        left -= 1

    if np.mean(delta_y[0:left]) > abs(th)*2/3:
        return find_valley, ids, stroke

    while (idx < n and delta_y[idx] > delta_y[idx+1]):
        idx += 1

    right = min(idx - left + idx, n)

    if right - left < th_t:
        return find_valley, ids, stroke

    if right - left > 15 and right == n:
        right -= th_t

    right_bound = min(right+shift, y.shape[0])
    ids = np.arange(left+shift, right_bound, 1)
    stroke = y[ids]
    find_valley = True

    return find_valley, ids, stroke
