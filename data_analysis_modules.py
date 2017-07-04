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

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def get_total_distance_km(R_lat, R_lng):

    dist_km = 0
    for i in range(1,len(R_lat),1):
        dist_km += haversine(R_lng[i-1], R_lat[i-1], R_lng[i], R_lat[i])

    return dist_km


def add_one_row_csv_column(csv_path, key_list, value_list):
    # read csv file
    assert len(key_list) == len(value_list)

    f = open(csv_path, 'rU')
    row_idx = 0
    for row in csv.reader(f):
        if row_idx == 0:
            csv_header = row
        if row_idx == 1:
            anlysis_result = row
        row_idx += 1

    for i in range(len(key_list)): 
        csv_header.append(key_list[i])
        value_str = str(value_list[i])
        anlysis_result.append(value_str)

    with open(csv_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        writer.writerow(anlysis_result)
        csvfile.close()

def data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng):

    # data padding
    w_t_padding = []
    w_hr_padding = []
    R_alt_m_padding = []
    R_dist_m_padding = []
    R_dist_km_padding = []
    R_speed_mps_padding = []
    R_speed_kmph_padding = []
    R_incline_padding = []
    R_lat_padding = []
    R_lng_padding = []

    for i in range(len(w_t)):
        if len(w_t_padding) == 0:
            #print("[len(w_t_padding) == 0]")
            w_t_padding += [w_t[i]]
            w_hr_padding += [w_hr[i]]
            R_alt_m_padding += [R_alt_m[i]]
            R_dist_m_padding += [R_dist_m[i]]
            R_dist_km_padding += [R_dist_km[i]]
            R_speed_mps_padding += [R_speed_mps[i]]
            R_speed_kmph_padding += [R_speed_kmph[i]]
            R_incline_padding += [R_incline[i]]
            R_lat_padding += [R_lat[i]]
            R_lng_padding += [R_lng[i]]
        elif len(w_t_padding) > 0:
            #print("w_t[i]:{}".format(w_t[i]))
            #print("w_t_padding[-1]:{}".format(w_t_padding[-1]))
            if w_t[i] - w_t_padding[-1] > 1:
                padding_len = w_t[i] - w_t_padding[-1] - 1
                #print("padding_len:{}".format(padding_len))
                for j in range(padding_len):
                    w_t_padding += [w_t_padding[-1]+1]
                    w_hr_padding += [w_hr_padding[-1]]
                    R_alt_m_padding += [R_alt_m_padding[-1]]
                    R_dist_m_padding += [R_dist_m_padding[-1]]
                    R_dist_km_padding += [R_dist_km_padding[-1]]
                    R_speed_mps_padding += [R_speed_mps_padding[-1]]
                    R_speed_kmph_padding += [R_speed_kmph_padding[-1]]
                    R_incline_padding += [R_incline_padding[-1]]
                    R_lat_padding += [R_lat_padding[-1]]
                    R_lng_padding += [R_lng_padding[-1]]
                w_t_padding += [w_t[i]]
                w_hr_padding += [w_hr[i]]
                R_alt_m_padding += [R_alt_m[i]]
                R_dist_m_padding += [R_dist_m[i]]
                R_dist_km_padding += [R_dist_km[i]]
                R_speed_mps_padding += [R_speed_mps[i]]
                R_speed_kmph_padding += [R_speed_kmph[i]]
                R_incline_padding += [R_incline[i]]
                R_lat_padding += [R_lat[i]]
                R_lng_padding += [R_lng[i]]
            elif w_t[i] - w_t_padding[-1] == 1:
                w_t_padding += [w_t[i]]
                w_hr_padding += [w_hr[i]]
                R_alt_m_padding += [R_alt_m[i]]
                R_dist_m_padding += [R_dist_m[i]]
                R_dist_km_padding += [R_dist_km[i]]
                R_speed_mps_padding += [R_speed_mps[i]]
                R_speed_kmph_padding += [R_speed_kmph[i]]
                R_incline_padding += [R_incline[i]]
                R_lat_padding += [R_lat[i]]
                R_lng_padding += [R_lng[i]]
    #print("w_t:{}".format(w_t))
    #print("w_t_padding:{}".format(w_t_padding))
    #print("w_hr:{}".format(w_hr))
    #print("w_hr_padding:{}".format(w_hr_padding))
    #print("len(w_t_padding):{}".format(len(w_t_padding)))
    w_t = w_t_padding
    w_hr = w_hr_padding
    R_alt_m = R_alt_m_padding
    R_dist_m = R_dist_m_padding
    R_dist_km = R_dist_km_padding 
    R_speed_mps = R_speed_mps_padding
    R_speed_kmph = R_speed_kmph_padding
    R_incline = R_incline_padding
    R_lat = R_lat_padding
    R_lng = R_lng_padding
    #print("len(w_hr):{}".format(len(w_hr)))
    #print("max(w_hr):{}".format(max(w_hr)))

    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng

def get_VDOT_from_speed_and_time(time_sec, speed_kmph):
    v_m_per_min = speed_kmph * 1000 / 60
    time_min = float(time_sec)/60.0

    F_VO2_max = (0.8 +  # unit %
                 0.2989558 * math.e**(-0.1932605 * time_min) +
                 0.1894393 * math.e**(-0.012778 * time_min))
    VO2 = (0.000104 * v_m_per_min**2 +  # unit (ml/min/kg)
           0.182258 * v_m_per_min -
           4.6)
    VDOT = VO2 / F_VO2_max

    return VDOT


def i_adj(vdot):
    i_adj = 1+ 0.08 * (50.0 - vdot)/10.0
    if i_adj < 1.0:
        i_adj = 1.0
    #i_adj = 1.0 # test only
    return i_adj

def get_effect_secs(hrr, FVO2):
    
    
    #effect_th_adjust = 0.98 # normalize training effect to 100%
    effect_th_adjust = 1.0

    effect_secs = 0
    if hrr > FVO2 * effect_th_adjust:
        effect_secs = 1
    elif FVO2 >= 0.99 and hrr >= 0.99:
        effect_secs = 1

    return effect_secs

def get_kcal_per_sec_by_VO2Max_ptc(age, gender, weight, bio_max_hr, bio_rest_hr, VO2Max_ptc, VO2Max):
    age = float(age)
    gender = float(gender)
    weight = float(weight)
    
    #print("VO2Max_ptc:{}".format(VO2Max_ptc))
    #print("bio_max_hr:{}".format(bio_max_hr))
    #print("bio_rest_hr:{}".format(bio_rest_hr))

    #hr_target = float(VO2Max_ptc)/100.0 * float(bio_max_hr)
    hr_target = float(VO2Max_ptc)/100.0 * float(bio_max_hr - bio_rest_hr) + float(bio_rest_hr)
    #hr_target = int(hr_target)
    #print("hr_target:{}".format(hr_target))
    # get one sec total kcal
    
    if gender == 1:
        delta_kcal = (
                        (#0.6340 * hr_target +
                         0.5000 * hr_target +
                         
                         #0.4040 * VO2Max +
                         #0.5040 * VO2Max + # adjust for making sure cmd dist >= target dist
                         0.5040 * VO2Max +
                         0.0100 * VO2Max**1.9 + 
                         
                         0.3940 * weight +
                         0.2710 * age - 95.7735) / 60.0
                     ) * 0.239
    else:
        delta_kcal = (
                        (#0.4500 * hr_target +
                         0.4400 * hr_target +

                         #0.3800 * VO2Max +
                         0.3800 * VO2Max +
                         0.0100 * VO2Max**1.9 + 

                         0.1030 * weight +
                         0.2740  * age - 59.3954) / 60.0
                     ) * 0.239
    
    kcal_one_sec = delta_kcal
    
    return kcal_one_sec

def fc(i_rate):
    fc_rate = 0.6422*i_rate**2 + 0.2999*i_rate + 0.003
    #print("fc_rate:{}".format(fc_rate))
    return fc_rate

def get_hrr_by_aero_total_capacity(end_aero_total_capacity, age, gender, weight, MaxHR_user, RestHR_user, time_min, vdot_full_marathon):
    
    age = float(age)
    gender = float(gender)
    weight = float(weight)

    time_sec = float(time_min) * 60.0
    the_carb_kcal_per_sec = end_aero_total_capacity / time_sec

    the_hrr_ptc = -1
    '''
    for hrr_ptc in np.arange(60.0, 90.0, 1.0):
        kcal_per_sec = get_kcal_per_sec_by_VO2Max_ptc(age, gender, weight, MaxHR_user, RestHR_user, hrr_ptc, vdot_full_marathon)
        carb_kcal_per_sec = kcal_per_sec * fc(hrr_ptc / 100.0)
        if carb_kcal_per_sec <= the_carb_kcal_per_sec:
            the_hrr_ptc = hrr_ptc
    '''

    #print("[get_hrr_by_aero_total_capacity] gender:{}".format(gender))
    if gender == 1:

        A = (
             0.5000 * float(MaxHR_user - RestHR_user)
            ) / 60.0 * 0.239
        B = (
             0.5000 * float(RestHR_user) + 
             0.5040 * vdot_full_marathon +
             0.0100 * vdot_full_marathon**1.9 + 
             0.3940 * weight +
             0.2710 * age - 95.7735
            ) / 60.0 * 0.239

        P_0 = B * 0.0030 - the_carb_kcal_per_sec
        P_1 = A * 0.0030 + B * 0.2990
        P_2 = A * 0.2990 + B * 0.6422
        P_3 = A * 0.6422
        roots = np.roots([P_3, P_2, P_1, P_0])
        the_root = 0
        for root in roots:
            if not np.iscomplex(root) and root > the_root:
                the_root = root
        #print("roots:{}".format(roots))    
    else:
        A = (
             0.4400 * float(MaxHR_user - RestHR_user)
            ) / 60.0 * 0.239
        B = (
             0.4400 * float(RestHR_user) + 
             0.3800 * vdot_full_marathon +
             0.0100 * vdot_full_marathon**1.9 + 
             0.1030 * weight +
             0.2740 * age - 59.3954
            ) / 60.0 * 0.239

        P_0 = B * 0.0030 - the_carb_kcal_per_sec
        P_1 = A * 0.0030 + B * 0.2990
        P_2 = A * 0.2990 + B * 0.6422
        P_3 = A * 0.6422
        roots = np.roots([P_3, P_2, P_1, P_0])
        the_root = 0
        for root in roots:
            if not np.iscomplex(root) and root > the_root:
                the_root = root
        #print("roots:0")
    the_hrr_ptc = the_root * 100.0
    
    if np.iscomplex(the_root):
        print("time_min:{}, roots:{}, the_root:{}".format(time_min, roots, the_root))
        assert not np.iscomplex(the_root) 
    the_hrr_ptc = float(the_hrr_ptc.real)

    if the_hrr_ptc > 90:
        the_hrr_ptc = 90

    #print("the_hrr_ptc:{}".format(the_hrr_ptc))
    return the_hrr_ptc



