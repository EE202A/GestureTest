from global_var_config import calc_ranging_threshold


def calc_ranging(times):
    light_speed = 299792458
    times = times / 63.8976 / 1e9
    rnd0 = times[:, 3] - times[:, 0]
    rnd1 = times[:, 5] - times[:, 2]
    rsp0 = times[:, 2] - times[:, 1]
    rsp1 = times[:, 4] - times[:, 3]
    sum_r = rnd0 + rnd1 + rsp0 + rsp1
    r = light_speed * (rnd0 * rnd1 - rsp0 * rsp1) / sum_r
    mask = (r < calc_ranging_threshold)

    return r, mask
