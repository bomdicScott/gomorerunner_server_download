# -*- coding: utf-8 -*-

import csv
import numpy as np
import json
import math
import os, sys
import itertools
import dateutil
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import urllib2
from BeautifulSoup import BeautifulSoup
from staticmap.staticmap import *
import zipfile
from shutil import copyfile

import data_parsing_modules as DPM
import single_workout_plot as SWP
import data_analysis_modules as DAM
import gomorerunner_server_download_modules as GSDM

print("sys.version:{}".format(sys.version))


##############################################################
v2_backend_URL_root = 'http://api.gomore.me/v2/backend/'
#v2_backend_URL_root = 'http://qa.bomdic.com/develop/backend/'
#v2_backend_URL_root = 'http://rin.bomdic.com/develop/backend/'
#user_ID = '2128'
#user_ID = '945'
#user_ID = '2139' #Ronnie
#user_ID = '1603' #incline / auto pause test
#user_ID = '423' #Scott
#user_ID = '49' #Scott
#user_ID = '2231' #Yothin
#user_ID = '2204' #Albert
#user_ID = '2244' #Albert 2
#user_ID = '1603' # speed check
#user_ID = '384' # strava pace error
#user_ID = '54' #Eddy test
#user_ID = '163' #Eddy test
#user_ID = '154' #Jason test
#user_ID = '287' #5k runner test
user_ID = '79' #Nick

# Jason test
#range_start_date = datetime.datetime(2013, 2, 22, 0, 0, 0)
#range_end_date = datetime.datetime(2015, 3, 1, 23, 59, 59)

# Nick demo
range_start_date = datetime.datetime(2017, 6, 26, 0, 0, 0)
range_end_date = datetime.datetime(2017, 6, 26, 23, 59, 59)

#range_start_date = datetime.datetime(2015, 1, 3, 0, 0, 0)
#range_end_date = datetime.datetime(2015, 1, 3, 23, 59, 59)

re_download = 1
raw_download_dir = "./test_data/"

########### server setting ###########
response = urllib2.urlopen(v2_backend_URL_root + 'user.php?user_id=' + user_ID + '&submit=Submit')
page = response.read()
soup = BeautifulSoup(page)

user_name = GSDM.get_user_name(soup)
print('user_name:{}'.format(user_name))


user_dir = raw_download_dir + '/{}_gomorerunner_{}/'.format(user_ID,user_name)
user_list_path = raw_download_dir + 'gomorerunner_user.csv'


# update gomorerunner_user.csv
GSDM.update_user_list(user_list_path, user_ID, user_name)

# check user folder and update user.csv
if not os.path.exists(user_dir):   
    os.makedirs(user_dir)


workout_dict = GSDM.get_workout_dict(soup, range_start_date, range_end_date)
print("workout_dict:{}".format(workout_dict))