def get_total_sec_with_VDOT_for_speed(speed_kmph, vdot_3km, vdot_5km, vdot_10km, vdot_15km, vdot_half_marathon, vdot_25km, vdot_30km, vdot_35km, vdot_full_marathon, end_aero_total_capacity, age, gender, weight, MaxHR_user, RestHR_user, init_aero_total_capacity_fix, init_aero_capacity_fix):

    #print("end_aero_total_capacity:{}, age:{}, gender:{}, weight:{}, MaxHR_user:{}, RestHR_user:{}".format(end_aero_total_capacity, age, gender, weight, MaxHR_user, RestHR_user))

    time_min_list = np.append(
                              np.arange(30*1 , 15*1, -0.2),
                              np.arange(15*1 ,    1, -0.1)
                             )
    time_min_list = np.append(
                              np.arange(60*1 , 30*1, -0.5),
                              time_min_list
                             )
    time_min_list = np.append(
                              np.arange(60*5 , 60*1, -1.0),
                              time_min_list
                             )
    time_min_list = np.append(
                              np.arange(60*10 , 60*5, -5.0),
                              time_min_list
                             )
    #print("time_min_list:{}".format(time_min_list))

    '''
    test_list = np.append(
                          [1,2],
                          [3,4],
                          [5,6]
                         )
    print("test_list:{}".format(test_list))
    '''

    total_min = 0
    the_F_VO2_max = 0
    the_use_aero_capacity_bundary = 0
    for time_min in time_min_list:
        
        v_m_per_min = speed_kmph * 1000.0 / 60.0

        target_dist_km = v_m_per_min * time_min / 1000.0
        
        F_VO2_max = (0.8 +  # unit %
                     0.2989558 * math.e**(-0.1932605 * time_min) +
                     0.1894393 * math.e**(-0.012778 * time_min))
        
        # try to add leg model into F_VO2_max fix!
        '''
        if F_VO2_max < 0.81:
            hrr_ptc_max = get_hrr_by_aero_total_capacity(end_aero_total_capacity, age, gender, weight, MaxHR_user, RestHR_user, time_min, vdot_full_marathon)
            if (hrr_ptc_max != -1 and 
                hrr_ptc_max < 80 and
                F_VO2_max > hrr_ptc_max/100.0):
                F_VO2_max = hrr_ptc_max/100.0
        '''
        hrr_ptc_max = get_hrr_by_aero_total_capacity(end_aero_total_capacity, age, gender, weight, MaxHR_user, RestHR_user, time_min, vdot_full_marathon)

        if (hrr_ptc_max != -1 and
            hrr_ptc_max < 89 and 
            F_VO2_max > hrr_ptc_max/100.0):
            F_VO2_max = hrr_ptc_max/100.0
            use_aero_capacity_bundary = 1
        else:
            use_aero_capacity_bundary = 0
        

        VO2 = (0.000104 * v_m_per_min**2 +  # unit (ml/min/kg)
               0.182258 * v_m_per_min -
               4.6)
        
        VDOT = VO2 / F_VO2_max
        
        # VDOT_user selection
        if target_dist_km <= 3.0:
            VDOT_user = vdot_3km
        elif target_dist_km <= 5.0: # 3~5
            VDOT_user = vdot_3km + (target_dist_km - 3.0)/(5.0 - 3.0) * (vdot_5km - vdot_3km)
        elif target_dist_km <= 10.0: # 5~10
            VDOT_user = vdot_5km + (target_dist_km - 5.0)/(10.0 - 5.0) * (vdot_10km - vdot_5km)
        elif target_dist_km <= 15.0: # 10~15
            VDOT_user = vdot_10km + (target_dist_km - 10.0)/(15.0 - 10.0) * (vdot_15km - vdot_10km)
        elif target_dist_km <= 21.0975: # 15 ~ 21.0975
            VDOT_user = vdot_15km + (target_dist_km - 15.0)/(21.0975 - 15.0) * (vdot_half_marathon - vdot_15km)
        elif target_dist_km <= 25.0: # 21.0575 ~ 25
            VDOT_user = vdot_half_marathon + (target_dist_km - 21.0975)/(25.0 - 21.0975) * (vdot_25km - vdot_half_marathon)
        elif target_dist_km <= 30.0: # 25~30
            VDOT_user = vdot_25km + (target_dist_km - 25.0)/(30.0 - 25.0) * (vdot_30km - vdot_25km)
        elif target_dist_km <= 35.0: # 30~35
            VDOT_user = vdot_30km + (target_dist_km - 30.0)/(35.0 - 30.0) * (vdot_35km - vdot_30km)
        elif target_dist_km <= 42.195: # 35~42.195
            VDOT_user = vdot_35km + (target_dist_km - 35.0)/(42.195 - 35.0) * (vdot_full_marathon - vdot_35km)
        else:
            VDOT_user = vdot_full_marathon

        if (VDOT > VDOT_user):
            total_min = time_min
            the_F_VO2_max = F_VO2_max
            the_use_aero_capacity_bundary = use_aero_capacity_bundary
        #if speed_kmph == 18.25:
        #    print("time_min:{}, VDOT:{}, VDOT_user:{}, F_VO2_max:{}, hrr_ptc_max:{}, total_min:{}, the_F_VO2_max:{}".format(time_min, VDOT, VDOT_user, F_VO2_max, hrr_ptc_max, total_min, the_F_VO2_max))

    if the_F_VO2_max > 0:
        kcal_per_sec = get_kcal_per_sec_by_VO2Max_ptc(age, gender, weight, MaxHR_user, RestHR_user, the_F_VO2_max*100.0, vdot_full_marathon)
        carb_kcal_per_sec = kcal_per_sec * fc(the_F_VO2_max)
        plus_secs = (init_aero_total_capacity_fix - init_aero_capacity_fix) / carb_kcal_per_sec
        #print("init_aero_total_capacity_fix:{}, init_aero_capacity_fix:{}, total_min:{}, the_F_VO2_max:{}".format(init_aero_total_capacity_fix, init_aero_capacity_fix, total_min, the_F_VO2_max))
        #print("speed_kmph:{}, carb_kcal_per_sec:{}, the_use_aero_capacity_bundary:{}, plus_secs:{}".format(speed_kmph, carb_kcal_per_sec, the_use_aero_capacity_bundary, plus_secs))
    else:
        plus_secs = -1

    total_sec = total_min * 60.0
    #print("the_F_VO2_max:{}".format(the_F_VO2_max))
    return total_sec, the_F_VO2_max, VDOT_user, the_use_aero_capacity_bundary, plus_secs



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

def get_max_speed_kmph(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng):

    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)

    speed_mps_list, speed_kmph_list = speed_mps_kmph_calculation(w_t, R_dist_m)

    return max(speed_kmph_list)

def incline_ptc_calculation(R_dist_m, R_alt_m):
    alpha = 0.99
    mv_delta_dist_m = 0
    mv_delta_alt_m = 0
    incline_ptc_list = [0]

    for i in range(1,len(R_dist_m),1):
        mv_delta_dist_m = mv_delta_dist_m * alpha + float(R_dist_m[i] - R_dist_m[i-1]) * (1-alpha) 
        #mv_delta_dist_m = mv_delta_dist_m * alpha
        mv_delta_alt_m = mv_delta_alt_m * alpha + float(R_alt_m[i] - R_alt_m[i-1]) * (1-alpha) 
        #mv_delta_alt_m = mv_delta_alt_m * alpha
        if mv_delta_dist_m <= 0.5: # to avoid unreasonable incline values
            incline_ptc = 0
        else:
            incline_ptc = mv_delta_alt_m / mv_delta_dist_m * 100.0
        incline_ptc_list += [incline_ptc]
        #print("i:{}, R_dist_m[i]:{}, R_alt_m[i]:{}".format(i, R_dist_m[i], R_alt_m[i]))
        #print("mv_delta_dist_m:{}, mv_delta_alt_m:{}, incline_ptc:{}".format(mv_delta_dist_m, mv_delta_alt_m, incline_ptc))

    assert len(R_dist_m) == len(incline_ptc_list)

    return incline_ptc_list



