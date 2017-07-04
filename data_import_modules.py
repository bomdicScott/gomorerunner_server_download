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


def update_user_setting_with_init(dst_user_setting_table_path, src_user_ID, src_user_name, age, gender, weight, height, max_HR):

    if max_HR == None:
        max_HR = -1

    # update user_setting.csv
    dst_user_ID_list = []
    dst_name_list = []
    dst_age_list = []
    dst_gender_list = []
    dst_weight_list = []
    dst_height_list = []

    dst_anaerobic_ptc_list = []
    dst_aerobic_ptc_list = []

    dst_run_max_HR_list = []
    dst_run_rest_HR_list = []
    dst_run_aero_total_capacity_list = []
    dst_run_LA_dilution_grade_list = []    
    dst_run_stamina_level_list = []

    dst_ride_max_HR_list = []
    dst_ride_rest_HR_list = []
    dst_ride_aero_total_capacity_list = []
    dst_ride_LA_dilution_grade_list = []    
    dst_ride_stamina_level_list = []

    has_user_ID_tag = -1
    if os.path.exists(dst_user_setting_table_path):
        # open csv
        f = open(dst_user_setting_table_path, 'rU')
        for row in csv.DictReader(f): 
            #print(row)
            dst_user_ID_list += [row['dst_user_ID_list']]
            dst_name_list += [row['dst_name_list']]
            dst_age_list += [row['dst_age_list']]
            dst_gender_list += [row['dst_gender_list']]
            dst_weight_list += [row['dst_weight_list']]
            dst_height_list += [row['dst_height_list']]
            
            dst_anaerobic_ptc_list += [row['dst_anaerobic_ptc_list']]
            dst_aerobic_ptc_list += [row['dst_aerobic_ptc_list']]

            dst_run_max_HR_list += [row['dst_run_max_HR_list']]
            dst_run_rest_HR_list += [row['dst_run_rest_HR_list']]
            dst_run_aero_total_capacity_list += [row['dst_run_aero_total_capacity_list']]
            dst_run_LA_dilution_grade_list += [row['dst_run_LA_dilution_grade_list']]
            dst_run_stamina_level_list += [row['dst_run_stamina_level_list']]

            dst_ride_max_HR_list += [row['dst_ride_max_HR_list']]
            dst_ride_rest_HR_list += [row['dst_ride_rest_HR_list']]
            dst_ride_aero_total_capacity_list += [row['dst_ride_aero_total_capacity_list']]
            dst_ride_LA_dilution_grade_list += [row['dst_ride_LA_dilution_grade_list']]
            dst_ride_stamina_level_list += [row['dst_ride_stamina_level_list']]

            if src_user_ID == row['dst_user_ID_list']:
                has_user_ID_tag = 1
        f.close()

    # age, gender, weight, height, max_HR

    if has_user_ID_tag == -1:
        dst_user_ID_list += [src_user_ID]
        dst_name_list += [src_user_name]
        dst_age_list += [age]
        dst_gender_list += [gender]
        dst_weight_list += [weight]
        dst_height_list += [height]
        
        dst_anaerobic_ptc_list += [100]
        dst_aerobic_ptc_list += [100]

        dst_run_max_HR_list += [max_HR]
        dst_run_rest_HR_list += [-1]
        dst_run_aero_total_capacity_list += [-1]
        dst_run_LA_dilution_grade_list += [-1]
        dst_run_stamina_level_list += [-1]

        dst_ride_max_HR_list += [max_HR]
        dst_ride_rest_HR_list += [-1]
        dst_ride_aero_total_capacity_list += [-1]
        dst_ride_LA_dilution_grade_list += [-1]
        dst_ride_stamina_level_list += [-1]

    csv_header = []
    csv_header += ["dst_user_ID_list"]
    csv_header += ["dst_name_list"]
    csv_header += ["dst_age_list"]
    csv_header += ["dst_gender_list"]
    csv_header += ["dst_weight_list"]
    csv_header += ["dst_height_list"]

    csv_header += ["dst_anaerobic_ptc_list"]
    csv_header += ["dst_aerobic_ptc_list"]

    csv_header += ["dst_run_max_HR_list"]
    csv_header += ["dst_run_rest_HR_list"]
    csv_header += ["dst_run_aero_total_capacity_list"]
    csv_header += ["dst_run_LA_dilution_grade_list"]
    csv_header += ["dst_run_stamina_level_list"]

    csv_header += ["dst_ride_max_HR_list"]
    csv_header += ["dst_ride_rest_HR_list"]
    csv_header += ["dst_ride_aero_total_capacity_list"]
    csv_header += ["dst_ride_LA_dilution_grade_list"]
    csv_header += ["dst_ride_stamina_level_list"]
            
    with open(dst_user_setting_table_path, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(dst_user_ID_list)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

def update_user_setting(dst_user_setting_table_path, src_user_ID, src_user_name):

    # update user_setting.csv
    dst_user_ID_list = []
    dst_name_list = []
    dst_age_list = []
    dst_gender_list = []
    dst_weight_list = []
    dst_height_list = []

    dst_anaerobic_ptc_list = []
    dst_aerobic_ptc_list = []

    dst_run_max_HR_list = []
    dst_run_rest_HR_list = []
    dst_run_aero_total_capacity_list = []
    dst_run_LA_dilution_grade_list = []    
    dst_run_stamina_level_list = []

    dst_ride_max_HR_list = []
    dst_ride_rest_HR_list = []
    dst_ride_aero_total_capacity_list = []
    dst_ride_LA_dilution_grade_list = []    
    dst_ride_stamina_level_list = []

    has_user_ID_tag = -1
    if os.path.exists(dst_user_setting_table_path):
        # open csv
        f = open(dst_user_setting_table_path, 'rU')
        for row in csv.DictReader(f): 
            #print(row)
            dst_user_ID_list += [row['dst_user_ID_list']]
            dst_name_list += [row['dst_name_list']]
            dst_age_list += [row['dst_age_list']]
            dst_gender_list += [row['dst_gender_list']]
            dst_weight_list += [row['dst_weight_list']]
            dst_height_list += [row['dst_height_list']]
            
            dst_anaerobic_ptc_list += [row['dst_anaerobic_ptc_list']]
            dst_aerobic_ptc_list += [row['dst_aerobic_ptc_list']]

            dst_run_max_HR_list += [row['dst_run_max_HR_list']]
            dst_run_rest_HR_list += [row['dst_run_rest_HR_list']]
            dst_run_aero_total_capacity_list += [row['dst_run_aero_total_capacity_list']]
            dst_run_LA_dilution_grade_list += [row['dst_run_LA_dilution_grade_list']]
            dst_run_stamina_level_list += [row['dst_run_stamina_level_list']]

            dst_ride_max_HR_list += [row['dst_ride_max_HR_list']]
            dst_ride_rest_HR_list += [row['dst_ride_rest_HR_list']]
            dst_ride_aero_total_capacity_list += [row['dst_ride_aero_total_capacity_list']]
            dst_ride_LA_dilution_grade_list += [row['dst_ride_LA_dilution_grade_list']]
            dst_ride_stamina_level_list += [row['dst_ride_stamina_level_list']]

            if src_user_ID == row['dst_user_ID_list']:
                has_user_ID_tag = 1
        f.close()

    if has_user_ID_tag == -1:
        dst_user_ID_list += [src_user_ID]
        dst_name_list += [src_user_name]
        dst_age_list += [-1]
        dst_gender_list += [-1]
        dst_weight_list += [-1]
        dst_height_list += [-1]
        
        dst_anaerobic_ptc_list += [-1]
        dst_aerobic_ptc_list += [-1]

        dst_run_max_HR_list += [-1]
        dst_run_rest_HR_list += [-1]
        dst_run_aero_total_capacity_list += [-1]
        dst_run_LA_dilution_grade_list += [-1]
        dst_run_stamina_level_list += [-1]

        dst_ride_max_HR_list += [-1]
        dst_ride_rest_HR_list += [-1]
        dst_ride_aero_total_capacity_list += [-1]
        dst_ride_LA_dilution_grade_list += [-1]
        dst_ride_stamina_level_list += [-1]

    csv_header = []
    csv_header += ["dst_user_ID_list"]
    csv_header += ["dst_name_list"]
    csv_header += ["dst_age_list"]
    csv_header += ["dst_gender_list"]
    csv_header += ["dst_weight_list"]
    csv_header += ["dst_height_list"]

    csv_header += ["dst_anaerobic_ptc_list"]
    csv_header += ["dst_aerobic_ptc_list"]

    csv_header += ["dst_run_max_HR_list"]
    csv_header += ["dst_run_rest_HR_list"]
    csv_header += ["dst_run_aero_total_capacity_list"]
    csv_header += ["dst_run_LA_dilution_grade_list"]
    csv_header += ["dst_run_stamina_level_list"]

    csv_header += ["dst_ride_max_HR_list"]
    csv_header += ["dst_ride_rest_HR_list"]
    csv_header += ["dst_ride_aero_total_capacity_list"]
    csv_header += ["dst_ride_LA_dilution_grade_list"]
    csv_header += ["dst_ride_stamina_level_list"]
            
    with open(dst_user_setting_table_path, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(dst_user_ID_list)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

def add_first_workout_table(dst_user_name, dst_workouts_table_path, dst_workout_name):
    with open(dst_workouts_table_path,'w') as dst_workouts_table:
        csv.writer(dst_workouts_table).writerow([dst_workout_name])
        dst_workouts_table.close()


def workout_table_update(dst_user_name, dst_workouts_table_path, dst_workout_name):

    workout_list = []
    has_workout_tag = -1
    if os.path.exists(dst_workouts_table_path):
        dst_workouts_table = open(dst_workouts_table_path,'Ur')
        for workout_name_L in csv.reader(dst_workouts_table):

            #print("workout_name_L:{}".format(workout_name_L))
            if workout_name_L[0] == dst_workout_name:
                has_workout_tag = 1
            workout_list += [workout_name_L]
        dst_workouts_table.close()

    # table update
    if has_workout_tag == 1:
        print("[User:{}][Workout:{} exists!]".format(dst_user_name,dst_workout_name))
    else:
        workout_list += [[dst_workout_name]]
        with open(dst_workouts_table_path,'w') as dst_workouts_table:
            csv.writer(dst_workouts_table).writerows(workout_list)
            dst_workouts_table.close()

    return has_workout_tag





