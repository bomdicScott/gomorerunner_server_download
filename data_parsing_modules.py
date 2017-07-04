import csv
import numpy as np
import json
import math
import os, sys
import itertools
import dateutil
import datetime
import time
import zipfile
#import route_filtering_modules as RFM

def get_epoch_sec(time):
    epoch_time = dateutil.parser.parse("1970-01-01T00:00:00Z")
    return int((time - epoch_time).total_seconds())

def get_data_from_epoch_sec(epoch_sec):
    #return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(epoch_sec))
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(epoch_sec))


def check_null(value):
    if value != None and value != 'Null':
        return value
    #elif float(value) == -1:
    #    return 0
    else:
        return 0

def gomorerider_status_parsing(src_user_obj_json_path, src_vdot_list_json_path):

    with open(src_vdot_list_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    last_workout_dir = 'NA'
    last_workout_time_sec = -1
    last_workout_duration_sec = -1
    last_stamina_level = -1
    for value in data:
        last_workout_time_sec = int(value['rec_epoch_sec'])
        last_workout_duration_sec = int(value['rec_end_epoch_sec']) - last_workout_time_sec
        last_stamina_level = float(value['stamina_level'])

    with open(src_user_obj_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    last_max_hr = int(data['maxHeartRate'])
    last_rest_hr = int(data['restingHeartRate'])
    last_aero_total_capacity = float(data['aeroTotalCapacity'])
    last_aero_capacity = float(data['aeroCapacity'])
    last_LA_dilution_grade = int(data['laDilutionGrade'])
    last_anaerobic_ptc = float(data['anaerobicPtc'])
    last_first_time_calibration = int(data['first_time'])

    print("[DPM]last_workout_time_sec:{}".format(last_workout_time_sec))
    print("[DPM]last_workout_duration_sec:{}".format(last_workout_duration_sec))

    return last_workout_time_sec,last_workout_duration_sec,last_workout_dir,last_max_hr,last_rest_hr,last_aero_total_capacity,last_aero_capacity,last_LA_dilution_grade,last_anaerobic_ptc,last_stamina_level,last_first_time_calibration

def gomorerunner_status_parsing(src_user_obj_json_path, src_vdot_list_json_path):

    with open(src_vdot_list_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    last_workout_dir = 'NA'
    last_workout_time_sec = -1
    last_workout_duration_sec = -1
    last_stamina_level = -1
    for value in data:
        last_workout_time_sec = int(value['rec_epoch_sec'])
        last_workout_duration_sec = int(value['rec_end_epoch_sec']) - last_workout_time_sec
        last_stamina_level = float(value['stamina_level'])

    with open(src_user_obj_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    last_max_hr = int(data['maxHeartRate'])
    last_rest_hr = int(data['restingHeartRate'])
    last_aero_total_capacity = float(data['aeroTotalCapacity'])
    last_aero_capacity = float(data['aeroCapacity'])
    last_LA_dilution_grade = int(data['laDilutionGrade'])
    last_anaerobic_ptc = float(data['anaerobicPtc'])
    last_first_time_calibration = int(data['first_time'])

    print("[DPM]last_workout_time_sec:{}".format(last_workout_time_sec))
    print("[DPM]last_workout_duration_sec:{}".format(last_workout_duration_sec))

    return last_workout_time_sec,last_workout_duration_sec,last_workout_dir,last_max_hr,last_rest_hr,last_aero_total_capacity,last_aero_capacity,last_LA_dilution_grade,last_anaerobic_ptc,last_stamina_level,last_first_time_calibration

def gomorerider_info_parsing(src_user_obj_json_path):

    with open(src_user_obj_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    workout_time_sec = int(data['workout_start'])
    workout_duration_sec = int(data['workout_end']) - workout_time_sec
    answer_breath = int(data['question_breath'])
    answer_muscle = int(data['question_muscle'])
    answer_RPE = int(data['question_rpe'])

    workout_text = 'NA'
    workout_date = get_data_from_epoch_sec(workout_time_sec)
    #print("workout_date:{}".format(workout_date))

    print("workout_duration_sec:{}".format(workout_duration_sec))


    return workout_date, workout_time_sec, workout_duration_sec, workout_text, answer_breath, answer_muscle, answer_RPE

def gomorerunner_info_parsing(src_user_obj_json_path):

    with open(src_user_obj_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    workout_time_sec = int(data['workout_start'])
    workout_duration_sec = int(data['workout_end']) - workout_time_sec
    answer_breath = int(data['question_breath'])
    answer_muscle = int(data['question_muscle'])
    answer_RPE = int(data['question_rpe'])

    workout_text = 'NA'
    workout_date = get_data_from_epoch_sec(workout_time_sec)
    #print("workout_date:{}".format(workout_date))


    return workout_date, workout_time_sec, workout_duration_sec, workout_text, answer_breath, answer_muscle, answer_RPE

def get_padding_data_to_workout_duration_sec(workout_duration_sec, t_list, data_list):

    # process data_list
    #print("t_list:{}".format(t_list))
    #print("data_list:{}".format(data_list))
    w_i = 0
    while w_i < len(t_list):
        if (w_i - 1) >= 0 and t_list[w_i-1] == t_list[w_i]:
            del t_list[w_i-1]
            del data_list[w_i-1]
        else:
            w_i += 1
    
    # remove time offset at very begining
    offset = t_list[0]
    for t in range(len(t_list)):
        t_list[t] = t_list[t] - offset

    #print("t_list:{}".format(t_list))
    #print("data_list:{}".format(data_list))

    # padding to workout_duration_sec
    t_list_padding = []
    data_list_padding = []
    for i in range(len(t_list)):
    #for i in range(9210):
        #if i > 10:
        #    assert False

        if len(t_list_padding) == 0:
            #print("[len(t_list_padding) == 0], i:{}".format(i))
            t_list_padding += [t_list[i]]
            data_list_padding += [data_list[i]]
        elif len(t_list_padding) > 0:
            #print("t_list[i]:{}".format(t_list[i]))
            #print("t_list_padding[-1]:{}".format(t_list_padding[-1]))
            if t_list[i] - t_list_padding[-1] > 1:
                padding_len = t_list[i] - t_list_padding[-1] - 1
                #print("padding_len:{}".format(padding_len))
                for j in range(padding_len):
                    t_list_padding += [t_list_padding[-1]+1]
                    data_list_padding += [data_list_padding[-1]]
                t_list_padding += [t_list[i]]
                data_list_padding += [data_list[i]]
            elif t_list[i] - t_list_padding[-1] == 1:
                t_list_padding += [t_list[i]]
                data_list_padding += [data_list[i]]
    #t_list = t_list_padding
    #data_list = data_list_padding
    #print("t_list_padding:{}".format(t_list_padding))
    #print("data_list_padding:{}".format(data_list_padding))

    # check end point
    #print("len(t_list_padding):{}".format(len(t_list_padding)))
    t_list = []
    data_list = []
    for i in range(workout_duration_sec+1):
        if i < len(t_list_padding) and i == t_list_padding[i]:
            t_list += [t_list_padding[i]]
            data_list += [data_list_padding[i]]
        else:
            t_list += [i]
            data_list += [data_list_padding[-1]]
    #print("t_list:{}".format(t_list))
    #print("data_list:{}".format(data_list))

    return t_list, data_list


def gomore_json_parsing(dst_raw_HR_path, dst_raw_route_path, workout_duration_sec):
    print("[DPM][parse] dst_raw_HR_path:{}".format(dst_raw_HR_path))

    w_t = []
    w_hr = []

    R_t = []
    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []
    R_watts = []
    R_cadence = []

    # parsing dst_raw_HR_path
    with open(dst_raw_HR_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    for value in data:
        w_t += [int(check_null(value['seconds']))]
        w_hr += [int(check_null(value['heartrate']))]

    # parsing dst_raw_route_path
    with open(dst_raw_route_path) as data_file:
        data = json.load(data_file) 
    data_file.close()
    #print("data:{}".format(data))
    if data == []:
        for i in range(len(w_t)):
            R_alt_m += [float( check_null('Null') )]
            R_dist_km += [float( check_null('Null') )]
            R_dist_m += [ R_dist_km[-1] * 1000.0 ]
            R_speed_mps += [float( check_null('Null') )]
            R_speed_kmph += [ R_speed_mps[-1] * 3.6 ]
            R_incline += [float( check_null('Null') )]
            R_lat += [float( check_null('Null') )]
            R_lng += [float( check_null('Null') )]
            R_watts += [0]
            R_cadence += [0]
            R_t += [w_t[i]]
    else:
        for value in data:
            R_alt_m += [float( check_null(value['altitude']) )]
            R_dist_m += [float( check_null(value['distance']) )]
            R_dist_km += [ R_dist_m[-1] / 1000.0 ]
            R_speed_mps += [float( check_null(value['speed']) )]
            R_speed_kmph += [ R_speed_mps[-1] * 3.6 ]
            R_incline += [0]
            R_lat += [float( check_null(value['latitude']) )]
            R_lng += [float( check_null(value['longitude']) )]
            R_watts += [0]
            R_cadence += [0]
            R_t += [int( check_null(value['seconds']) )]

    print("len(w_t):{}".format(len(w_t)))
    print("len(R_dist_km):{}".format(len(R_dist_km)))
    print("workout_duration_sec:{}".format(workout_duration_sec))

    """
    # process w_hr
    print("w_t:{}".format(w_t))
    print("w_hr:{}".format(w_hr))
    w_i = 0
    # w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng
    while w_i < len(w_t):
        if (w_i - 1) >= 0 and w_t[w_i-1] == w_t[w_i]:
            del w_t[w_i-1]
            del w_hr[w_i-1]
        else:
            w_i += 1
    
    # remove time offset at very begining
    offset = w_t[0]
    for t in range(len(w_t)):
        w_t[t] = w_t[t] - offset

    print("w_t:{}".format(w_t))
    print("w_hr:{}".format(w_hr))

    # padding to workout_duration_sec
    w_t_padding = []
    w_hr_padding = []
    for i in range(len(w_t)):
    #for i in range(9210):
        #if i > 10:
        #    assert False

        if len(w_t_padding) == 0:
            #print("[len(w_t_padding) == 0], i:{}".format(i))
            w_t_padding += [w_t[i]]
            w_hr_padding += [w_hr[i]]
        elif len(w_t_padding) > 0:
            #print("w_t[i]:{}".format(w_t[i]))
            #print("w_t_padding[-1]:{}".format(w_t_padding[-1]))
            if w_t[i] - w_t_padding[-1] > 1:
                padding_len = w_t[i] - w_t_padding[-1] - 1
                #print("padding_len:{}".format(padding_len))
                for j in range(padding_len):
                    w_t_padding += [w_t_padding[-1]+1]
                    w_hr_padding += [w_hr_padding[-1]]
                w_t_padding += [w_t[i]]
                w_hr_padding += [w_hr[i]]
            elif w_t[i] - w_t_padding[-1] == 1:
                w_t_padding += [w_t[i]]
                w_hr_padding += [w_hr[i]]
    #w_t = w_t_padding
    #w_hr = w_hr_padding
    print("w_t_padding:{}".format(w_t_padding))
    print("w_hr_padding:{}".format(w_hr_padding))

    # check end point
    print("len(w_t_padding):{}".format(len(w_t_padding)))
    w_t = []
    w_hr = []
    for i in range(workout_duration_sec+1):
        if i < len(w_t_padding) and i == w_t_padding[i]:
            w_t += [w_t_padding[i]]
            w_hr += [w_hr_padding[i]]
        else:
            w_t += [i]
            w_hr += [w_hr_padding[-1]]
    print("w_t:{}".format(w_t))
    print("w_hr:{}".format(w_hr))
    """

    padding_w_t, padding_w_hr = get_padding_data_to_workout_duration_sec(workout_duration_sec, w_t, w_hr)

    padding_R_t, padding_R_alt_m = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_alt_m)
    padding_R_t, padding_R_dist_m = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_dist_m)
    padding_R_t, padding_R_dist_km = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_dist_km)
    padding_R_t, padding_R_speed_mps = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_speed_mps)
    padding_R_t, padding_R_speed_kmph = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_speed_kmph)
    padding_R_t, padding_R_incline = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_incline)
    padding_R_t, padding_R_lat = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_lat)
    padding_R_t, padding_R_lng = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_lng)
    padding_R_t, padding_R_watts = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_watts)
    padding_R_t, padding_R_cadence = get_padding_data_to_workout_duration_sec(workout_duration_sec, R_t, R_cadence)


    """
    padding_w_t = []
    padding_w_hr = []

    #print("padding_w_t[-1]:{}".format(padding_w_t[-1]))

    padding_R_alt_m = []
    padding_R_dist_m = []
    padding_R_dist_km = []
    padding_R_speed_mps = []
    padding_R_speed_kmph = []
    padding_R_incline = []
    padding_R_lat = []
    padding_R_lng = []
    padding_R_watts = []
    padding_R_cadence = []
    padding_R_t = []

    w_i = 0
    R_i = 0
    for t in range(workout_duration_sec + 1):
        if t > 15:
            assert False
        ######
        
        if w_i < len(w_t) and w_t[w_i] <=  t:
            print("t:{}, w_i:{}, w_t[w_i]:{}, w_hr[w_i]:{}".format(t, w_i, w_t[w_i], w_hr[w_i]))
            if w_t[w_i] ==  t:
                padding_w_t += [w_t[w_i]]
                padding_w_hr += [w_hr[w_i]]
            else: # padding required
                
                while w_i < len(w_t) and w_i > 0 and w_t[w_i-1] == w_t[w_i]: # handle duplicated w_t
                    print("[duplicated sec]w_i:{}, w_t[w_i]:{}".format(w_i, w_t[w_i]))
                    padding_w_t[-1] = w_t[w_i]
                    padding_w_hr[-1] = w_hr[w_i]
                    w_i += 1
                w_i -= 1 

                print("[A]padding w_t:{}, w_hr:{}".format(padding_w_t[-1]+1, padding_w_hr[-1]))
                padding_w_t += [padding_w_t[-1]+1]
                padding_w_hr += [padding_w_hr[-1]]
                
                
            w_i += 1
        else: # padding required
            print("[B]padding w_t:{}, w_hr:{}".format(padding_w_t[-1]+1, padding_w_hr[-1]))
            if t == 0:
                padding_w_t += [0]
                padding_w_hr += [w_hr[0]]
            else:
                padding_w_t += [padding_w_t[-1]+1]
                padding_w_hr += [padding_w_hr[-1]]
        print("[t]:{}, w_i:{} padding_w_t:{}, padding_w_hr:{}".format(t, w_i, padding_w_t, padding_w_hr))
        ######
        if R_i < len(R_t) and R_t[R_i] <= t:
            #print("t:{}, R_i:{}, R_t[R_i]:{}".format(t, R_i, R_t[R_i]))
            if R_t[R_i] == t:
                #print("t:{}".format(t))
                #print("R_i:{}".format(R_i))
                #print("R_dist_km[R_i]:{}".format(R_dist_km[R_i]))
                padding_R_t += [R_t[R_i]]
                padding_R_dist_km += [R_dist_km[R_i]]
                padding_R_alt_m += [R_alt_m[R_i]]
                padding_R_dist_m += [R_dist_m[R_i]]
                padding_R_speed_mps += [R_speed_mps[R_i]]
                padding_R_speed_kmph += [R_speed_kmph[R_i]]
                padding_R_incline += [R_incline[R_i]]
                padding_R_lat += [R_lat[R_i]]
                padding_R_lng += [R_lng[R_i]]
                padding_R_watts += [R_watts[R_i]]
                padding_R_cadence += [R_cadence[R_i]]

            else: # padding required

                while R_i < len(R_t) and R_i > 0 and R_t[R_i-1] == R_t[R_i]: # handle duplicated R_t
                    padding_R_t[-1] = R_t[R_i]
                    padding_R_dist_km[-1] = R_dist_km[R_i]
                    padding_R_alt_m[-1] = R_alt_m[R_i]
                    padding_R_dist_m[-1] = R_dist_m[R_i]
                    padding_R_speed_mps[-1] = R_speed_mps[R_i]
                    padding_R_speed_kmph[-1] = R_speed_kmph[R_i]
                    padding_R_incline[-1] = R_incline[R_i]
                    padding_R_lat[-1] = R_lat[R_i]
                    padding_R_lng[-1] = R_lng[R_i]
                    padding_R_watts[-1] = R_watts[R_i]
                    padding_R_cadence[-1] = R_cadence[R_i]
                    R_i += 1 
                R_i -= 1

                padding_R_t += [padding_R_t[-1]+1]
                padding_R_dist_km += [padding_R_dist_km[-1]]
                padding_R_alt_m += [padding_R_alt_m[-1]]
                padding_R_dist_m += [padding_R_dist_m[-1]]
                padding_R_speed_mps += [padding_R_speed_mps[-1]]
                padding_R_speed_kmph += [padding_R_speed_kmph[-1]]
                padding_R_incline += [padding_R_incline[-1]]
                padding_R_lat += [padding_R_lat[-1]]
                padding_R_lng += [padding_R_lng[-1]]
                padding_R_watts += [padding_R_watts[-1]]
                padding_R_cadence += [padding_R_cadence[-1]]

            #if R_i+1 < len(R_t):
            
            R_i += 1
        
        else:  # padding required
            if t == 0:
                padding_R_t += [0]
                padding_R_dist_km += [R_dist_km[0]]
                padding_R_alt_m += [R_alt_m[0]]
                padding_R_dist_m += [R_dist_m[0]]
                padding_R_speed_mps += [R_speed_mps[0]]
                padding_R_speed_kmph += [R_speed_kmph[0]]
                padding_R_incline += [R_incline[0]]
                padding_R_lat += [R_lat[0]]
                padding_R_lng += [R_lng[0]]
                padding_R_watts += [R_watts[0]]
                padding_R_cadence += [R_cadence[0]]
            else:
                padding_R_t += [padding_R_t[-1]+1]
                padding_R_dist_km += [padding_R_dist_km[-1]]
                padding_R_alt_m += [padding_R_alt_m[-1]]
                padding_R_dist_m += [padding_R_dist_m[-1]]
                padding_R_speed_mps += [padding_R_speed_mps[-1]]
                padding_R_speed_kmph += [padding_R_speed_kmph[-1]]
                padding_R_incline += [padding_R_incline[-1]]
                padding_R_lat += [padding_R_lat[-1]]
                padding_R_lng += [padding_R_lng[-1]]
                padding_R_watts += [padding_R_watts[-1]]
                padding_R_cadence += [padding_R_cadence[-1]]

    """
    #print("workout_duration_sec:{}".format(workout_duration_sec))
    #print("len(padding_w_t):{}".format(len(padding_w_t)))
    #print("len(padding_R_t):{}".format(len(padding_R_t)))
    #print("len(padding_R_dist_km):{}".format(len(padding_R_dist_km)))

    #print("        w_hr:{}".format(w_hr))
    #print("padding_w_hr:{}".format(padding_w_hr))

    #print("        R_dist_km:{}".format(R_dist_km))
    #print("padding_R_dist_km:{}".format(padding_R_dist_km))

    #print("        w_t:{}".format(w_t))
    #print("padding_w_t:{}".format(padding_w_t))
    #print("        R_t:{}".format(R_t))
    #print("padding_R_t:{}".format(padding_R_t))

    #print("len(w_t):{}".format(len(w_t)))
    #print("len(R_dist_km):{}".format(len(R_dist_km)))


    w_t = padding_w_t
    w_hr = padding_w_hr

    R_alt_m = padding_R_alt_m
    R_dist_m = padding_R_dist_m
    R_dist_km = padding_R_dist_km
    R_speed_mps = padding_R_speed_mps
    R_speed_kmph = padding_R_speed_kmph
    R_incline = padding_R_incline
    R_lat = padding_R_lat
    R_lng = padding_R_lng
    R_watts = padding_R_watts
    R_cadence = padding_R_cadence
    R_t = padding_R_t

    '''
    for i in range(len(w_t)):
        print("w_t[i]:{}, w_hr[i]:{}, R_dist_m[i]:{}".format(w_t[i], w_hr[i], R_dist_m[i]))
        #if i > 50:
        #    assert False
    '''
    assert len(padding_w_t) == len(padding_w_hr)
    assert len(padding_R_t) == len(padding_R_dist_km)
    assert len(padding_R_t) == len(padding_R_speed_mps)
    assert len(w_t) == len(R_dist_km)
    
    

    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence



def gomorerider_json_parsing(src_verified_json_path, src_route_json_path):
    print("[DPM][parse] src_verified_json_path:{}".format(src_verified_json_path))
    
    w_t = []
    w_hr = []
    w_kcal = []
    w_kcal_max = []
    w_kcal_aerobic = []
    w_kcal_aerobic_max = []
    w_kcal_anaerobic = []
    w_kcal_anaerobic_max = []
    w_stamina = []
    w_stamina_aerobic = []
    w_stamina_anaerobic = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []
    R_watts = []
    R_cadence = []

    # parsing src_verified_json_path
    with open(src_verified_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    # sort by time
    for row in data:
        for key in row.keys():
            if key == "second":
                    row[key] = int(row[key])
    data = sorted(data,key=lambda x:x['second'])

    for value in data:
        w_t += [int(check_null(value['second']))]
        w_hr += [int(check_null(value['heartrate']))]
        w_kcal += [float( check_null(value['kcal']) )]
        w_kcal_max += [float( check_null(value['kcal_max']) )]
        if 'kcal_aerobic' in value:
            w_kcal_aerobic += [float( check_null(value['kcal_aerobic']) )]
        else:
            w_kcal_aerobic += [-1]
        if 'kcal_aerobic_max' in value:
            w_kcal_aerobic_max += [float( check_null(value['kcal_aerobic_max']) )]
        else:
            w_kcal_aerobic_max += [-1]
        if 'kcal_anaerobic' in value:
            w_kcal_anaerobic += [float( check_null(value['kcal_anaerobic']) )]
        else:
            w_kcal_anaerobic += [-1]
        if 'kcal_anaerobic_max' in value:
            w_kcal_anaerobic_max += [float( check_null(value['kcal_anaerobic_max']) )]
        else:
            w_kcal_anaerobic_max += [-1]

        w_stamina += [float( check_null(value['stamina']) )]
        w_stamina_aerobic += [float( check_null(value['stamina_aerobic']) )]
        w_stamina_anaerobic += [float( check_null(value['stamina_anaerobic']) )]
        
        # only for yayu's format ?
        if 'power' in value:
            R_watts += [float (check_null(value['power']))]

        if 'cadence' in value:
            R_cadence += [float (check_null(value['cadence']))]


    # parsing src_route_json_path
    with open(src_route_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    if data == []:
        for i in range(len(w_t)):
            R_alt_m += [float( check_null('Null') )]
            R_dist_km += [float( check_null('Null') )]
            R_dist_m += [ R_dist_km[-1] * 1000.0 ]
            R_speed_mps += [float( check_null('Null') )]
            R_speed_kmph += [ R_speed_mps[-1] * 3.6 ]
            R_incline += [float( check_null('Null') )]
            R_lat += [float( check_null('Null') )]
            R_lng += [float( check_null('Null') )]
    else:
        for value in data:
            R_alt_m += [float( check_null(value['altitude']) )]
            R_dist_km += [float( check_null(value['distance_km']) )]
            R_dist_m += [ R_dist_km[-1] * 1000.0 ]
            R_speed_mps += [float( check_null(value['speed']) )]
            R_speed_kmph += [ R_speed_mps[-1] * 3.6 ]
            R_incline += [float( check_null(value['geo_incline']) )]
            R_lat += [float( check_null(value['latitude']) )]
            R_lng += [float( check_null(value['longitude']) )]

    assert len(w_t) == len(R_dist_km)

    #print("R_watts:{}".format(R_watts))
    w_t_duration = max(w_t)
    print("w_t_duration:{}".format(w_t_duration))

    return w_t, w_hr, w_kcal, w_kcal_max, w_kcal_aerobic, w_kcal_aerobic_max, w_kcal_anaerobic, w_kcal_anaerobic_max, w_stamina, w_stamina_aerobic, w_stamina_anaerobic, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence

def gomorerunner_json_parsing(src_verified_json_path, src_route_json_path):
    print("[DPM][parse] src_verified_json_path:{}".format(src_verified_json_path))
    
    w_t = []
    w_hr = []
    w_kcal = []
    w_kcal_max = []
    w_kcal_aerobic = []
    w_kcal_aerobic_max = []
    w_kcal_anaerobic = []
    w_kcal_anaerobic_max = []
    w_stamina = []
    w_stamina_aerobic = []
    w_stamina_anaerobic = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []

    # parsing src_verified_json_path
    with open(src_verified_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    # sort by time
    for row in data:
        for key in row.keys():
            if key == "second":
                    row[key] = int(row[key])

    data = sorted(data,key=lambda x:x['second'])

    for value in data:
        w_t += [int(check_null(value['second']))]
        w_hr += [int(check_null(value['heartrate']))]
        w_kcal += [float( check_null(value['kcal']) )]
        w_kcal_max += [float( check_null(value['kcal_max']) )]
        if 'kcal_aerobic' in value:
            w_kcal_aerobic += [float( check_null(value['kcal_aerobic']) )]
        else:
            w_kcal_aerobic += [-1]
        if 'kcal_aerobic_max' in value:
            w_kcal_aerobic_max += [float( check_null(value['kcal_aerobic_max']) )]
        else:
            w_kcal_aerobic_max += [-1]
        if 'kcal_anaerobic' in value:
            w_kcal_anaerobic += [float( check_null(value['kcal_anaerobic']) )]
        else:
            w_kcal_anaerobic += [-1]
        if 'kcal_anaerobic_max' in value:
            w_kcal_anaerobic_max += [float( check_null(value['kcal_anaerobic_max']) )]
        else:
            w_kcal_anaerobic_max += [-1]

        w_stamina += [float( check_null(value['stamina']) )]
        w_stamina_aerobic += [float( check_null(value['stamina_aerobic']) )]
        w_stamina_anaerobic += [float( check_null(value['stamina_anaerobic']) )]

    # parsing src_route_json_path
    with open(src_route_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    if data == []:
        for i in range(len(w_t)):
            R_alt_m += [float( check_null('Null') )]
            R_dist_km += [float( check_null('Null') )]
            R_dist_m += [ R_dist_km[-1] * 1000.0 ]
            R_speed_mps += [float( check_null('Null') )]
            R_speed_kmph += [ R_speed_mps[-1] * 3.6 ]
            R_incline += [float( check_null('Null') )]
            R_lat += [float( check_null('Null') )]
            R_lng += [float( check_null('Null') )]
    else:
        for value in data:
            R_alt_m += [float( check_null(value['altitude']) )]
            R_dist_km += [float( check_null(value['distance_km']) )]
            R_dist_m += [ R_dist_km[-1] * 1000.0 ]
            R_speed_mps += [float( check_null(value['speed']) )]
            R_speed_kmph += [ R_speed_mps[-1] * 3.6 ]
            R_incline += [float( check_null(value['geo_incline']) )]
            R_lat += [float( check_null(value['latitude']) )]
            R_lng += [float( check_null(value['longitude']) )]

    assert len(w_t) == len(R_dist_km)

    return w_t, w_hr, w_kcal, w_kcal_max, w_kcal_aerobic, w_kcal_aerobic_max, w_kcal_anaerobic, w_kcal_anaerobic_max, w_stamina, w_stamina_aerobic, w_stamina_anaerobic, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng

def raw_data_truncation(raw_data_path, raw_data_info_path, truncation_start_sec, truncation_end_sec, raw_data_balck_list_backup_path, raw_data_info_balck_list_backup_path):
    print("[DPM][raw_data_truncation] raw_data_path:{}".format(raw_data_path))
    
    # hadling raw data first
    w_t = []
    w_hr = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []

    f = open(raw_data_balck_list_backup_path, 'rU')
    for row in csv.DictReader(f):
        time_raw = int(check_null(row['w_t']))
        #w_t += [int(check_null(row['w_t']))]

        if time_raw >= truncation_start_sec and time_raw <= truncation_end_sec:
            w_t += [time_raw - truncation_start_sec]

            w_hr += [int(check_null(row['w_hr']))]
            R_alt_m += [float(check_null(row['R_alt_m']))]
            R_dist_m += [float(check_null(row['R_dist_m']))]
            R_dist_km += [float(check_null(row['R_dist_km']))]
            R_speed_mps += [float(check_null(row['R_speed_mps']))]
            R_speed_kmph += [float(check_null(row['R_speed_kmph']))]
            R_incline += [float(check_null(row['R_incline']))]
            R_lat += [float(check_null(row['R_lat']))]
            R_lng += [float(check_null(row['R_lng']))]
    f.close()
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
            
    with open(raw_data_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(w_t)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

    f = open(raw_data_info_balck_list_backup_path, 'rU')
    for row in csv.DictReader(f):

        #workout_date = row['workout_date']
        workout_date = get_data_from_epoch_sec(int(row['workout_time_sec'])+truncation_start_sec)
        workout_time_sec = int(row['workout_time_sec'])+truncation_start_sec
        #workout_duration_sec = int(row['workout_duration_sec'])
        workout_duration_sec = truncation_end_sec - truncation_start_sec + 1
        workout_text = row['workout_text']
        interval_training = row['interval_training']
        answer_breath = int(row['answer_breath'])
        answer_muscle = int(row['answer_muscle'])
        answer_RPE = int(row['answer_RPE'])
        has_heartrate = int(row['has_heartrate'])
        has_distance = int(row['has_distance'])
        has_route = int(row['has_route'])
        has_altitude = int(row['has_altitude'])
    f.close()
    csv_header = []
    csv_header += ["workout_date"]
    csv_header += ["workout_time_sec"]
    csv_header += ["workout_duration_sec"]
    csv_header += ["workout_text"]
    csv_header += ["interval_training"]
    csv_header += ["answer_breath"]
    csv_header += ["answer_muscle"]
    csv_header += ["answer_RPE"]
    csv_header += ["has_heartrate"]
    csv_header += ["has_distance"]
    csv_header += ["has_route"]
    csv_header += ["has_altitude"]
            
    with open(raw_data_info_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        anlysis_result = []
        for col in range(len(csv_header)):
            anlysis_result += [eval(csv_header[col])]
        writer.writerow(anlysis_result)
        csvfile.close()

    #return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng

def ride_raw_data_parsing(raw_data_path):
    print("[DPM][parse] raw_data_path:{}".format(raw_data_path))
    
    w_t = []
    w_hr = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []
    R_watts = []
    R_cadence = []

    f = open(raw_data_path, 'rU')
    for row in csv.DictReader(f):
        w_t += [int(check_null(row['w_t']))]
        w_hr += [int(check_null(row['w_hr']))]
        R_alt_m += [float(check_null(row['R_alt_m']))]
        R_dist_m += [float(check_null(row['R_dist_m']))]
        R_dist_km += [float(check_null(row['R_dist_km']))]
        R_speed_mps += [float(check_null(row['R_speed_mps']))]
        R_speed_kmph += [float(check_null(row['R_speed_kmph']))]
        R_incline += [float(check_null(row['R_incline']))]
        R_lat += [float(check_null(row['R_lat']))]
        R_lng += [float(check_null(row['R_lng']))]
        R_watts += [float(check_null(row['R_watts']))]
        R_cadence += [float(check_null(row['R_cadence']))]
    f.close()

    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence

def run_raw_data_parsing(raw_data_path):
    print("[DPM][parse] raw_data_path:{}".format(raw_data_path))
    
    w_t = []
    w_hr = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []

    f = open(raw_data_path, 'rU')
    for row in csv.DictReader(f):
        w_t += [int(check_null(row['w_t']))]
        w_hr += [int(check_null(row['w_hr']))]
        R_alt_m += [float(check_null(row['R_alt_m']))]
        R_dist_m += [float(check_null(row['R_dist_m']))]
        R_dist_km += [float(check_null(row['R_dist_km']))]
        R_speed_mps += [float(check_null(row['R_speed_mps']))]
        R_speed_kmph += [float(check_null(row['R_speed_kmph']))]
        R_incline += [float(check_null(row['R_incline']))]
        R_lat += [float(check_null(row['R_lat']))]
        R_lng += [float(check_null(row['R_lng']))]
    f.close()

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

    # try to pick route points
    """
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = RFM.picking_route_point_by_limit_accleration(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)
    """
    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng

def raw_data_parsing(raw_data_path):
    print("[DPM][parse] raw_data_path:{}".format(raw_data_path))
    
    w_t = []
    w_hr = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []

    f = open(raw_data_path, 'rU')
    for row in csv.DictReader(f):
        w_t += [int(check_null(row['w_t']))]
        w_hr += [int(check_null(row['w_hr']))]
        R_alt_m += [float(check_null(row['R_alt_m']))]
        R_dist_m += [float(check_null(row['R_dist_m']))]
        R_dist_km += [float(check_null(row['R_dist_km']))]
        R_speed_mps += [float(check_null(row['R_speed_mps']))]
        R_speed_kmph += [float(check_null(row['R_speed_kmph']))]
        R_incline += [float(check_null(row['R_incline']))]
        R_lat += [float(check_null(row['R_lat']))]
        R_lng += [float(check_null(row['R_lng']))]
    f.close()

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

    # try to pick route points
    """
    w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = RFM.picking_route_point_by_limit_accleration(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng)
    """

    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng

def ride_raw_data_info_parsing(raw_data_info_path):
    print("[DPM][parse] raw_data_info_path:{}".format(raw_data_info_path))

    f = open(raw_data_info_path, 'rU')
    for row in csv.DictReader(f):

        workout_date = row['workout_date']
        workout_time_sec = int(row['workout_time_sec'])
        workout_duration_sec = int(row['workout_duration_sec'])
        workout_text = row['workout_text']
        interval_training = row['interval_training']
        answer_breath = int(row['answer_breath'])
        answer_muscle = int(row['answer_muscle'])
        answer_RPE = int(row['answer_RPE'])
        has_heartrate = int(row['has_heartrate'])
        has_distance = int(row['has_distance'])
        has_route = int(row['has_route'])
        has_altitude = int(row['has_altitude'])
        has_power = int(row['has_power'])
        has_cadence = int(row['has_cadence'])
    f.close()

    return workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude, has_power, has_cadence


def raw_data_info_parsing(raw_data_info_path):
    print("[DPM][parse] raw_data_info_path:{}".format(raw_data_info_path))

    f = open(raw_data_info_path, 'rU')
    for row in csv.DictReader(f):

        workout_date = row['workout_date']
        workout_time_sec = int(row['workout_time_sec'])
        workout_duration_sec = int(row['workout_duration_sec'])
        workout_text = row['workout_text']
        interval_training = row['interval_training']
        answer_breath = int(row['answer_breath'])
        answer_muscle = int(row['answer_muscle'])
        answer_RPE = int(row['answer_RPE'])
        has_heartrate = int(row['has_heartrate'])
        has_distance = int(row['has_distance'])
        has_route = int(row['has_route'])
        has_altitude = int(row['has_altitude'])
    f.close()

    return workout_date, workout_time_sec, workout_duration_sec, workout_text, interval_training, answer_breath, answer_muscle, answer_RPE, has_heartrate, has_distance, has_route, has_altitude

def calculation_result_parsing(calculation_result_path):
    print("[DPM][parse] calculation_result_path:{}".format(calculation_result_path))
    
    w_t = []
    w_hr = []
    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []

    stamina_ptc_list = []
    aerobic_ptc_list = []
    anaerobic_ptc_list = []
    max_dist_km_list = []

    f = open(calculation_result_path, 'rU')
    for row in csv.DictReader(f):
        w_t += [int(check_null(row['w_t']))]
        w_hr += [int(check_null(row['w_hr']))]
        R_alt_m += [float(check_null(row['R_alt_m']))]
        R_dist_m += [float(check_null(row['R_dist_m']))]
        R_dist_km += [float(check_null(row['R_dist_km']))]
        R_speed_mps += [float(check_null(row['R_speed_mps']))]
        R_speed_kmph += [float(check_null(row['R_speed_kmph']))]
        R_incline += [float(check_null(row['R_incline']))]
        R_lat += [float(check_null(row['R_lat']))]
        R_lng += [float(check_null(row['R_lng']))]
        stamina_ptc_list += [float(check_null(row['stamina_ptc_list']))]
        aerobic_ptc_list += [float(check_null(row['aerobic_ptc_list']))]
        anaerobic_ptc_list += [float(check_null(row['anaerobic_ptc_list']))]
        max_dist_km_list += [float(check_null(row['max_dist_km_list']))]
    f.close()

    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, stamina_ptc_list, aerobic_ptc_list, anaerobic_ptc_list, max_dist_km_list

def calculation_statistics_parsing(calculation_statistics_path):
    print("[DPM][parse] calculation_statistics_parsing:{}".format(calculation_statistics_path))
    f = open(calculation_statistics_path, 'rU')
    for row in csv.DictReader(f):

        vdot_3km = float(row['vdot_3km'])
        vdot_5km = float(row['vdot_5km'])
        vdot_10km = float(row['vdot_10km'])
        vdot_15km = float(row['vdot_15km'])
        vdot_half_marathon = float(row['vdot_half_marathon'])
        vdot_25km = float(row['vdot_25km'])
        vdot_30km = float(row['vdot_30km'])
        vdot_35km = float(row['vdot_35km'])
        vdot_full_marathon = float(row['vdot_full_marathon'])

        vdot_CP8 = float(row['vdot_CP8'])
        vdot_CP20 = float(row['vdot_CP20'])
        vdot_CP60 = float(row['vdot_CP60'])
        vdot_CP120 = float(row['vdot_CP120'])
        vdot_CP180 = float(row['vdot_CP180'])

    f.close()

    return vdot_3km, vdot_5km, vdot_10km, vdot_15km, vdot_half_marathon, vdot_25km, vdot_30km, vdot_35km, vdot_full_marathon, vdot_CP8, vdot_CP20, vdot_CP60, vdot_CP120, vdot_CP180


def user_status_in_server_parsing(user_status_path):
    print("[DPM][parse] user_status_path:{}".format(user_status_path))

    f = open(user_status_path, 'rU')
    for row in csv.DictReader(f):
        
        last_workout_time_sec = int(row['last_workout_time_sec'])
        last_workout_duration_sec = int(row['last_workout_duration_sec'])
        last_max_hr = int(row['last_max_hr'])
        last_rest_hr = int(row['last_rest_hr'])
        last_aero_capacity = float(row['last_aero_capacity'])
        last_aero_total_capacity = float(row['last_aero_total_capacity'])
        last_LA_dilution_grade = float(row['last_LA_dilution_grade'])
        last_anaerobic_ptc = float(row['last_anaerobic_ptc'])
        last_stamina_level = float(row['last_stamina_level'])
        last_first_time_calibration = int(row['last_first_time_calibration'])

    return last_workout_time_sec, last_workout_duration_sec, last_max_hr, last_rest_hr, last_aero_capacity, last_aero_total_capacity, last_LA_dilution_grade, last_anaerobic_ptc, last_stamina_level, last_first_time_calibration

def user_run_status_parsing(user_status_path):
    print("[DPM][parse] user_status_path:{}".format(user_status_path))

    f = open(user_status_path, 'rU')
    for row in csv.DictReader(f):
        
        last_workout_time_sec = int(row['last_workout_time_sec'])
        last_workout_duration_sec = int(row['last_workout_duration_sec'])
        last_workout_dir = (row['last_workout_dir'])
        last_anaerobic_ptc = float(row['last_anaerobic_ptc'])
        last_aerobic_ptc = float(row['last_aerobic_ptc'])
        last_run_max_HR = float(row['last_run_max_HR'])
        last_run_rest_HR = float(row['last_run_rest_HR'])
        last_run_aero_total_capacity = float(row['last_run_aero_total_capacity'])
        last_run_LA_dilution_grade = float(row['last_run_LA_dilution_grade'])
        last_run_stamina_level = float(row['last_run_stamina_level'])
        last_run_first_time_calibration = float(row['last_run_first_time_calibration'])

    return last_workout_time_sec,last_workout_duration_sec,last_workout_dir,last_anaerobic_ptc,last_aerobic_ptc,last_run_max_HR,last_run_rest_HR,last_run_aero_total_capacity,last_run_LA_dilution_grade,last_run_stamina_level,last_run_first_time_calibration

def user_status_parsing(user_status_path):
    print("[DPM][parse] user_status_path:{}".format(user_status_path))

    f = open(user_status_path, 'rU')
    for row in csv.DictReader(f):
        
        last_workout_time_sec = int(row['last_workout_time_sec'])
        last_workout_duration_sec = int(row['last_workout_duration_sec'])
        last_max_hr = int(row['last_max_hr'])
        last_rest_hr = int(row['last_rest_hr'])
        last_aero_capacity = float(row['last_aero_capacity'])
        last_aero_total_capacity = float(row['last_aero_total_capacity'])
        last_LA_dilution_grade = float(row['last_LA_dilution_grade'])
        last_anaerobic_ptc = float(row['last_anaerobic_ptc'])
        last_stamina_level = float(row['last_stamina_level'])
        last_first_time_calibration = int(row['last_first_time_calibration'])

    return last_workout_time_sec, last_workout_duration_sec, last_max_hr, last_rest_hr, last_aero_capacity, last_aero_total_capacity, last_LA_dilution_grade, last_anaerobic_ptc, last_stamina_level, last_first_time_calibration


def strava_run_and_ride_json_parsing(workout_json_path, workout_info_path):
    # parse workout_json_path
    print("[DPM][parse] workout_json_path:{}".format(workout_json_path))
    with open(workout_json_path) as data_file:
        data = json.load(data_file) 
    data_file.close()

    w_t = []
    w_hr = []

    R_alt_m = []
    R_dist_m = []
    R_dist_km = []
    R_speed_mps = []
    R_speed_kmph = []
    R_incline = []
    R_lat = []
    R_lng = []
    R_watts = []
    R_cadence = []

    for value in data:
        w_t += [int(check_null(value['time']))]
        w_hr += [int(check_null(value['heartrate']))]
        R_alt_m += [float(check_null(value['altitude']))]
        R_dist_m += [float(check_null(value['distance']))]
        R_dist_km += [R_dist_m[-1]/1000.0]
        R_speed_mps += [float(check_null(value['velocity_smooth']))]
        R_speed_kmph += [R_speed_mps[-1]*3.6]
        R_incline += [float(check_null(value['grade_smooth']))]
        R_lat += [float(check_null(value['lat']))]
        R_lng += [float(check_null(value['lng']))]
        R_watts += [float(check_null(value['watts']))]
        R_cadence += [float(check_null(value['cadence']))]


    #print("w_t:{}".format(w_t))

    # parse workout_info_path
    if os.path.exists(workout_info_path):
        f = open(workout_info_path)
        info = json.load(f)

        workout_date = info["start_date_local"]
        print("[DPM]time:{}".format(workout_date))
        workout_time_sec = get_epoch_sec(dateutil.parser.parse(workout_date))
        print("[DPM]workout_time_sec:{}".format(workout_time_sec))

        workout_text = info["name"].encode('utf8')
        #print("workout_text:{}".format(workout_text))

    if len(w_t) == 0:
        workout_duration_sec = 0
    else:
        workout_duration_sec = max(w_t)


    return workout_date, workout_time_sec, workout_duration_sec, workout_text, w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence

# /Users/Scott/git_repositories/test_workspace/downloading_gomorerunner_server/workout_data/2128_ Kumtorn Natee/run_4835__ 13.40km_ 471.08pace_ 132bpm/2128_582d17c41f748_verified.zip

def unzipfile(zip_path, extract_dir):
    zf = zipfile.ZipFile(zip_path)
    zf.extractall(extract_dir)

'''
zip_path = '/Users/Scott/git_repositories/test_workspace/downloading_gomorerunner_server/workout_data/2128_ Kumtorn Natee/run_4835__ 13.40km_ 471.08pace_ 132bpm/2128_582d17c41f748_verified.zip'
extract_dir = '/Users/Scott/git_repositories/test_workspace/downloading_gomorerunner_server/workout_data/2128_ Kumtorn Natee/run_4835__ 13.40km_ 471.08pace_ 132bpm/'
unzipfile(zip_path, extract_dir)
'''

###########################################


def ride_data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence):

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
    R_watts_padding = []
    R_cadence_padding = []

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
            R_watts_padding += [R_watts[i]]
            R_cadence_padding += [R_cadence[i]]
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
                    R_watts_padding += [R_watts_padding[-1]]
                    R_cadence_padding += [R_cadence_padding[-1]]
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
                R_watts_padding += [R_watts[i]]
                R_cadence_padding += [R_cadence[i]]
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
                R_watts_padding += [R_watts[i]]
                R_cadence_padding += [R_cadence[i]]
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
    R_watts = R_watts_padding
    R_cadence = R_cadence_padding
    #print("len(w_hr):{}".format(len(w_hr)))
    #print("max(w_hr):{}".format(max(w_hr)))

    return w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence


def run_data_padding(w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng):

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


def get_list_user_ride_grade_search_path(stamina_lib_analysis_dir, user_setting_table_path):
    list_user_ride_grade_search_path = []
    list_user_name = []

    user_setting_table = open(user_setting_table_path, 'Urb')

    for row in csv.DictReader(user_setting_table):
        name = row["dst_name_list"]
        print("name:{}".format(name))
        list_user_name += [name]
        user_dir = stamina_lib_analysis_dir + '{}/'.format(name)

        user_ride_grade_search_path = user_dir + 'user_ride_grade_search.csv'

        list_user_ride_grade_search_path += [user_ride_grade_search_path]


    user_setting_table.close()

    return list_user_ride_grade_search_path, list_user_name

def parse_user_ride_grade_search(user_ride_grade_search_path):
    
    print("[DPM][parse_user_ride_grade_search] user_ride_grade_search_path:{}".format(user_ride_grade_search_path))

    list_end_LA_dilution_grade = []
    list_min_positive_sta_grade = []
    list_grade_predict_error = []

    workout_ride_dir_list = []
    list_sim_mean_watts_hrrVDOT = []
    list_sim_mean_watts_CP20 = []
    list_mean_hr_max_stable = []
    list_mean_hrr_ptc_max_stable = []
    list_max_HR = []
    list_rest_HR = []
    list_sim_mean_watts_max_stable = []
    list_avg_R_incline_p_max_stable = []
    list_age = []
    list_gender = []
    list_weight = []
    list_height = []
    list_avg_R_speed_kmph_p_max_stable = []


    f = open(user_ride_grade_search_path, 'rU')
    for row in csv.DictReader(f):
        list_end_LA_dilution_grade += [int(row['list_end_LA_dilution_grade'])]
        list_min_positive_sta_grade += [int(row['list_min_positive_sta_grade'])]
        list_grade_predict_error += [int(row['list_grade_predict_error'])]

        workout_ride_dir_list += [row['workout_ride_dir_list']]
        list_sim_mean_watts_hrrVDOT += [float(row['list_sim_mean_watts_hrrVDOT'])]
        list_sim_mean_watts_CP20 += [float(row['list_sim_mean_watts_CP20'])]
        list_mean_hr_max_stable += [float(row['list_mean_hr_max_stable'])]
        list_mean_hrr_ptc_max_stable += [float(row['list_mean_hrr_ptc_max_stable'])]
        list_max_HR += [float(row['list_max_HR'])]
        list_rest_HR += [float(row['list_rest_HR'])]
        list_sim_mean_watts_max_stable += [float(row['list_sim_mean_watts_max_stable'])]
        list_avg_R_incline_p_max_stable += [float(row['list_avg_R_incline_p_max_stable'])]
        list_age += [float(row['list_age'])]
        list_gender += [float(row['list_gender'])]
        list_weight += [float(row['list_weight'])]
        list_height += [float(row['list_height'])]
        list_avg_R_speed_kmph_p_max_stable += [float(row['list_avg_R_speed_kmph_p_max_stable'])]

    f.close()

    return workout_ride_dir_list,list_end_LA_dilution_grade,list_min_positive_sta_grade,list_grade_predict_error,list_sim_mean_watts_hrrVDOT,list_sim_mean_watts_CP20,list_mean_hr_max_stable,list_mean_hrr_ptc_max_stable,list_max_HR,list_rest_HR,list_sim_mean_watts_max_stable,list_avg_R_incline_p_max_stable, list_age, list_gender, list_weight, list_height, list_avg_R_speed_kmph_p_max_stable


# test only 
"""



'''
dst_raw_HR_path = '/Users/Scott/git_repositories/gomore_raw_data/14_HsinFu.Kuo/Ride_7780_25.07km_21.54kmph_155bpm/raw_HR.json'
dst_raw_route_path = '/Users/Scott/git_repositories/gomore_raw_data/14_HsinFu.Kuo/Ride_7780_25.07km_21.54kmph_155bpm/raw_route.json'
workout_duration_sec = 4189

gomore_json_parsing(dst_raw_HR_path, dst_raw_route_path, workout_duration_sec)
'''
dst_raw_HR_path = '/Users/Scott/git_repositories/gomore_raw_data/14_HsinFu.Kuo/Ride_348_32.48km_12.7kmph_163bpm/raw_HR.json'
dst_raw_route_path = '/Users/Scott/git_repositories/gomore_raw_data/14_HsinFu.Kuo/Ride_348_32.48km_12.7kmph_163bpm/raw_route.json'
workout_duration_sec = 9210

dst_workout_data_csv_path = '/Users/Scott/git_repositories/gomore_raw_data/14_HsinFu.Kuo/Ride_348_32.48km_12.7kmph_163bpm/raw_data.csv'

w_t, w_hr, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence = gomore_json_parsing(dst_raw_HR_path, dst_raw_route_path, workout_duration_sec)

# workout raw dump ##################################
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
csv_header += ["R_watts"]
csv_header += ["R_cadence"]
        
with open(dst_workout_data_csv_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in range(len(w_t)+1):
        data = []
        if row == 0:
            data = csv_header
        else:
            for col in range(len(csv_header)):
                data += [eval(csv_header[col])[row-1]]
        writer.writerow(data)
    csvfile.close()
# test only end


"""