def cardio_training_effect_analysis(workout_dir, MaxHR_user, RestHR_user, target_dist_km, target_finish_time_sec, end_aero_total_capacity, age, gender, weight, init_aero_total_capacity_fix, init_aero_capacity_fix):
    calculation_statistics_path = workout_dir + 'calculation_statistics.csv'
    raw_data_path = workout_dir + 'raw_data.csv'
    raw_data_info_path = workout_dir + 'raw_data_info.csv'


    VDOT_target = get_VDOT_from_speed_and_time(target_finish_time_sec, target_dist_km / (target_finish_time_sec/3600.0))

    MaxHR_user = float(MaxHR_user)
    RestHR_user = float(RestHR_user)

    if RestHR_user == -1:
        RestHR_user = 71
        print("    [cardio_training_effect_analysis] no default rest HR")

    vdot_3km, vdot_5km, vdot_10km, vdot_15km, vdot_half_marathon, vdot_25km, vdot_30km, vdot_35km, vdot_full_marathon, vdot_CP8, vdot_CP20, vdot_CP60, vdot_CP120, vdot_CP180 = DPM.calculation_statistics_parsing(calculation_statistics_path)

    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = DPM.raw_data_parsing(raw_data_path)

    workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude = DPM.raw_data_info_parsing(raw_data_info_path)

    # data padding
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)
  
    R_speed_mps, R_speed_kmph = speed_mps_kmph_calculation(w_t, R_dist_m)



    if len(w_t) >=2 and vdot_3km != -1:

        speed_step = 0.25
        min_speed_kmph = 6.0
        max_speec_kmph = 20.0
        speed_kmph_list = np.arange(min_speed_kmph, max_speec_kmph, speed_step)
        Cardio_training_effect_ptc = []
        total_sec_list = []
        total_hour_list = []
        effect_sec_list = []
        FVO2_list = []
        FVO2_original_list = []
        speed_kmph_ptc_list = []
        training_load = 0

        E_speed_kmph = -1
        M_speed_kmph = -1
        T_speed_kmph = -1
        I_speed_kmph = -1
        H_speed_kmph = -1

        E_FVO2 = 0.59 / i_adj(vdot_CP180)
        M_FVO2 = 0.75 / i_adj(vdot_full_marathon)
        T_FVO2 = 0.83 / i_adj(vdot_CP60)
        I_FVO2 = 0.95 / i_adj(vdot_3km)
        H_FVO2 = 1.00

        speed_effect_sec_list = []
        time_limit_sec_for_effect_list = []

        for speed_kmph in speed_kmph_list:
            total_sec, FVO2, VDOT_user, the_use_aero_capacity_bundary, plus_secs = get_total_sec_with_VDOT_for_speed(speed_kmph, vdot_3km, vdot_5km, vdot_10km, vdot_15km, vdot_half_marathon, vdot_25km, vdot_30km, vdot_35km, vdot_full_marathon, end_aero_total_capacity, age, gender, weight, MaxHR_user, RestHR_user, init_aero_total_capacity_fix, init_aero_capacity_fix)
            #print("speed_kmph:{}, total_sec:{}, FVO2:{}, VDOT_user:{}, the_use_aero_capacity_bundary:{}, plus_secs:{}".format(speed_kmph, total_sec, FVO2, VDOT_user, the_use_aero_capacity_bundary, plus_secs))
            speed_CP_total_sec = total_sec
            FVO2_original_list += [FVO2]
            FVO2 = FVO2 / i_adj(VDOT_user)
            FVO2_list += [FVO2]
            #print("speed_kmph:{}, total_sec:{}, FVO2:{}".format(speed_kmph, total_sec, FVO2))

            # speed to zone search
            if FVO2 < E_FVO2:
                E_speed_kmph = speed_kmph
            if FVO2 < M_FVO2:
                M_speed_kmph = speed_kmph
            if FVO2 < T_FVO2:
                T_speed_kmph = speed_kmph
            if FVO2 < I_FVO2:
                I_speed_kmph = speed_kmph
            if FVO2 <= H_FVO2:
                H_speed_kmph = speed_kmph

            time_to_VO2_ready = 60 * 3
            if total_sec - time_to_VO2_ready > 0:
                total_sec = total_sec - time_to_VO2_ready
            else:
                total_sec = -1

            effect_secs = 0
            speed_in_range_secs = 0

            #print("MaxHR_user:{}, RestHR_user:{}".format(MaxHR_user, RestHR_user))
            for t in range(len(w_hr)):
                hrr = (w_hr[t] - RestHR_user) / (MaxHR_user - RestHR_user)
                #print("FVO2:{}, hrr:{}".format(FVO2, hrr))

                this_effect_secs = get_effect_secs(hrr, FVO2)
                effect_secs += this_effect_secs
                #print("t:{}, w_hr[t]:{}, hrr:{}, FVO2:{}, this_effect_secs:{}, speed_kmph:{}".format(t, w_hr[t], hrr, FVO2, this_effect_secs, speed_kmph))

                if R_speed_mps[t] * 3.6 >= speed_kmph and R_speed_mps[t] * 3.6 < speed_kmph + speed_step:
                    speed_in_range_secs += 1

            if speed_CP_total_sec <= 0:
                speed_effect_ptc = -1
                speed_effect_sec_list += [-1]
                time_limit_sec_for_effect_list += [-1]
            else:
                speed_effect_secs = 0
                for t in range(len(R_speed_kmph)):
                    if R_speed_kmph[t] >= speed_kmph:
                        speed_effect_secs += 1
                speed_effect_sec_list += [speed_effect_secs]
                time_limit_sec_for_effect = speed_CP_total_sec * 4.2*(float(speed_CP_total_sec)/60.0)**-0.35
                time_limit_sec_for_effect_list += [time_limit_sec_for_effect]
                # fitting by 
                # CP_min = [0.2, 0.5, 10, 20, 60, 180]
                # weight = [  8,   6,1.7,1.3,  1,0.78]
                #print("speed_kmph:{}, speed_CP_total_sec:{}, time_limit_sec_for_effect:{}, speed_effect_secs:{}".format(speed_kmph, speed_CP_total_sec, time_limit_sec_for_effect, speed_effect_secs))
                
                if the_use_aero_capacity_bundary == 1:
                    speed_effect_ptc = (float(speed_effect_secs)+float(plus_secs))/ float(time_limit_sec_for_effect) * 100.0
                else:
                    speed_effect_ptc = float(speed_effect_secs) / float(time_limit_sec_for_effect) * 100.0
                #speed_effect_ptc = float(speed_effect_secs) / float(time_limit_sec_for_effect) * 100.0


            total_sec_list += [speed_CP_total_sec]
            total_hour_list += [float(speed_CP_total_sec)/3600.0]
            effect_sec_list += [effect_secs]
            speed_kmph_ptc_list += [float(speed_in_range_secs) / float(w_t[-1]) * 100.0]
            if total_sec <= 0:
                Cardio_training_effect_ptc += [-1]
            else:
                effect_ptc = effect_secs / total_sec * 100.0

                # compare effect_ptc and speed_effect_ptc
                # print("speed_effect_ptc:{}, effect_ptc:{}".format(speed_effect_ptc, effect_ptc))
                effect_ptc = max(speed_effect_ptc, effect_ptc)
                if effect_ptc >= 200.0: # not a reasonable value
                    effect_ptc = -1
                    effect_secs = -1

                Cardio_training_effect_ptc += [effect_ptc]
                training_load += effect_secs

            #print("speed_kmph:{}, training_load:{}, Cardio_training_effect_ptc:{}".format(speed_kmph, training_load, Cardio_training_effect_ptc))

            #print("E_speed_kmph:{}, E_FVO2:{}".format(E_speed_kmph, E_FVO2))
            #print("M_speed_kmph:{}, M_FVO2:{}".format(M_speed_kmph, M_FVO2))
            #print("T_speed_kmph:{}, T_FVO2:{}".format(T_speed_kmph, T_FVO2))
            #print("I_speed_kmph:{}, I_FVO2:{}".format(I_speed_kmph, I_FVO2))
            #print("H_speed_kmph:{}, H_FVO2:{}".format(H_speed_kmph, H_FVO2))

        # dump calculation results
        cardio_training_effect_results_path = workout_dir + 'cardio_training_effect_results.csv'

        csv_header = []
        csv_header += ["speed_kmph_list"]
        csv_header += ["Cardio_training_effect_ptc"]
        csv_header += ["speed_kmph_ptc_list"]
        csv_header += ["effect_sec_list"]
        csv_header += ["speed_effect_sec_list"]
        csv_header += ["time_limit_sec_for_effect_list"]
        csv_header += ["FVO2_list"]
        csv_header += ["total_sec_list"]
        csv_header += ["total_hour_list"]
                
        with open(cardio_training_effect_results_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in range(len(speed_kmph_list)+1):
                data = []
                if row == 0:
                    data = csv_header
                else:
                    for col in range(len(csv_header)):
                        data += [eval(csv_header[col])[row-1]]
                writer.writerow(data)
            csvfile.close()

        cardio_training_pace_results_path = workout_dir + 'cardio_training_pace_results.csv'

        csv_header = []
        csv_header += ["E_speed_kmph"]
        csv_header += ["M_speed_kmph"]
        csv_header += ["T_speed_kmph"]
        csv_header += ["I_speed_kmph"]
        csv_header += ["H_speed_kmph"]

        with open(cardio_training_pace_results_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_header)
            anlysis_result = []
            for col in range(len(csv_header)):
                anlysis_result += [eval(csv_header[col])]
            writer.writerow(anlysis_result)
            csvfile.close()


        # add plots
        plot_dir = workout_dir
        if has_heartrate == 1 and vdot_3km != -1:

            fig = SWP.get_fig_cardio_training_effect_distribution(speed_kmph_list, Cardio_training_effect_ptc, speed_kmph_ptc_list, E_speed_kmph,M_speed_kmph,T_speed_kmph,I_speed_kmph,H_speed_kmph)
            fig.savefig(plot_dir + 'cardio_training_effect_distribution.png')
            plt.close(fig)

            fig = SWP.get_fig_cardio_training_effect_on_CP_curve(total_hour_list, speed_kmph_list, Cardio_training_effect_ptc, speed_kmph_ptc_list, E_speed_kmph,M_speed_kmph,T_speed_kmph,I_speed_kmph,H_speed_kmph, target_dist_km, target_finish_time_sec)
            fig.savefig(plot_dir + 'cardio_training_effect_CP_curve.png')
            plt.close(fig)

            fig = SWP.get_fig_vdot_curve_vs_target(vdot_3km, vdot_5km, vdot_10km, vdot_15km, vdot_half_marathon, vdot_25km, vdot_30km, vdot_35km, vdot_full_marathon, target_dist_km, VDOT_target)
            fig.savefig(plot_dir + 'vdot_dist_curve_vs_target.png')
            plt.close(fig)






        

def run_stamina_level_analysis(workout_dir,
                               rec_vdot_list,
                               vdot_valid_tag_list,
                               vdot_max_dist_km_list,
                               rec_max_dist_km_list,
                               rec_dist_km_list,
                               rec_epoch_sec_list,
                               rec_vdot_from_workout_dir_list):
    calculation_statistics_path = workout_dir + 'calculation_statistics.csv'
    print("    [stamina_level block] input data length:{}".format(len(rec_vdot_list)))

    runner = ex.User()
    for i in range(len(rec_vdot_list)):
        #print("-----[input]------ rec_vdot_from_workout_dir_list:{}".format(rec_vdot_from_workout_dir_list[i]))
        print("-----[input]------ rec_vdot_from_workout_dir_list:{}, rec_vdot_list:{}, vdot_valid_tag_list:{}, vdot_max_dist_km_list:{}, rec_max_dist_km_list:{}, rec_dist_km_list:{}, rec_epoch_sec_list:{}".format(rec_vdot_from_workout_dir_list[i], rec_vdot_list[i], vdot_valid_tag_list[i], vdot_max_dist_km_list[i], rec_max_dist_km_list[i], rec_dist_km_list[i], rec_epoch_sec_list[i]))
        runner.update_user_record_for_best_running_time_calc(rec_vdot_list[i],
                                                             vdot_valid_tag_list[i],
                                                             vdot_max_dist_km_list[i],
                                                             rec_max_dist_km_list[i],
                                                             rec_dist_km_list[i],
                                                             rec_epoch_sec_list[i])
    vdot_3km = runner.get_user_best_running_vdot_3km()
    vdot_2mile = runner.get_user_best_running_vdot_2mile()
    vdot_5km = runner.get_user_best_running_vdot_5km()
    vdot_10km = runner.get_user_best_running_vdot_10km()
    vdot_15km = runner.get_user_best_running_vdot_15km()
    vdot_half_marathon = runner.get_user_best_running_vdot_half_marathon()
    vdot_25km = runner.get_user_best_running_vdot_25km()
    vdot_30km = runner.get_user_best_running_vdot_30km()
    vdot_35km = runner.get_user_best_running_vdot_35km()
    vdot_full_marathon = runner.get_user_best_running_vdot_full_marathon()
    vdot_CP8 = runner.get_user_best_running_vdot_CP8()
    vdot_CP60 = runner.get_user_best_running_vdot_CP60()
    vdot_CP180 = runner.get_user_best_running_vdot_CP180()
    vdot_CP20 = runner.get_user_best_running_vdot_CP20()
    vdot_CP120 = runner.get_user_best_running_vdot_CP120()

    add_one_row_csv_column(calculation_statistics_path, 
        ['vdot_3km','vdot_2mile','vdot_5km','vdot_10km','vdot_15km','vdot_half_marathon','vdot_25km','vdot_30km','vdot_35km','vdot_full_marathon','vdot_CP8','vdot_CP60','vdot_CP180','vdot_CP20','vdot_CP120'], 
        [vdot_3km,vdot_2mile,vdot_5km,vdot_10km,vdot_15km,vdot_half_marathon,vdot_25km,vdot_30km,vdot_35km,vdot_full_marathon,vdot_CP8,vdot_CP60,vdot_CP180,vdot_CP20,vdot_CP120])
    return vdot_3km,vdot_2mile,vdot_5km,vdot_10km,vdot_15km,vdot_half_marathon,vdot_25km,vdot_30km,vdot_35km,vdot_full_marathon,vdot_CP8,vdot_CP60,vdot_CP180,vdot_CP20,vdot_CP120

def recovery_calculation(recovery_secs,
                         age, 
                         gender,
                         weight,
                         height, 
                         max_HR,
                         rest_HR,
                         aero_total_capacity,
                         aero_capacity,
                         LA_dilution_grade,
                         anaerobic_ptc,
                         stamina_level):
    #print("recovery_secs:{}".format(recovery_secs))
    #print("age:{}".format(age))
    #print("gender:{}".format(gender))
    #print("weight:{}".format(weight))
    #print("height:{}".format(height))
    #print("max_HR:{}".format(max_HR))
    #print("rest_HR:{}".format(rest_HR))
    #print("aero_total_capacity:{}".format(aero_total_capacity))
    #print("aero_capacity:{}".format(aero_capacity))
    #print("LA_dilution_grade:{}".format(LA_dilution_grade))
    #print("anaerobic_ptc:{}".format(anaerobic_ptc))
    #print("stamina_level:{}".format(stamina_level))

    
    runner = ex.User.new_with(int(age), 
                              int(gender),
                              int(weight),
                              int(height), 
                              int(max_HR),
                              31,
                              int(rest_HR),
                              -1,
                              -1,
                              -1,
                              -1,
                              -1,
                              float(aero_total_capacity),
                              float(aero_capacity),
                              int(LA_dilution_grade),
                              float(anaerobic_ptc),
                              float(stamina_level))
    aero_capacity = runner.get_user_aero_capacity_from_status(recovery_secs)
    anaerobic_ptc = runner.get_user_anaerobic_ptc_from_status(recovery_secs)
    full_recovery_sec = runner.get_user_full_recovery_secs_from_status(0)

    runner.user_delete()
    del runner

    print("    [Recovery Block]full_recovery_sec:{}".format(full_recovery_sec))
    print("    [Recovery Block] --After recovery--")
    print("    [Recovery Block]aero_total_capacity:{}".format(aero_total_capacity))
    print("    [Recovery Block]aero_capacity:{}".format(aero_capacity))
    print("    [Recovery Block]LA_dilution_grade:{}".format(LA_dilution_grade))
    print("    [Recovery Block]anaerobic_ptc:{}".format(anaerobic_ptc))

    return aero_total_capacity, aero_capacity, LA_dilution_grade, anaerobic_ptc

def stamina_c_lib_calculation(enable_calibration, 
                              age, 
                              gender,
                              weight,
                              height, 
                              max_HR,
                              rest_HR,
                              aero_total_capacity,
                              aero_capacity,
                              LA_dilution_grade,
                              anaerobic_ptc,
                              stamina_level,
                              first_time_calibration,
                              w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng,
                              workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude): # only return c lib output. no more py calculation 
    print("    [Stamina CALC Block]aero_total_capacity:{}".format(aero_total_capacity))
    print("    [Stamina CALC Block]aero_capacity:{}".format(aero_capacity))
    print("    [Stamina CALC Block]LA_dilution_grade:{}".format(LA_dilution_grade))
    print("    [Stamina CALC Block]anaerobic_ptc:{}".format(anaerobic_ptc))
    print("    [Stamina CALC Block]stamina_level:{}".format(stamina_level))
    print("    [Stamina CALC Block]first_time_calibration:{}".format(first_time_calibration))

    #print("len(w_t):{}".format(len(w_t)))
    #print("len(w_hr):{}".format(len(w_hr)))

    age = int(age)
    gender = int(gender)
    weight = int(weight)
    height = int(height)
    init_max_HR = int(max_HR)
    init_rest_HR = int(rest_HR)
    init_aero_total_capacity = float(aero_total_capacity)
    init_aero_capacity = float(aero_capacity)
    init_LA_dilution_grade = int(LA_dilution_grade)
    init_anaerobic_ptc = float(anaerobic_ptc)
    init_stamina_level = float(stamina_level)

    # round to digit 2 # apply server's setting
    init_aero_total_capacity = round(init_aero_total_capacity,2)
    init_aero_capacity = round(init_aero_capacity,2)
    init_anaerobic_ptc = round(init_anaerobic_ptc,2)
    init_stamina_level = round(init_stamina_level,2)

    runner = ex.User.new_with(age, 
                              gender,
                              weight,
                              height, 
                              init_max_HR,
                              31,
                              init_rest_HR,
                              -1,
                              -1,
                              -1,
                              -1,
                              -1,
                              init_aero_total_capacity,
                              init_aero_capacity,
                              init_LA_dilution_grade,
                              init_anaerobic_ptc,
                              init_stamina_level)
    runner.start_session()

    # collect data by sec
    stamina_ptc_list = []
    aerobic_ptc_list = []
    anaerobic_ptc_list = []
    total_kcal_list = []
    exercise_kcal_list = []
    BMR_kcal_list = []
    max_burn_kcal_list = []
    max_dist_km_list = []
    instant_vdot_list = []

    # duplicate sec handling
    w_i = 0
    # w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng
    while w_i < len(w_t):
        if (w_i - 1) >= 0 and w_t[w_i-1] == w_t[w_i]:
            del w_t[w_i]
            del w_hr[w_i]
            del R_dist_m[w_i]
            del R_dist_km[w_i]
            del R_speed_mps[w_i]
            del R_speed_kmph[w_i]
            del R_incline[w_i]
            del R_alt_m[w_i]
            del R_lat[w_i]
            del R_lng[w_i]
        else:
            w_i += 1

    # remove time offset at very begining
    offset = w_t[0]
    for t in range(len(w_t)):
        w_t[t] = w_t[t] - offset

    w_i = 0
    #print("max(w_t)+1:{}".format(max(w_t)+1))
    for i in range(max(w_t)+1):
        if i < max(w_t)+1 and i == w_t[w_i]:
            #print("i:{}, w_i:{}, w_t[w_i]:{}".format(i,w_i,w_t[w_i]))

            t = w_t[w_i]
            hr = w_hr[w_i]

            runner.update_new_heartrate(t, hr)

            stamina_ptc_list += [runner.get_user_now_stamina_ptc()]
            aerobic_ptc_list += [runner.get_user_now_aerobic_ptc()]
            anaerobic_ptc_list += [runner.get_user_now_anaerobic_ptc()]
            
            total_kcal_list += [runner.get_user_now_meta_session_total_kcal()]
            exercise_kcal_list += [runner.get_user_now_meta_session_exercise_kcal()]
            BMR_kcal_list += [runner.get_user_now_meta_session_BMR_kcal()]
            max_burn_kcal_list += [runner.get_user_now_predicted_last_pace_max_burn_with_stamina_left()]

            dist_km = R_dist_km[w_i]
            incline_ptc = R_incline[w_i]
            speed_mps = R_speed_mps[w_i]
            speed_kmph = R_speed_kmph[w_i]
            lng = R_lng[w_i]
            lat = R_lat[w_i]
            alt_m = R_alt_m[w_i]

            #print("[t]:{}, dist_km:{}".format(t, dist_km))
            #print("speed_kmph:{}".format(speed_kmph))

            runner.update_new_physic_full(t, 
                                          dist_km, 
                                          speed_kmph, 
                                          31,  # running 
                                          -1, # front_area
                                          incline_ptc, 
                                          -1, # wind_speed_kmph
                                          -1, # air_temp_c
                                          lng, 
                                          lat, 
                                          alt_m, 
                                          -1, # power_watt
                                          -1)  # cadence_rpm
            max_dist_km_list += [runner.get_user_now_predicted_last_pace_max_dist_km_with_stamina_left()]
            instant_vdot_list += [runner.get_user_now_predicted_sudo_VDOT()]
            #print("             max_dist_km_list[-1]:{}".format(max_dist_km_list[-1]))

            # test only
            """
            time_sec_now = runner.get_user_now_heartD_time()
            print("time_sec_now:{}".format(time_sec_now))
            """
            
            w_i += 1

    #print("len(stamina_ptc_list):{}".format(len(stamina_ptc_list)))

    runner.stop_session()

    stamina_ptc_end = stamina_ptc_list[-1]
    aerobic_ptc_end = aerobic_ptc_list[-1]
    anaerobic_ptc_end = anaerobic_ptc_list[-1]
    total_kcal_end = total_kcal_list[-1]
    exercise_kcal_end = exercise_kcal_list[-1]
    BMR_kcal_end = BMR_kcal_list[-1]
    max_burn_kcal_end = max_burn_kcal_list[-1]
    max_dist_km_end = max_dist_km_list[-1]
    aero_total_capacity_end = runner.get_user_now_aero_total_capacity()
    aero_capacity_end = runner.get_user_now_aero_capacity()
    carbon_kcal_end = runner.get_user_now_meta_session_carbon_kcal()
    fat_kcal_end = runner.get_user_now_meta_session_fat_kcal()
       
    print("    [Stamina CALC Block] stamina_ptc_end:{}".format(stamina_ptc_end))
    print("    [Stamina CALC Block] aerobic_ptc_end:{}".format(aerobic_ptc_end))
    print("    [Stamina CALC Block] aero_total_capacity_end:{}".format(aero_total_capacity_end))
    print("    [Stamina CALC Block] aero_capacity_end:{}".format(aero_capacity_end))
    print("    [Stamina CALC Block] anaerobic_ptc_end:{}".format(anaerobic_ptc_end))
    print("    [Stamina CALC Block] total_kcal_end:{}".format(total_kcal_end))
    print("    [Stamina CALC Block] exercise_kcal_end:{}".format(exercise_kcal_end))
    print("    [Stamina CALC Block] BMR_kcal_end:{}".format(BMR_kcal_end))
    print("    [Stamina CALC Block] carbon_kcal_end:{}".format(carbon_kcal_end))
    print("    [Stamina CALC Block] fat_kcal_end:{}".format(fat_kcal_end))
    print("    [Stamina CALC Block] max_burn_kcal_end:{}".format(max_burn_kcal_end))
    print("    [Stamina CALC Block] max_dist_km_end:{}".format(max_dist_km_end))

    #
    if enable_calibration == 1 and answer_breath != -1:
        success_cali = runner.update_aerobic_anaerobic_result_by_question(first_time_calibration, answer_breath, answer_muscle, answer_RPE)
        if success_cali == 1:
            first_time_calibration = 0
            print("        [Stamina CALC Block] [successful calibration] answer_breath:{}, answer_muscle:{}, answer_RPE:{}, first_time_calibration:{}".format(answer_breath, answer_muscle, answer_RPE, first_time_calibration))
        else:
            print("        [Stamina CALC Block] [no calibration] answer_breath:{}, answer_muscle:{}, answer_RPE:{}, first_time_calibration:{}".format(answer_breath, answer_muscle, answer_RPE, first_time_calibration))
    else:
        success_cali = 0
    
    #
    if init_max_HR == -1:
      init_max_HR = runner.get_user_default_max_HR()
    if runner.get_user_session_max_HR() > init_max_HR:
        end_max_HR = runner.get_user_session_max_HR()
        print("        [Stamina CALC Block] [max_HR update] init_max_HR:{}, end_max_HR:{}, runner.get_user_session_max_HR():{}, runner.get_user_default_max_HR():{}".format(init_max_HR, end_max_HR, runner.get_user_session_max_HR(), runner.get_user_default_max_HR()))
    else:
        end_max_HR = init_max_HR
    #end_rest_HR
    end_aero_total_capacity = runner.get_user_now_aero_total_capacity()
    end_aero_capacity = runner.get_user_now_aero_capacity()
    end_LA_dilution_grade = runner.get_user_now_LA_dilution_grade()
    end_anaerobic_ptc = runner.get_user_now_anaerobic_ptc()
    max_delta_aero_capacity = (end_aero_total_capacity - init_aero_total_capacity) + init_aero_capacity

    print("        [Stamina CALC Block] max_delta_aero_capacity:{}".format(max_delta_aero_capacity))
    
    #
    rec_vdot = runner.get_user_session_VDOT()
    vdot_valid_tag = runner.get_user_is_valid_VDOT()
    vdot_max_dist_km = runner.get_user_session_VDOT_max_dist_km()
    rec_max_dist_km = max_dist_km_end
    rec_dist_km = R_dist_km[-1]
    rec_epoch_sec = workout_time_sec

    #init_aero_total_capacity_fix = runner.get_user_now_aero_total_capacity()
    delta_estimate_aero_total_capacity = max_delta_aero_capacity / (init_aero_capacity / init_aero_total_capacity)
    new_aero_total_capacity = runner.get_user_now_aero_total_capacity()
    
    if init_aero_capacity / init_aero_total_capacity <= 0.05: # to avoid over estimation of delta_estimate_aero_total_capacity
        init_aero_total_capacity_fix = new_aero_total_capacity
    else:
        init_aero_total_capacity_fix = max( delta_estimate_aero_total_capacity, new_aero_total_capacity)
    
    print("        [Stamina CALC Block] delta_estimate_aero_total_capacity:{}".format(delta_estimate_aero_total_capacity))
    print("        [Stamina CALC Block] new_aero_total_capacity:{}".format(new_aero_total_capacity))
    init_aero_capacity_fix = init_aero_capacity / init_aero_total_capacity * init_aero_total_capacity_fix
    init_LA_dilution_grade_fix = runner.get_user_now_LA_dilution_grade()
    init_anaerobic_ptc_fix = init_anaerobic_ptc
    print("        [Stamina CALC Block] init_aero_total_capacity_fix:{}".format(init_aero_total_capacity_fix))
    print("        [Stamina CALC Block] init_aero_capacity_fix:{}".format(init_aero_capacity_fix))

    # test only extra info for albert
    session_TRIMP = (
                     runner.get_user_HR_z1_sec_HRR_50_60() * 1 +
                     runner.get_user_HR_z2_sec_HRR_60_70() * 2 +
                     runner.get_user_HR_z3_sec_HRR_70_80() * 3 +
                     runner.get_user_HR_z4_sec_HRR_80_90() * 4 +
                     runner.get_user_HR_z5_sec_HRR_90_up() * 5
                    )
    need_recovery_sec = runner.get_user_full_recovery_secs_from_status(0)

    print("session_TRIMP:{}".format(session_TRIMP))
    print("need_recovery_sec:{}".format(need_recovery_sec))

    runner.user_delete()
    del runner

    if enable_calibration == 1:
        return init_aero_total_capacity_fix, init_aero_capacity_fix, init_LA_dilution_grade_fix, init_anaerobic_ptc_fix, end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, total_kcal_list, exercise_kcal_list, BMR_kcal_list, max_burn_kcal_list, max_dist_km_list, success_cali
    else:
        return end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, total_kcal_list, exercise_kcal_list, BMR_kcal_list, max_burn_kcal_list, max_dist_km_list, rec_vdot, vdot_valid_tag, vdot_max_dist_km, rec_max_dist_km, rec_dist_km, rec_epoch_sec, instant_vdot_list, session_TRIMP, need_recovery_sec

#######################################################
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def get_butter_bandpass_plot(lowcut, highcut, fs, order_list):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for order in order_list:
        B, A = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(B, A, worN=2000)
        ax.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
    w, mag, phase = bode((B, A))
    ax.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain')
    #ax.set_xlim([0,0.1])
    ax.grid(True)
    ax.legend(loc='best')     

    return fig

def get_freq_domain_plot(x, y, sr):

    x = np.array(x)
    y = np.array(y)
    
    yf = scipy.fftpack.fft(y)/len(y)

    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/sr
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    yf_abs = abs(yf[0:len(y)/2])

    # find suitable x lim
    yf_abs_max = max (yf_abs)
    x_lim = 0
    for i in range(len(yf_abs)):
        if yf_abs[i] > (yf_abs_max * 0.01) and frq[i] > x_lim:
            #print("yf_abs_max:{}, yf_abs[i]:{}, frq[i]:{}, x_lim:{}".format(yf_abs_max, yf_abs[i], frq[i], x_lim))
            x_lim = frq[i]
    x_lim = x_lim * 2

    Y_max = max(y)
    if Y_max >= 200:
        Ylim = max(y) * 1.3
    else:
        Ylim = 230

    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(frq,yf_abs)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('|Y(freq)|')
    ax.set_xlim([0, x_lim])
    ax.grid(True)

    ax = fig.add_subplot(212)
    ax.plot(x,y)
    ax.set_xlabel('sec')
    ax.set_ylabel('Amp')
    ax.set_ylim([0, Ylim])
    ax.grid(True)

    return fig

def get_freq_domain_compare_plot(fig, x, y, sr, line_style):

    x = np.array(x)
    y = np.array(y)
    
    yf = scipy.fftpack.fft(y)/len(y)

    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/sr
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    yf_abs = abs(yf[0:len(y)/2])

    # find suitable x lim
    yf_abs_max = max (yf_abs)
    x_lim = 0
    for i in range(len(yf_abs)):
        if yf_abs[i] > (yf_abs_max * 0.01) and frq[i] > x_lim:
            #print("yf_abs_max:{}, yf_abs[i]:{}, frq[i]:{}, x_lim:{}".format(yf_abs_max, yf_abs[i], frq[i], x_lim))
            x_lim = frq[i]
    x_lim = x_lim * 2

    Y_max = max(y)
    if Y_max >= 200:
        Ylim = max(y) * 1.3
    else:
        Ylim = 230

    #fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(frq,yf_abs)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('|Y(freq)|')
    ax.set_xlim([0, x_lim])
    ax.grid(True)

    ax = fig.add_subplot(212)
    ax.plot(x,y)
    ax.set_xlabel('sec')
    ax.set_ylabel('Amp')
    ax.set_ylim([0, Ylim])
    ax.grid(True)

    return fig

def stamina_TRIMP_distribution(w_t, stamina_ptc_list):

    delta_sta_list = [0]
    for i in range(1,len(w_t)):
        delta_sta = stamina_ptc_list[i] - stamina_ptc_list[i-1]
        alpha = 0.1
        delta_sta_list += [delta_sta*alpha + delta_sta_list[-1]*(1-alpha)]


    s1_secs = 0
    s2_secs = 0
    s3_secs = 0
    s4_secs = 0
    s5_secs = 0
    s1_ptc = 0
    s2_ptc = 0
    s3_ptc = 0
    s4_ptc = 0
    s5_ptc = 0
    s1_consume = 0
    s2_consume = 0
    s3_consume = 0
    s4_consume = 0
    s5_consume = 0

    for i in range(len(delta_sta_list)):
        if delta_sta_list[i] <= -0.166: # about 10min
            s5_secs += 1
            s5_consume += (delta_sta_list[i])*-1
        elif delta_sta_list[i] <= -0.083: # about 20min
            s4_secs += 1
            s4_consume += (delta_sta_list[i])*-1
        elif delta_sta_list[i] <= -0.0277: # about 1hr
            s3_secs += 1
            s3_consume += (delta_sta_list[i])*-1
        elif delta_sta_list[i] <= -0.00925: # about 3hr
            s2_secs += 1
            s2_consume += (delta_sta_list[i])*-1
        else:
            s1_secs += 1
            s1_consume += (delta_sta_list[i])*-1

    s1_ptc = float(s1_secs)/(max(w_t)+1) * 100.0
    s2_ptc = float(s2_secs)/(max(w_t)+1) * 100.0
    s3_ptc = float(s3_secs)/(max(w_t)+1) * 100.0
    s4_ptc = float(s4_secs)/(max(w_t)+1) * 100.0
    s5_ptc = float(s5_secs)/(max(w_t)+1) * 100.0

    print("s1_secs:{}".format(s1_secs)) 
    print("s2_secs:{}".format(s2_secs)) 
    print("s3_secs:{}".format(s3_secs)) 
    print("s4_secs:{}".format(s4_secs)) 
    print("s5_secs:{}".format(s5_secs)) 
    print("s1_ptc:{}".format(s1_ptc)) 
    print("s2_ptc:{}".format(s2_ptc)) 
    print("s3_ptc:{}".format(s3_ptc)) 
    print("s4_ptc:{}".format(s4_ptc)) 
    print("s5_ptc:{}".format(s5_ptc)) 
    print("s1_consume:{}".format(s1_consume)) 
    print("s2_consume:{}".format(s2_consume)) 
    print("s3_consume:{}".format(s3_consume)) 
    print("s4_consume:{}".format(s4_consume)) 
    print("s5_consume:{}".format(s5_consume)) 

    return delta_sta_list, s1_secs, s2_secs, s3_secs, s4_secs, s5_secs, s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc, s1_consume, s2_consume, s3_consume, s4_consume, s5_consume


def TRIMP_zone_distribution(max_HR, rest_HR, w_t, w_hr, stamina_ptc_list):
    if rest_HR < 0:
        rest_HR = 71
    z1_trimp = 0
    z2_trimp = 0
    z3_trimp = 0
    z4_trimp = 0
    z5_trimp = 0
    z1_secs = 0
    z2_secs = 0
    z3_secs = 0
    z4_secs = 0
    z5_secs = 0
    z1_ptc = 0
    z2_ptc = 0
    z3_ptc = 0
    z4_ptc = 0
    z5_ptc = 0

    z1_consume = 0
    z2_consume = 0
    z3_consume = 0
    z4_consume = 0
    z5_consume = 0
    delta_sta_list = [0]
    for i in range(1,len(w_t)):
        delta_sta = stamina_ptc_list[i] - stamina_ptc_list[i-1]
        alpha = 0.1
        delta_sta_list += [delta_sta*alpha + delta_sta_list[-1]*(1-alpha)]

    for i in range(len(w_t)):
        hrr_ptc = float(w_hr[i] - rest_HR)/float(max_HR - rest_HR) * 100.0
        if hrr_ptc >= 90.0:
            z5_secs += 1
            z5_trimp += 5
            z5_consume += delta_sta_list[i]*-1
        elif hrr_ptc >= 80.0:
            z4_secs += 1
            z4_trimp += 4
            z4_consume += delta_sta_list[i]*-1
        elif hrr_ptc >= 70.0:
            z3_secs += 1
            z3_trimp += 3
            z3_consume += delta_sta_list[i]*-1
        elif hrr_ptc >= 60.0:
            z2_secs += 1
            z2_trimp += 2
            z2_consume += delta_sta_list[i]*-1
        elif hrr_ptc >= 50.0:
            z1_secs += 1
            z1_trimp += 1
            z1_consume += delta_sta_list[i]*-1
    total_trimp = z1_trimp + z2_trimp + z3_trimp + z4_trimp + z5_trimp
    z1_ptc = float(z1_secs)/(max(w_t)+1) * 100.0
    z2_ptc = float(z2_secs)/(max(w_t)+1) * 100.0
    z3_ptc = float(z3_secs)/(max(w_t)+1) * 100.0
    z4_ptc = float(z4_secs)/(max(w_t)+1) * 100.0
    z5_ptc = float(z5_secs)/(max(w_t)+1) * 100.0

    print("z1_trimp:{}".format(z1_trimp)) 
    print("z2_trimp:{}".format(z2_trimp)) 
    print("z3_trimp:{}".format(z3_trimp)) 
    print("z4_trimp:{}".format(z4_trimp)) 
    print("z5_trimp:{}".format(z5_trimp)) 
    print("z1_secs:{}".format(z1_secs)) 
    print("z2_secs:{}".format(z2_secs)) 
    print("z3_secs:{}".format(z3_secs)) 
    print("z4_secs:{}".format(z4_secs)) 
    print("z5_secs:{}".format(z5_secs)) 
    print("z1_ptc:{}".format(z1_ptc)) 
    print("z2_ptc:{}".format(z2_ptc)) 
    print("z3_ptc:{}".format(z3_ptc)) 
    print("z4_ptc:{}".format(z4_ptc)) 
    print("z5_ptc:{}".format(z5_ptc)) 
    print("z1_consume:{}".format(z1_consume)) 
    print("z2_consume:{}".format(z2_consume)) 
    print("z3_consume:{}".format(z3_consume)) 
    print("z4_consume:{}".format(z4_consume)) 
    print("z5_consume:{}".format(z5_consume)) 

    return total_trimp, z1_trimp, z2_trimp, z3_trimp, z4_trimp, z5_trimp, z1_secs, z2_secs, z3_secs, z4_secs, z5_secs, z1_ptc, z2_ptc, z3_ptc, z4_ptc, z5_ptc, z1_consume, z2_consume, z3_consume, z4_consume, z5_consume

def VO2(speed_kmph):
    v_m_per_min = speed_kmph / 3.6 * 60.0
    vo2 = (0.000104 * v_m_per_min**2 +  # unit (ml/min/kg)
           0.182258 * v_m_per_min -
           4.6)
    return vo2

def get_FVO2_anaerobic_capacity(FCP_rate, time_mins):
    F_VO2_max = (0.8 +  # unit %
                 0.2989558 * math.e**(-0.1932605 * time_mins) +
                 0.1894393 * math.e**(-0.012778 * time_mins))
    anaerobic_capacity = (F_VO2_max - FCP_rate)*time_mins*60.0

    return F_VO2_max, anaerobic_capacity

def anaerobic_consumption_skiba_model(w_t, R_speed_kmph):
    print("[anaerobic_consumption_skiba_model]")
    Wp_list = []
    WpPtc_list = []
    #Wp(VO2)
    #Wp0 = 2200.0
    #Wp0 = 3500.0 # 15kmph 5min VDOT about 43
    Wp0 = 1300.0 # 16kmph 2.25min VDOT about 43
    #Wp0 = 4200.0
    Wp = Wp0
    #CP(VO2)
    CP = VO2(13.5)
    #speed to power calculation

    # test 
    print("CP:{}".format(CP))
    print("VO2(15):{}".format(VO2(15)))
    print("VO2(16):{}".format(VO2(16)))



    for i in range(len(w_t)):
        P = VO2(R_speed_kmph[i])
        if P > CP:
            Wp -= (P - CP)
        else:
            #Wp += (1-Wp/Wp0)*(CP - P)*0.1
            Wp += (1-Wp/Wp0)*(CP - P)*0.4
        Wp_list += [Wp]
        WpPtc_list += [Wp/Wp0*100.0]

    return Wp_list, WpPtc_list




def stamina_analysis(workout_dir):

    print("[Stamina Analysis]")
    print("workout_dir:{}".format(workout_dir))
    calculation_result_path = workout_dir + 'calculation_result.csv'
    user_status_path = workout_dir + 'user_status_before_workout.csv'
    print("calculation_result_path:{}".format(calculation_result_path))
    raw_data_info_path = workout_dir + 'raw_data_info.csv'
    stamina_analysis_dir = workout_dir + 'stamina_analysis/'
    plot_dir = stamina_analysis_dir

    if not os.path.exists(stamina_analysis_dir):   
        os.makedirs(stamina_analysis_dir)

    # load user status
    last_workout_time_sec,last_workout_duration_sec,last_workout_dir,last_anaerobic_ptc,last_aerobic_ptc,last_run_max_HR,last_run_rest_HR,last_run_aero_total_capacity,last_run_LA_dilution_grade,last_run_stamina_level,last_run_first_time_calibration = DPM.user_run_status_parsing(user_status_path)

    # load calculation results
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, max_dist_km_list = DPM.calculation_result_parsing(calculation_result_path)

    workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude = DPM.raw_data_info_parsing(raw_data_info_path)

    total_trimp, z1_trimp, z2_trimp, z3_trimp, z4_trimp, z5_trimp, z1_secs, z2_secs, z3_secs, z4_secs, z5_secs, z1_ptc, z2_ptc, z3_ptc, z4_ptc, z5_ptc, z1_consume, z2_consume, z3_consume, z4_consume, z5_consume = TRIMP_zone_distribution(last_run_max_HR, last_run_rest_HR, w_t, w_hr, stamina_ptc_list)

    delta_sta_list, s1_secs, s2_secs, s3_secs, s4_secs, s5_secs, s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc, s1_consume, s2_consume, s3_consume, s4_consume, s5_consume = stamina_TRIMP_distribution(w_t, stamina_ptc_list)

    Wp_list, WpPtc_list = anaerobic_consumption_skiba_model(w_t, R_speed_kmph)

    fig = SWP.get_fig_time_stamina_WpPtc(w_t, stamina_ptc_list,aerobic_ptc_list, anaerobic_ptc_list, WpPtc_list)
    fig.savefig(plot_dir + 'stamina_WpPtc.png')
    plt.close(fig)

    fig = SWP.get_fig_stamina_trimp_consumption_bars(s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc, s1_consume, s2_consume, s3_consume, s4_consume, s5_consume)
    fig.savefig(plot_dir + 'stamina_trimp_consumption_bars.png')
    plt.close(fig)

    fig = SWP.get_fig_stamina_consumption_bar(s1_consume, s2_consume, s3_consume, s4_consume, s5_consume)
    fig.savefig(plot_dir + 'stamina_consumption_bar.png')
    plt.close(fig)

    fig = SWP.get_fig_stamina_consumption_bar_by_HRR(z1_consume, z2_consume, z3_consume, z4_consume, z5_consume)
    fig.savefig(plot_dir + 'stamina_consumption_bar_by_HRR.png')
    plt.close(fig)

    fig = SWP.get_fig_stamina_trimp_bar(s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc)
    fig.savefig(plot_dir + 'stamina_trimp_bar.png')
    plt.close(fig)
    
    fig = SWP.get_fig_delta_sta_distribution(delta_sta_list)
    fig.savefig(plot_dir + 'delta_sta_distribution.png')
    plt.close(fig)

    fig = SWP.get_fig_trimp_bar(z1_trimp, z2_trimp, z3_trimp, z4_trimp, z5_trimp)
    fig.savefig(plot_dir + 'trimp_distribution.png')
    plt.close(fig)

    fig = SWP.get_fig_time_stamina_alt(w_t,stamina_ptc_list,aerobic_ptc_list,anaerobic_ptc_list,R_alt_m,answer_breath,answer_muscle,answer_RPE,-1,-1,-1)
    fig.savefig(plot_dir + 'stamina_plot_test.png')
    plt.close(fig)

    fig = SWP.get_fig_time_speed_alt(w_t,R_speed_kmph,R_alt_m)
    fig.savefig(plot_dir + 'time_speed_kmph.png')
    plt.close(fig)

    # test
    # test
    '''
    FCP_080_cap_list = []
    FCP_090_cap_list = []
    FCP_095_cap_list = []
    FCP_100_cap_list = []
    for time_mins in np.arange(0.5, 10, 0.5):
        FCP_rate = 0.8
        F_VO2_max, anaerobic_capacity = get_FVO2_anaerobic_capacity(FCP_rate, time_mins)
        FCP_080_cap_list += [anaerobic_capacity]
        #print("FCP_rate:{}, time_mins:{}, F_VO2_max:{}, anaerobic_capacity:{}".format(FCP_rate, time_mins, F_VO2_max, anaerobic_capacity))

    for time_mins in np.arange(0.5, 10, 0.5):
        FCP_rate = 0.9
        F_VO2_max, anaerobic_capacity = get_FVO2_anaerobic_capacity(FCP_rate, time_mins)
        FCP_090_cap_list += [anaerobic_capacity]
        #print("FCP_rate:{}, time_mins:{}, F_VO2_max:{}, anaerobic_capacity:{}".format(FCP_rate, time_mins, F_VO2_max, anaerobic_capacity))

    for time_mins in np.arange(0.5, 10, 0.5):
        FCP_rate = 0.95
        F_VO2_max, anaerobic_capacity = get_FVO2_anaerobic_capacity(FCP_rate, time_mins)
        FCP_095_cap_list += [anaerobic_capacity]
        #print("FCP_rate:{}, time_mins:{}, F_VO2_max:{}, anaerobic_capacity:{}".format(FCP_rate, time_mins, F_VO2_max, anaerobic_capacity))

    for time_mins in np.arange(0.5, 10, 0.5):
        FCP_rate = 1.0
        F_VO2_max, anaerobic_capacity = get_FVO2_anaerobic_capacity(FCP_rate, time_mins)
        FCP_100_cap_list += [anaerobic_capacity]
        #print("FCP_rate:{}, time_mins:{}, F_VO2_max:{}, anaerobic_capacity:{}".format(FCP_rate, time_mins, F_VO2_max, anaerobic_capacity))
    fig = SWP.get_fig_anaerobic_capacity_with_FCP(FCP_080_cap_list, FCP_090_cap_list, FCP_095_cap_list, FCP_100_cap_list)
    fig.savefig(plot_dir + 'anaerobic_capacity_with_FCP.png')
    plt.close(fig)
    '''
    

def HR_filtering(workout_dir):

    print("[HR Filtering]")
    raw_data_path = workout_dir + 'raw_data.csv'
    raw_data_filtering_path = workout_dir + 'raw_data_filtering.csv'
    hr_filtering_dir = workout_dir + 'hr_filtering/'
    plot_dir = hr_filtering_dir

    if not os.path.exists(hr_filtering_dir):   
            os.makedirs(hr_filtering_dir)

    # load raw_data (call module)
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = DPM.raw_data_parsing(raw_data_path)

    # data padding
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)

    fs = 1.0
    #highcut = 1/10.0 # delay about 6 sec
    highcut = 1/25.0 # delay about 13 sec
    #highcut = 1/50.0 # delay about 26 sec
    print("[HR Filtering] highcut:{}".format(highcut))
    w_hr_f = butter_lowpass_filter(w_hr, highcut, fs, order=3)

    w_hr = w_hr_f

    # dump hr filter result 
    csv_header = []
    csv_header += ["w_t"]
    csv_header += ["w_hr"]
    csv_header += ["R_alt_m"]
    csv_header += ["R_dist_m"]
    csv_header += ["R_dist_km"]
    csv_header += ["R_speed_mps"]
    csv_header += ["R_speed_kmph"]
    csv_header += ["R_incline"]
    csv_header += ["R_lat"]
    csv_header += ["R_lng"]
            
    with open(raw_data_filtering_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(w_t)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    if csv_header[col] == 'w_hr':
                        data += [int(eval(csv_header[col])[row-1])]
                    else:
                        data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()


    '''
    fs = 1.0 
    lowcut = 1/300.0
    highcut = 1/10.0
    order_list = [3,5]

    fig = get_butter_bandpass_plot(lowcut, highcut, fs, order_list)
    fig.savefig(plot_dir + 'butter_bandpass_design.png')
    plt.close(fig)

    # freq domain plot
    f1 = 0.5 #Hz
    f2 = 3 #Hz
    sr = 10.0 #sample rate Hz >= 2*f
    x = np.arange(0,100,1/sr)
    #test = np.sin(2*np.pi*f1*x) + np.sin(2*np.pi*f2*x)*0.5
    test = np.sin(2*np.pi*f1*x)
    
    fig = get_freq_domain_plot(x, test, sr)
    fig.savefig(plot_dir + 'freq_plot_test.png')
    plt.close(fig)
    '''
    # signal filtering
    sr = 1.0 #sample rate Hz >= 2*f

    fig = get_freq_domain_plot(w_t, w_hr, sr)
    fig.savefig(plot_dir + 'freq_plot_hr.png')
    plt.close(fig)
    
    highcut = 1/10.0
    w_hr_f = butter_lowpass_filter(w_hr, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t, w_hr_f, sr)
    fig.savefig(plot_dir + 'freq_plot_hr_filtering_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/25.0
    w_hr_f = butter_lowpass_filter(w_hr, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t, w_hr_f, sr)
    fig.savefig(plot_dir + 'freq_plot_hr_filtering_cut_{}.png'.format(highcut))
    plt.close(fig)
    
    highcut = 1/50.0
    w_hr_f = butter_lowpass_filter(w_hr, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t, w_hr_f, sr)
    fig.savefig(plot_dir + 'freq_plot_hr_filtering_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/100.0
    w_hr_f = butter_lowpass_filter(w_hr, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t, w_hr_f, sr)
    fig.savefig(plot_dir + 'freq_plot_hr_filtering_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/200.0
    w_hr_f = butter_lowpass_filter(w_hr, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t, w_hr_f, sr)
    fig.savefig(plot_dir + 'freq_plot_hr_filtering_cut_{}.png'.format(highcut))
    plt.close(fig)


    
    # delay test
    w_test = np.ones(30) * 80
    w_test = np.append(w_test, np.ones(10) * 90)
    w_test = np.append(w_test, np.ones(10) * 80)
    w_test = np.append(w_test, np.ones(10) * 100)
    w_test = np.append(w_test, np.ones(10) * 80)
    w_test = np.append(w_test, np.ones(10) * 120)
    w_test = np.append(w_test, np.ones(10) * 80)
    w_test = np.append(w_test, np.ones(10) * 140)
    w_test = np.append(w_test, np.ones(10) * 80)
    w_t_test = np.arange(0,len(w_test),1)

    highcut = 1/10.0
    w_test_f = butter_lowpass_filter(w_test, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t_test, w_test, sr)
    fig = get_freq_domain_compare_plot(fig, w_t_test, w_test_f, sr, '--')
    fig.savefig(plot_dir + 'freq_plot_delay_test_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/25.0
    w_test_f = butter_lowpass_filter(w_test, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t_test, w_test, sr)
    fig = get_freq_domain_compare_plot(fig, w_t_test, w_test_f, sr, '--')
    fig.savefig(plot_dir + 'freq_plot_delay_test_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/50.0
    w_test_f = butter_lowpass_filter(w_test, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t_test, w_test, sr)
    fig = get_freq_domain_compare_plot(fig, w_t_test, w_test_f, sr, '--')
    fig.savefig(plot_dir + 'freq_plot_delay_test_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/100.0
    w_test_f = butter_lowpass_filter(w_test, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t_test, w_test, sr)
    fig = get_freq_domain_compare_plot(fig, w_t_test, w_test_f, sr, '--')
    fig.savefig(plot_dir + 'freq_plot_delay_test_cut_{}.png'.format(highcut))
    plt.close(fig)

    highcut = 1/200.0
    w_test_f = butter_lowpass_filter(w_test, highcut, fs, order=3)
    fig = get_freq_domain_plot(w_t_test, w_test, sr)
    fig = get_freq_domain_compare_plot(fig, w_t_test, w_test_f, sr, '--')
    fig.savefig(plot_dir + 'freq_plot_delay_test_cut_{}.png'.format(highcut))
    plt.close(fig)
    

#######################################################

def get_delta_hr_plot(x, y_1, y_2, y_3, y_4):



    Y_max = max(y_1)
    if Y_max >= 200:
        Ylim = max(y_1) * 1.3
    else:
        Ylim = 230

    fig = plt.figure()
    ax = fig.add_subplot(411)
    ax.plot(x,y_2)
    ax.set_ylabel('')
    #ax.set_ylim([-0.2, 1.0])
    ax.grid(True)

    ax = fig.add_subplot(412)
    ax.plot(x,y_1)
    ax.set_xlabel('sec')
    ax.set_ylabel('bpm')
    ax.set_ylim([0, Ylim])
    ax.grid(True)

    ax = fig.add_subplot(413)
    ax.plot(x,y_3)
    ax.set_xlabel('sec')
    ax.set_ylabel('ptc integral')
    #ax.set_ylim([0, 100])
    ax.grid(True)

    ax = fig.add_subplot(414)
    ax.plot(x,y_4)
    ax.set_xlabel('sec')
    ax.set_ylabel('')
    #ax.set_ylim([0, 100])
    ax.grid(True)

    return fig

def HR_analysis(workout_dir):

    print("[HR Analysis]")
    raw_data_path = workout_dir + 'raw_data.csv'
    user_status_path = workout_dir + 'user_status_before_workout.csv'
    hr_analysis_dir = workout_dir + 'hr_analysis/'
    plot_dir = hr_analysis_dir

    if not os.path.exists(hr_analysis_dir):   
            os.makedirs(hr_analysis_dir)

    # load raw_data (call module)
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = DPM.raw_data_parsing(raw_data_path)

    # data padding
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)

    last_workout_time_sec, last_workout_duration_sec, last_max_hr, last_rest_hr, last_aero_capacity, last_aero_total_capacity, last_LA_dilution_grade, last_anaerobic_ptc, last_stamina_level, last_first_time_calibration = DPM.user_status_parsing(user_status_path)
    print("last_max_hr:{}, last_rest_hr:{}".format(last_max_hr, last_rest_hr))
    if last_rest_hr == -1:
        last_rest_hr = 71

    w_hr_filter = []
    for i in range(len(w_hr)):
        if i == 0:
            w_hr_filter += [w_hr[i]]
        else:
            w_hr_filter += [w_hr_filter[-1]*0.5 + w_hr[i]*0.5]
    w_hr = w_hr_filter

    # find delta hrr ptc change
    delta_hrr_ptc_list = []
    hrr_ptc_list = []
    
    pre_hrr_ptc = 0
    for i in range(len(w_hr)):
        hrr_ptc = float(w_hr[i] - last_rest_hr) / float(last_max_hr - last_rest_hr) * 100.0
        hrr_ptc_list += [hrr_ptc]
        if i == 0:
            delta_hrr_ptc_list += [0]
        else:
            delta_hrr_ptc_list += [hrr_ptc - pre_hrr_ptc]
        pre_hrr_ptc = hrr_ptc

    mavg_delta_hrr_ptc_list = []

    alpha = 0.99
    for i in range(len(delta_hrr_ptc_list)):
        if i == 0:
            mavg_delta_hrr_ptc_list += [0]
        else:
            #if delta_hrr_ptc_list[i] > 0:
            #    #delta_tune = (delta_hrr_ptc_list[i]+2.0)/2.0
            #    delta_tune = math.log(delta_hrr_ptc_list[i]*10 + 1)
            #    #delta_tune = 0.25
            #else:
            #    delta_tune = delta_hrr_ptc_list[i]
            delta_tune = delta_hrr_ptc_list[i]

            new_mavg = (
                        mavg_delta_hrr_ptc_list[-1] * alpha +
                        #delta_hrr_ptc_list[i] * (1-alpha)
                        #(math.exp(delta_hrr_ptc_list[i])-1) * (1-alpha)
                        delta_tune * (1-alpha)
                       )
            mavg_delta_hrr_ptc_list += [new_mavg]

    # integral of mavg_delta_hrr_ptc_list
    ig_list = []
    for i in range(len(mavg_delta_hrr_ptc_list)):
        if i == 0:
            ig_list += [mavg_delta_hrr_ptc_list[i]]
        else:
            mavg_tune = mavg_delta_hrr_ptc_list[i]
            ig = ig_list[-1] + mavg_tune
            ig_list += [ig]

    beta = 0.95
    f_mavg_list = []
    for i in range(len(mavg_delta_hrr_ptc_list)):
        if i == 0:
            f_mavg_list += [0]
        else:
            mavg_delta = mavg_delta_hrr_ptc_list[i] - mavg_delta_hrr_ptc_list[i-1]
            f_mavg_list += [f_mavg_list[-1]*beta + mavg_delta*(1-beta)]

    ff_mavg_list = []
    for i in range(len(f_mavg_list)):
        if i == 0:
            ff_mavg_list += [f_mavg_list[0]]
        else:
            f_mavg_delta = f_mavg_list[i] - f_mavg_list[i-1]
            ff_mavg_list += [ff_mavg_list[-1]*beta + f_mavg_delta*(1-beta)]

    
    pulse_list = []
    start_detect = -1
    for i in range(len(ff_mavg_list)):
        if hrr_ptc_list[i] >= 85:
            start_detect = 1
        elif hrr_ptc_list[i] <= 45:
            start_detect = -1

        if i == 0 or start_detect == -1:
            pulse_list += [0]
        else:
            '''
            if ff_mavg_list[i] >= 0.0:
                pulse_list += [pulse_list[-1] + ff_mavg_list[i]]
            else:
                pulse_list += [ pulse_list[-1] * math.exp(ff_mavg_list[i]*1000.0)]
            '''
            if mavg_delta_hrr_ptc_list[i] >= 0.0:
                if abs(f_mavg_list[i]) >= 0.004:
                    pulse_list += [pulse_list[-1] + mavg_delta_hrr_ptc_list[i]* ( 0.004 + (abs(f_mavg_list[i]) - 0.004)*0.0 ) ]
                else:
                    pulse_list += [pulse_list[-1] + mavg_delta_hrr_ptc_list[i]*abs(f_mavg_list[i]) ]
            else:
                pulse_list += [ pulse_list[-1] * math.exp(mavg_delta_hrr_ptc_list[i]*0.2)]
            '''
            if ff_mavg_list[i] >= 0.0 and f_mavg_list[i] >= 0.0:
                pulse_list += [pulse_list[-1] + ff_mavg_list[i]]
            elif ff_mavg_list >= 0.0:
                pulse_list += [ pulse_list[-1] * 0.99]
            else:
                pulse_list += [ pulse_list[-1] * math.exp(ff_mavg_list[i]*1000.0)]
            '''
    pulse_ptc_list = []
    for i in range(len(pulse_list)):
        if i == 0:
            pulse_ptc_list += [0]
        else:
            #pulse_limit = 0.01
            #pulse_limit = 0.4
            pulse_limit = 0.05
            pulse_ptc_list += [ pulse_ptc_list[-1]*beta + (pulse_limit - pulse_list[i])/pulse_limit * 100.0 * (1-beta)]



    # save to temp dir
    #fig = get_delta_hr_plot(w_t, w_hr, mavg_delta_hrr_ptc_list, ig_list, pulse_ptc_list)
    #fig = get_delta_hr_plot(w_t, w_hr, mavg_delta_hrr_ptc_list, ff_mavg_list, pulse_ptc_list)
    fig = get_delta_hr_plot(w_t, w_hr, mavg_delta_hrr_ptc_list, f_mavg_list, pulse_ptc_list)
    

    fig.savefig('/Users/Scott/git_repositories/stamina_lib_analysis_data/temp_output/' + 'delta_hr_{}.png'.format(workout_dir.replace('/','_')))

    plt.close(fig)
    
#######################################################
def t_sorted(to_be_sorted_list, time_sec_list):

    return [sorted_result for (sorted_total_secs, sorted_result) in sorted(zip(time_sec_list, to_be_sorted_list), key=lambda pair: pair[0])]


def sort_workout_and_remove_overlap(workout_dir_list, workout_time_sec_list, workout_duration_sec_list, stamina_lib_analysis_dir, name):
    # sort workout 
    workout_dir_list_sorted = t_sorted(workout_dir_list, workout_time_sec_list)
    workout_time_sec_list_sorted = t_sorted(workout_time_sec_list, workout_time_sec_list)
    workout_duration_sec_list_sorted = t_sorted(workout_duration_sec_list, workout_time_sec_list)
    print("workout_dir_list_sorted:{}".format(workout_dir_list_sorted))

    # remove overlap workout
    remove_list = []
    for i in range(len(workout_dir_list_sorted) - 1):
        
        this_workout_dir = workout_dir_list_sorted[i]   # this workout
        
        this_raw_data_info_path = stamina_lib_analysis_dir + name + '/' + this_workout_dir + '/' + 'raw_data_info.csv'

        # parsing this workout ################################################
        # read raw_data_info.csv
        data_info = open(this_raw_data_info_path, 'Ur')
        for raw in csv.DictReader(data_info):
            this_workout_time_sec = int(raw['workout_time_sec'])
            this_workout_duration_sec = int(raw['workout_duration_sec'])
            this_has_heartrate = int(float(raw['has_heartrate']))
            this_has_distance = int(float(raw['has_distance']))
            this_has_route = int(float(raw['has_route']))
            this_has_altitude = int(float(raw['has_altitude']))
            workout_text = raw['workout_text']
        data_info.close()
        
        if this_has_heartrate != 1:
            remove_list += [i]
        #if 'Gomore' in workout_text: # why add this limitation?
        #    remove_list += [i]

        #print("len(remove_list):{}".format(len(remove_list)))
        if len(remove_list) == 0 or (len(remove_list) > 0 and i != remove_list[-1]):
            for j in range(i+1, len(workout_dir_list_sorted) - 1, 1):
                next_workout_dir = workout_dir_list_sorted[j]   # this workout
                next_raw_data_info_path = stamina_lib_analysis_dir + name + '/' + next_workout_dir + '/' + 'raw_data_info.csv'
                # parsing next workout ################################################
                # read raw_data_info.csv
                #print("next_raw_data_info_path:{}".format(next_raw_data_info_path))
                data_info = open(next_raw_data_info_path, 'Ur')
                for raw in csv.DictReader(data_info):
                    next_workout_time_sec = int(raw['workout_time_sec'])
                    next_workout_duration_sec = int(raw['workout_duration_sec'])
                    next_has_heartrate = int(float(raw['has_heartrate']))
                    next_has_distance = int(float(raw['has_distance']))
                    next_has_route = int(float(raw['has_route']))
                    next_has_altitude = int(float(raw['has_altitude']))
                data_info.close()

                #print("this_workout_time_sec:{}".format(this_workout_time_sec))
                #print("next_workout_time_sec:{}".format(next_workout_time_sec))
                
                # opverlap detected
                if (
                    next_workout_time_sec >=  this_workout_time_sec and 
                    next_workout_time_sec <=  (this_workout_time_sec + this_workout_duration_sec) 
                   ):
                    #print("i:{}".format(i))
                    #print("workout_dir_list_sorted[i]:{}".format(workout_dir_list_sorted[i]))
                    # decide the remove workout
                    if (this_has_heartrate > next_has_heartrate):
                        remove_list += [j]
                    elif (this_has_heartrate == next_has_heartrate):
                        if (this_has_distance > next_has_distance):
                            remove_list += [j]
                        elif (this_has_distance == next_has_distance):
                            if (this_has_route >= next_has_route):
                                remove_list += [j]
                            else:
                                remove_list += [i]
                        else:
                            remove_list += [i]
                    else:
                        remove_list += [i]
                    
                    if next_has_heartrate != 1:
                        remove_list += [j]

                    #print("remove_list[-1]:{}".format(remove_list[-1]))
                    #print("workout_dir_list_sorted[remove_list[-1]]:{}".format(workout_dir_list_sorted[remove_list[-1]]))
    
    # take care the last workout check
    this_workout_dir = workout_dir_list_sorted[-1]   # this workout
        
    this_raw_data_info_path = stamina_lib_analysis_dir + name + '/' + this_workout_dir + '/' + 'raw_data_info.csv'

    # parsing this workout ################################################
    # read raw_data_info.csv
    data_info = open(this_raw_data_info_path, 'Ur')
    for raw in csv.DictReader(data_info):
        this_workout_time_sec = int(raw['workout_time_sec'])
        this_workout_duration_sec = int(raw['workout_duration_sec'])
        this_has_heartrate = int(float(raw['has_heartrate']))
        this_has_distance = int(float(raw['has_distance']))
        this_has_route = int(float(raw['has_route']))
        this_has_altitude = int(float(raw['has_altitude']))  
        workout_text = raw['workout_text']  
    data_info.close()
    
    if this_has_heartrate != 1:
        remove_list += [len(workout_dir_list_sorted) - 1]
    #if 'Gomore' in workout_text:
    #        remove_list += [len(workout_dir_list_sorted) - 1]

    print("remove_list:{}".format(remove_list))
    #for i in remove_list:
    #    print("workout_dir_list_sorted[i]:{}".format(workout_dir_list_sorted[i]))
    # update list of workout_dir_list_sorted
    workout_dir_list = []
    workout_time_sec_list = []
    workout_duration_sec_list = []
    for i in range(len(workout_dir_list_sorted)):
        if not (i in remove_list):
            assert not ('488676315' in workout_dir_list_sorted[i])
            workout_dir_list += [workout_dir_list_sorted[i]]
            workout_time_sec_list += [workout_time_sec_list_sorted[i]]
            workout_duration_sec_list += [workout_duration_sec_list_sorted[i]]
    #print("len(workout_dir_list_sorted):{}".format(len(workout_dir_list_sorted)))
    #print("len(workout_time_sec_list):{}".format(len(workout_time_sec_list)))

    return workout_dir_list, workout_time_sec_list, workout_duration_sec_list




#######################################################
#######################################################
#######################################################


def ride_stamina_analysis(workout_dir,
                         enable_grade_search,
                         age,
                         gender,
                         weight,
                         height,
                         max_HR,
                         rest_HR,
                         aero_total_capacity,
                         aero_capacity,
                         LA_dilution_grade,
                         anaerobic_ptc,
                         stamina_level,
                         recovery_secs,
                         first_time_calibration):
    print("workout_dir:{}".format(workout_dir))
    print("recovery_secs:{}".format(recovery_secs))

    raw_data_path = workout_dir + 'raw_data.csv'
    raw_data_filtering_path = workout_dir + 'raw_data_filtering.csv'
    raw_data_info_path = workout_dir + 'raw_data_info.csv'
    sv_user_status_path = workout_dir + 'user_status_before_workout_server.csv'
    user_status_path = workout_dir + 'user_status_before_workout.csv'
    calculation_result_path = workout_dir + 'calculation_result.csv'
    calculation_statistics_path = workout_dir + 'calculation_statistics.csv'

    # load raw_data (call module)
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence = DPM.ride_raw_data_parsing(raw_data_path)

    # load raw_data_info (call module)
    workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude, has_power, has_cadence = DPM.ride_raw_data_info_parsing(raw_data_info_path)

    # [Recovery calculation]
    print("    >>>>[Recovery calculation] start----")
    if recovery_secs == -1:
        recovery_secs = 0
    aero_total_capacity, aero_capacity, LA_dilution_grade, anaerobic_ptc = recovery_calculation(recovery_secs, age, gender, weight,height, max_HR,rest_HR,aero_total_capacity,aero_capacity,LA_dilution_grade,anaerobic_ptc,stamina_level)

    print("    ----[Recovery calculation] end<<<<")

    # [Grade search]
    '''
    if enable_grade_search == 1:
        grade_searched = GSM.ride_grade_search(raw_data_path, 
                                               age,
                                               gender,
                                               weight,
                                               height,
                                               max_HR,
                                               rest_HR)
        print("grade_searched:{}".format(grade_searched))
    '''
    
    # [Calculation + Calibration & update user parameters] dump calibration results
    print("    >>>>[Calibration calculation] start----")
    enable_calibration = 1
    init_aero_total_capacity_fix, init_aero_capacity_fix, init_LA_dilution_grade_fix, init_anaerobic_ptc_fix, end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, total_kcal_list, exercise_kcal_list, BMR_kcal_list, max_burn_kcal_list, max_dist_km_list, success_cali = stamina_c_lib_calculation(enable_calibration, 
                              age, 
                              gender,
                              weight,
                              height, 
                              max_HR,
                              rest_HR,
                              aero_total_capacity,
                              aero_capacity,
                              LA_dilution_grade,
                              anaerobic_ptc,
                              stamina_level,
                              first_time_calibration,
                              w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng,
                              workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude)
    
    if success_cali == 1:
        first_time_calibration = 0
    end_first_time_calibration = first_time_calibration
    print("    ----[Calibration calculation] end<<<<")

    # [Second Calculation]
    print("    >>>>[Second calculation] start----")
    enable_calibration = 0
    end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, total_kcal_list, exercise_kcal_list, BMR_kcal_list, max_burn_kcal_list, max_dist_km_list, rec_vdot, vdot_valid_tag, vdot_max_dist_km, rec_max_dist_km, rec_dist_km, rec_epoch_sec, instant_vdot_list, session_TRIMP, need_recovery_sec = stamina_c_lib_calculation(enable_calibration, 
                              age, 
                              gender,
                              weight,
                              height, 
                              end_max_HR,
                              rest_HR,
                              init_aero_total_capacity_fix,
                              init_aero_capacity_fix,
                              init_LA_dilution_grade_fix,
                              init_anaerobic_ptc_fix,
                              stamina_level,
                              end_first_time_calibration,
                              w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng,
                              workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude)
    # not for cycling now [TODO]
    #print("rec_vdot:{}".format(rec_vdot))
    #print("vdot_valid_tag:{}".format(vdot_valid_tag))
    #print("vdot_max_dist_km:{}".format(vdot_max_dist_km))
    #print("rec_max_dist_km:{}".format(rec_max_dist_km))
    #print("rec_dist_km:{}".format(rec_dist_km))
    #print("rec_epoch_sec:{}".format(rec_epoch_sec))

    print("    ----[Second calculation] end<<<<")

    # dump basic calculation results

    csv_header = []
    csv_header += ["w_t"]
    csv_header += ["w_hr"]
    csv_header += ["R_alt_m"]
    csv_header += ["R_dist_m"]
    csv_header += ["R_dist_km"]
    csv_header += ["R_speed_mps"]
    csv_header += ["R_speed_kmph"]
    csv_header += ["R_incline"]
    csv_header += ["R_lat"]
    csv_header += ["R_lng"]
    csv_header += ["stamina_ptc_list"]
    csv_header += ["aerobic_ptc_list"]
    csv_header += ["anaerobic_ptc_list"]
    csv_header += ["total_kcal_list"]
    csv_header += ["exercise_kcal_list"]
    csv_header += ["BMR_kcal_list"]
    csv_header += ["max_burn_kcal_list"]
    csv_header += ["max_dist_km_list"]
    #csv_header += ["instant_vdot_list"] # not for cycling now

    #print("len(w_t):{}".format(len(w_t)))
    #print("len(R_dist_km):{}".format(len(R_dist_km)))
    #print("len(stamina_ptc_list):{}".format(len(stamina_ptc_list)))

    with open(calculation_result_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(w_t)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    #print("csv_header[col]:{}".format((csv_header[col])))
                    #print("len:{}".format(len(eval(csv_header[col]))))
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

    # other analysis sub modules (py_prototype or c results analysis) py_prototype should start with py_
    # - add py_cardio_training_effect 

    # dump calculation statistics (may include py statistics)
    
    stamina_ptc_end = stamina_ptc_list[-1]
    aerobic_ptc_end = aerobic_ptc_list[-1]
    anaerobic_ptc_end = anaerobic_ptc_list[-1]
    total_kcal_end = total_kcal_list[-1]
    exercise_kcal_end = exercise_kcal_list[-1]
    BMR_kcal_end = BMR_kcal_list[-1]
    max_burn_kcal_end = max_burn_kcal_list[-1]
    max_dist_km_end = max_dist_km_list[-1]

    csv_header = []
    csv_header += ["stamina_ptc_end"]
    csv_header += ["aerobic_ptc_end"]
    csv_header += ["anaerobic_ptc_end"]
    csv_header += ["total_kcal_end"]
    csv_header += ["exercise_kcal_end"]
    csv_header += ["BMR_kcal_end"]
    csv_header += ["max_burn_kcal_end"]
    csv_header += ["max_dist_km_end"]

    with open(calculation_statistics_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        anlysis_result = []
        for col in range(len(csv_header)):
            anlysis_result += [eval(csv_header[col])]
        writer.writerow(anlysis_result)
        csvfile.close()

    # add plots
    plot_dir = workout_dir

    if has_heartrate == 1:

        fig = SWP.get_fig_time_stamina_alt(w_t,stamina_ptc_list,aerobic_ptc_list,anaerobic_ptc_list,R_alt_m,answer_breath,answer_muscle,answer_RPE,first_time_calibration, end_LA_dilution_grade, end_aero_total_capacity)
        fig.savefig(plot_dir + 'stamina_time.png')
        plt.close(fig)
    '''
    if has_heartrate == 1 and has_distance == 1: 
        fig = SWP.get_fig_time_vdot_alt(w_t,instant_vdot_list,R_alt_m,answer_breath,answer_muscle,answer_RPE,first_time_calibration, end_LA_dilution_grade, end_aero_total_capacity)
        fig.savefig(plot_dir + 'instant_vdot_time.png')
        plt.close(fig)
    '''
    if has_heartrate == 1:
        fig = SWP.get_fig_time_max_burn_alt(w_t,total_kcal_list,max_burn_kcal_list,R_alt_m)
        fig.savefig(plot_dir + 'max_burn_time.png')
        plt.close(fig)

    if has_heartrate == 1 and has_distance == 1:
        fig = SWP.get_fig_dist_max_dist_alt(R_dist_km,R_dist_km,max_dist_km_list,R_alt_m)
        fig.savefig(plot_dir + 'max_dist_dist.png')
        plt.close(fig)

    return end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, end_first_time_calibration, init_aero_total_capacity_fix, init_aero_capacity_fix


def run_stamina_analysis(workout_dir,
                         enable_grade_search,
                         age,
                         gender,
                         weight,
                         height,
                         max_HR,
                         rest_HR,
                         aero_total_capacity,
                         aero_capacity,
                         LA_dilution_grade,
                         anaerobic_ptc,
                         stamina_level,
                         recovery_secs,
                         first_time_calibration):
    print("workout_dir:{}".format(workout_dir))
    print("recovery_secs:{}".format(recovery_secs))

    # data of different analysis should be stored in seperated files?
    # or CSV append?

    raw_data_path = workout_dir + 'raw_data.csv'
    raw_data_filtering_path = workout_dir + 'raw_data_filtering.csv'
    raw_data_info_path = workout_dir + 'raw_data_info.csv'
    sv_user_status_path = workout_dir + 'user_status_before_workout_server.csv'
    user_status_path = workout_dir + 'user_status_before_workout.csv'
    calculation_result_path = workout_dir + 'calculation_result.csv'
    calculation_statistics_path = workout_dir + 'calculation_statistics.csv'

    # load raw_data (call module)
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = DPM.raw_data_parsing(raw_data_path)
    
    # load filter w_hr !!!
    #print("!!! load filtered Heart Rate")
    #w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = DPM.raw_data_parsing(raw_data_filtering_path)

    # load raw_data_info (call module)
    workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude = DPM.raw_data_info_parsing(raw_data_info_path)

    '''
    # user status before workout in server parse (call func)
    if os.path.exists(sv_user_status_path): # data from gomore server
        sv_last_workout_time_sec, sv_last_workout_duration_sec, sv_last_max_hr, sv_last_rest_hr, sv_last_aero_capacity, sv_last_aero_total_capacity, sv_last_LA_dilution_grade, sv_last_anaerobic_ptc, sv_last_stamina_level, sv_last_first_time_calibration = DPM.user_status_in_server_parsing(sv_user_status_path)
        # swap init value here!
        # TBD
    '''

    max_speed_kmph = get_max_speed_kmph(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)

    # [Recovery calculation]
    print("    >>>>[Recovery calculation] start----")
    if recovery_secs == -1:
        recovery_secs = 0
    aero_total_capacity, aero_capacity, LA_dilution_grade, anaerobic_ptc = recovery_calculation(recovery_secs, age, gender, weight,height, max_HR,rest_HR,aero_total_capacity,aero_capacity,LA_dilution_grade,anaerobic_ptc,stamina_level)

    print("    ----[Recovery calculation] end<<<<")
    # [Grade search]
    '''
    if enable_grade_search == 1:
        grade_searched = GSM.run_grade_search(raw_data_path, 
                                               age,
                                               gender,
                                               weight,
                                               height,
                                               max_HR,
                                               rest_HR)
        print("grade_searched:{}".format(grade_searched))
    '''

    # [Calculation + Calibration & update user parameters] dump calibration results
    print("    >>>>[Calibration calculation] start----")
    enable_calibration = 1
    init_aero_total_capacity_fix, init_aero_capacity_fix, init_LA_dilution_grade_fix, init_anaerobic_ptc_fix, end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, total_kcal_list, exercise_kcal_list, BMR_kcal_list, max_burn_kcal_list, max_dist_km_list, success_cali = stamina_c_lib_calculation(enable_calibration, 
                              age, 
                              gender,
                              weight,
                              height, 
                              max_HR,
                              rest_HR,
                              aero_total_capacity,
                              aero_capacity,
                              LA_dilution_grade,
                              anaerobic_ptc,
                              stamina_level,
                              first_time_calibration,
                              w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng,
                              workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude)
    
    if success_cali == 1:
        first_time_calibration = 0
    end_first_time_calibration = first_time_calibration
    print("    ----[Calibration calculation] end<<<<")

    # [Second Calculation]
    print("    >>>>[Second calculation] start----")
    enable_calibration = 0
    end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, total_kcal_list, exercise_kcal_list, BMR_kcal_list, max_burn_kcal_list, max_dist_km_list, rec_vdot, vdot_valid_tag, vdot_max_dist_km, rec_max_dist_km, rec_dist_km, rec_epoch_sec, instant_vdot_list, session_TRIMP, need_recovery_sec = stamina_c_lib_calculation(enable_calibration, 
                              age, 
                              gender,
                              weight,
                              height, 
                              end_max_HR,
                              rest_HR,
                              init_aero_total_capacity_fix,
                              init_aero_capacity_fix,
                              init_LA_dilution_grade_fix,
                              init_anaerobic_ptc_fix,
                              stamina_level,
                              end_first_time_calibration,
                              w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng,
                              workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude)
    print("rec_vdot:{}".format(rec_vdot))
    print("vdot_valid_tag:{}".format(vdot_valid_tag))
    print("vdot_max_dist_km:{}".format(vdot_max_dist_km))
    print("rec_max_dist_km:{}".format(rec_max_dist_km))
    print("rec_dist_km:{}".format(rec_dist_km))
    print("rec_epoch_sec:{}".format(rec_epoch_sec))

    print("    ----[Second calculation] end<<<<")
    # dump basic calculation results

    csv_header = []
    csv_header += ["w_t"]
    csv_header += ["w_hr"]
    csv_header += ["R_alt_m"]
    csv_header += ["R_dist_m"]
    csv_header += ["R_dist_km"]
    csv_header += ["R_speed_mps"]
    csv_header += ["R_speed_kmph"]
    csv_header += ["R_incline"]
    csv_header += ["R_lat"]
    csv_header += ["R_lng"]
    csv_header += ["stamina_ptc_list"]
    csv_header += ["aerobic_ptc_list"]
    csv_header += ["anaerobic_ptc_list"]
    csv_header += ["total_kcal_list"]
    csv_header += ["exercise_kcal_list"]
    csv_header += ["BMR_kcal_list"]
    csv_header += ["max_burn_kcal_list"]
    csv_header += ["max_dist_km_list"]
    csv_header += ["instant_vdot_list"]

    #print("len(w_t):{}".format(len(w_t)))
    #print("len(R_dist_km):{}".format(len(R_dist_km)))
    #print("len(stamina_ptc_list):{}".format(len(stamina_ptc_list)))
            
    with open(calculation_result_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(w_t)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    #print("csv_header[col]:{}".format((csv_header[col])))
                    #print("len:{}".format(len(eval(csv_header[col]))))
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

    # other analysis sub modules (py_prototype or c results analysis) py_prototype should start with py_
    # - add py_cardio_training_effect 

    # dump calculation statistics (may include py statistics)
    
    stamina_ptc_end = stamina_ptc_list[-1]
    aerobic_ptc_end = aerobic_ptc_list[-1]
    anaerobic_ptc_end = anaerobic_ptc_list[-1]
    total_kcal_end = total_kcal_list[-1]
    exercise_kcal_end = exercise_kcal_list[-1]
    BMR_kcal_end = BMR_kcal_list[-1]
    max_burn_kcal_end = max_burn_kcal_list[-1]
    max_dist_km_end = max_dist_km_list[-1]

    csv_header = []
    csv_header += ["stamina_ptc_end"]
    csv_header += ["aerobic_ptc_end"]
    csv_header += ["anaerobic_ptc_end"]
    csv_header += ["total_kcal_end"]
    csv_header += ["exercise_kcal_end"]
    csv_header += ["BMR_kcal_end"]
    csv_header += ["max_burn_kcal_end"]
    csv_header += ["max_dist_km_end"]
    csv_header += ["session_TRIMP"]
    csv_header += ["need_recovery_sec"]

    with open(calculation_statistics_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        anlysis_result = []
        for col in range(len(csv_header)):
            anlysis_result += [eval(csv_header[col])]
        writer.writerow(anlysis_result)
        csvfile.close()



    

    # add plots
    plot_dir = workout_dir

    if has_heartrate == 1:

        fig = SWP.get_fig_time_stamina_alt(w_t,stamina_ptc_list,aerobic_ptc_list,anaerobic_ptc_list,R_alt_m,answer_breath,answer_muscle,answer_RPE,first_time_calibration, end_LA_dilution_grade, end_aero_total_capacity)
        fig.savefig(plot_dir + 'stamina_time.png')
        plt.close(fig)

    if has_heartrate == 1 and has_distance == 1: 
        fig = SWP.get_fig_time_vdot_alt(w_t,instant_vdot_list,R_alt_m,answer_breath,answer_muscle,answer_RPE,first_time_calibration, end_LA_dilution_grade, end_aero_total_capacity)
        fig.savefig(plot_dir + 'instant_vdot_time.png')
        plt.close(fig)

    if has_heartrate == 1:
        fig = SWP.get_fig_time_max_burn_alt(w_t,total_kcal_list,max_burn_kcal_list,R_alt_m)
        fig.savefig(plot_dir + 'max_burn_time.png')
        plt.close(fig)

    if has_heartrate == 1 and has_distance == 1:
        fig = SWP.get_fig_dist_max_dist_alt(R_dist_km,R_dist_km,max_dist_km_list,R_alt_m)
        fig.savefig(plot_dir + 'max_dist_dist.png')
        plt.close(fig)

    # temp output
    '''
    plot_dir = '/Users/Scott/git_repositories/stamina_lib_analysis_data/temp_output/'
    if has_heartrate == 1:

        fig = SWP.get_fig_time_stamina_alt(w_t,stamina_ptc_list,aerobic_ptc_list,anaerobic_ptc_list,R_alt_m,answer_breath,answer_muscle,answer_RPE,first_time_calibration, end_LA_dilution_grade, end_aero_total_capacity)
        fig.savefig(plot_dir + 'stamina_time_{}.png'.format(workout_dir.replace("/","_")))
        plt.close(fig)

    if has_heartrate == 1 and has_distance == 1:
        fig = SWP.get_fig_dist_max_dist_alt(R_dist_km,R_dist_km,max_dist_km_list,R_alt_m)
        fig.savefig(plot_dir + 'max_dist_dist_{}.png'.format(workout_dir.replace("/","_")))
        plt.close(fig)
    '''
    



    return end_max_HR, end_aero_total_capacity, end_aero_capacity, end_LA_dilution_grade, end_anaerobic_ptc, end_first_time_calibration, rec_vdot, vdot_valid_tag, vdot_max_dist_km, rec_max_dist_km, rec_dist_km, rec_epoch_sec, init_aero_total_capacity_fix, init_aero_capacity_fix, max_speed_kmph

























