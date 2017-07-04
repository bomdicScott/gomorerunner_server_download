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