for key, value in workout_dict.iteritems():
    user_workout_id = str(key)
    type_id = str(value)

    # http://api.gomore.me/v2/backend/workout.php?user_workout_id=4579
    response = urllib2.urlopen(v2_backend_URL_root+'workout.php?user_workout_id=' + user_workout_id)
    page = response.read()
    soup = BeautifulSoup(page)
    
    heart_rate_avg,distance_km,file_Route_HR_verified,pace_avg,pace_avg_min,pace_avg_sec,mission_name, laDilutionGrade, LA_dilution_grade, aeroCapacity, aero_capacity, aeroTotalCapacity, aero_total_capacity, valid_calibration, stamina_max_use, stamina_aerobic_max_use, stamina_anaerobic_max_use, stamina_level, aerobic_level, anaerobic_level = GSDM.get_workout_description(soup)
    print('user_workout_id:{}, type_id:{}'.format(user_workout_id, type_id))
    print('heart_rate_avg:{}'.format(heart_rate_avg))
    print('distance_km:{}'.format(distance_km))
    print('file_Route_HR_verified:{}'.format(file_Route_HR_verified))
    print('pace_avg:{}'.format(pace_avg))
    print('mission_name:{}'.format(mission_name))

    session_vdot_url, user_object_url = GSDM.get_workout_urls(soup)
    print("session_vdot_url:{}".format(session_vdot_url))
    print("user_object_url:{}".format(user_object_url))

    
    # update workout list
    user_workout_list_path = user_dir + 'direct_table.csv'

    if 'run' in type_id:
        if mission_name != '':
            workout_dir_s = 'Run_{}_{}_{}km_{:d}.{:02d}pace_{}bpm'.format(user_workout_id, mission_name, distance_km, pace_avg_min, pace_avg_sec, heart_rate_avg)
        else:
            workout_dir_s = 'Run_{}_{}km_{:d}.{:02d}pace_{}bpm'.format(user_workout_id, distance_km, pace_avg_min, pace_avg_sec, heart_rate_avg)
    elif 'cycle' in type_id:
        if mission_name != '':
            workout_dir_s = 'Ride_{}_{}_{}km_{:d}.{:02d}pace_{}bpm'.format(user_workout_id, mission_name, distance_km, pace_avg_min, pace_avg_sec, heart_rate_avg)
        else:
            workout_dir_s = 'Ride_{}_{}km_{:d}.{:02d}pace_{}bpm'.format(user_workout_id, distance_km, pace_avg_min, pace_avg_sec, heart_rate_avg)


    workout_dir = user_dir + '/{}/'.format(workout_dir_s)

    has_workout_tag = GSDM.update_workout_list(user_workout_list_path, workout_dir_s, user_workout_id)

    if has_workout_tag == -1 or re_download == 1:
        # check workout folder
        if not os.path.exists(workout_dir):
            os.makedirs(workout_dir)

        # download files
        user_obj_json_path = workout_dir + 'user_object_server.json'
        vdot_list_json_path = workout_dir + 'session_vdot_server.json'

        if session_vdot_url != 'NA':
            session_vdot_url = GSDM.download_file(session_vdot_url, vdot_list_json_path)
        if user_object_url != 'NA':
            user_object_url = GSDM.download_file(user_object_url, user_obj_json_path)
        GSDM.download_file(file_Route_HR_verified, workout_dir + 'workout_data_verified.zip')

        # upzip
        GSDM.unzipfile(workout_dir + 'workout_data_verified.zip', 
                  workout_dir + 'workout_data_verified/')
        data_verified_dir = workout_dir + 'workout_data_verified/'
        
        verified_json_path = workout_dir + 'file_STA_HR_Kcal_verified.json'
        route_json_path = workout_dir + 'file_route.json'

        copyfile(data_verified_dir + 'file_route', route_json_path)
        copyfile(data_verified_dir + 'file_STA_HR_Kcal_verified', verified_json_path)

        
        # call workout parsing module ##################################
        # parsing workout raw data
        if 'Run' in workout_dir:
            w_t, w_hr, w_kcal, w_kcal_max, w_kcal_aerobic, w_kcal_aerobic_max, w_kcal_anaerobic, w_kcal_anaerobic_max, w_stamina, w_stamina_aerobic, w_stamina_anaerobic, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng = DPM.gomorerunner_json_parsing(verified_json_path, route_json_path)
        elif 'Ride' in workout_dir:
            w_t, w_hr, w_kcal, w_kcal_max, w_kcal_aerobic, w_kcal_aerobic_max, w_kcal_anaerobic, w_kcal_anaerobic_max, w_stamina, w_stamina_aerobic, w_stamina_anaerobic, R_alt_m, R_dist_m, R_dist_km, R_speed_mps, R_speed_kmph, R_incline, R_lat, R_lng, R_watts, R_cadence = DPM.gomorerider_json_parsing(verified_json_path, route_json_path)

        w_stamina_end = w_stamina[-1]
        w_stamina_aerobic_end = w_stamina_aerobic[-1]
        w_stamina_anaerobic_end = w_stamina_anaerobic[-1]
        #w_stamina_RPE

        # parsing workout raw data info
        if user_object_url != 'NA' and session_vdot_url != 'NA':
            workout_date, workout_time_sec, workout_duration_sec, workout_text, answer_breath, answer_muscle, answer_RPE = DPM.gomorerunner_info_parsing(user_obj_json_path)
        else:
            workout_date = 'ND'
            workout_time_sec = 'ND'
            workout_duration_sec = 'ND'
            workout_text = 'ND'
            answer_breath = 'ND'
            answer_muscle = 'ND'
            answer_RPE = 'ND'

        
        # parsing user status before workout of server record
        # 
        if user_object_url != 'NA' and session_vdot_url != 'NA':
            last_workout_time_sec,last_workout_duration_sec,last_workout_dir,last_max_hr,last_rest_hr,last_aero_total_capacity,last_aero_capacity,last_LA_dilution_grade,last_anaerobic_ptc,last_stamina_level,last_first_time_calibration = DPM.gomorerunner_status_parsing(user_obj_json_path, vdot_list_json_path)
        else:
            last_workout_time_sec = 'ND'
            last_workout_duration_sec = 'ND'
            last_workout_dir = 'ND'
            last_max_hr = 'ND'
            last_rest_hr = 'ND'
            last_aero_total_capacity = 'ND'
            last_aero_capacity = 'ND'
            last_LA_dilution_grade = 'ND'
            last_anaerobic_ptc = 'ND'
            last_stamina_level = 'ND'
            last_first_time_calibration = 'ND'

        # default value
        interval_training = 'NA'

        # data simple scan
        has_heartrate = 1
        has_distance = 1
        has_route = 1
        has_altitude = 1
        if len(w_hr) == 0 or max(w_hr) == 0:
            has_heartrate = 0
        if len(R_dist_km) == 0 or max(R_dist_km) == 0:
            has_distance = 0
        if len(R_lat) == 0 or max(R_lat) == 0:
            has_route = 0
        if len(R_alt_m) == 0 or max(R_alt_m) == 0:
            has_altitude = 0

        # write server algorithm summary
        server_algorithm_summary_path = workout_dir + 'server_algorithm_summary.csv'
        GSDM.write_algorithm_summary(server_algorithm_summary_path, laDilutionGrade, LA_dilution_grade, aeroCapacity, aero_capacity, aeroTotalCapacity, aero_total_capacity, valid_calibration, stamina_max_use, stamina_aerobic_max_use, stamina_anaerobic_max_use, workout_date, workout_time_sec, answer_breath, answer_muscle, answer_RPE, w_stamina_end, w_stamina_aerobic_end, w_stamina_anaerobic_end, stamina_level, aerobic_level, anaerobic_level)


        # workout plot save ##############################
        ##############################
        plot_dir = workout_dir
        #plot_dir = src_workout_dir
        if has_heartrate == 1:
            fig = SWP.get_fig_time_HR_alt(w_t,w_hr,R_alt_m)
            fig.savefig(plot_dir + 'heartrate_time.png')
            plt.close(fig)

            fig = SWP.get_fig_time_stamina_alt(w_t,w_stamina,w_stamina_aerobic,w_stamina_anaerobic,R_alt_m,answer_breath,answer_muscle,answer_RPE,last_first_time_calibration,LA_dilution_grade,aero_total_capacity)
            fig.savefig(plot_dir + 'stamina_time_server_verify.png')
            plt.close(fig)

        if has_heartrate == 1 and has_distance == 1:
            fig = SWP.get_fig_dist_HR_alt(R_dist_km,w_hr,R_alt_m)
            fig.savefig(plot_dir + 'heartrate_dist.png')
            plt.close(fig)

        if has_distance == 1:
            fig = SWP.get_fig_time_speed_alt(w_t,R_speed_kmph,R_alt_m)
            fig.savefig(plot_dir + 'speed_time.png')
            plt.close(fig)

            fig = SWP.get_fig_dist_speed_alt(R_dist_km,R_speed_kmph,R_alt_m)
            fig.savefig(plot_dir + 'speed_dist.png')
            plt.close(fig)

            fig = SWP.get_fig_time_pace_alt(w_t,R_speed_kmph,R_alt_m)
            fig.savefig(plot_dir + 'pace_time.png')
            plt.close(fig)

            fig = SWP.get_fig_dist_pace_alt(R_dist_km,R_speed_kmph,R_alt_m)
            fig.savefig(plot_dir + 'pace_dist.png')
            plt.close(fig)
        
        
        if (
            has_route == 1 and 
            not os.path.exists(plot_dir + 'twoD_route_{}_km.png'.format(R_dist_km[-1]))
           ):
            fig = SWP.get_fig_2D_route(R_lat, R_lng)
            #fig.save(dst_workout_dir + 'twoD_route.png')
            fig.save(plot_dir + 'twoD_route_{}_km.png'.format(R_dist_km[-1]))

        ###### extra plot ######
        R_speed_mps_p, R_speed_kmph_p = DAM.speed_mps_kmph_calculation(w_t, R_dist_m)
        extra_process_output_dir = workout_dir + 'extra_process_output/'
        if not os.path.exists(extra_process_output_dir):   
            os.makedirs(extra_process_output_dir)
        fig = SWP.get_fig_time_speed_alt(w_t,R_speed_kmph_p,R_alt_m)
        fig.savefig(extra_process_output_dir + 'speed_p_time.png')
        plt.close(fig)

        fig = SWP.get_fig_time_pace_alt(w_t,R_speed_kmph_p,R_alt_m)
        fig.savefig(extra_process_output_dir + 'pace_p_time.png')
        plt.close(fig)


        ###### extra plot end ######


# update server algorithm summary list
server_algorithm_summary_list_path = user_dir + 'server_algorithm_summary_list.csv'
user_workout_list_path = user_dir + 'direct_table.csv'

# require sorting!!
GSDM.update_server_algorithm_summary_list(user_dir, server_algorithm_summary_list_path, user_workout_list_path)
























