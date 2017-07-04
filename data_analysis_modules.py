import csv
import numpy as np
import json
import math
import os, sys
import itertools
import dateutil
import datetime
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, bode, freqz
import scipy
from math import radians, cos, sin, asin, sqrt

import data_parsing_modules as DPM
import single_workout_plot as SWP
#import grade_search_modules as GSM


sys.path.append('/Users/Scott/git_repositories/stamina_lib/lib_py_API/src/')
import stamina_api as ex

def speed_mps_kmph_calculation(w_t, R_dist_m):
    alpha = 0.999
    mv_delta_t = 0
    mv_delta_dist_m = 0
    speed_mps_list = [0]
    speed_kmph_list = [0]

    for i in range(1,len(w_t),1):
        mv_delta_dist_m = mv_delta_dist_m * alpha + float(R_dist_m[i] - R_dist_m[i-1]) * (1-alpha)
        mv_delta_t = mv_delta_t * alpha + float(w_t[i] - w_t[i-1]) * (1-alpha)
        if mv_delta_t == 0:
            speed_mps = 0
        else:
            speed_mps = mv_delta_dist_m / mv_delta_t
        speed_mps_list += [speed_mps]
        speed_kmph_list += [speed_mps * 3.6]

    assert len(speed_kmph_list) == len(w_t)

    return speed_mps_list, speed_kmph_list





















