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

def t_sorted(to_be_sorted_list, time_sec_list):

    return [sorted_result for (sorted_total_secs, sorted_result) in sorted(zip(time_sec_list, to_be_sorted_list), key=lambda pair: pair[0])]

def get_workout_urls(soup):
    session_vdot_url = 'NA'
    user_object_url = 'NA'
    for link in soup.findAll("a"):
        #print("link:{}".format(link))
        url = link.get('href')
        #print("url:{}".format(url))
        text = link.text
        #print("text:{}".format(text))

        if text == 'Session_VDOT':
            session_vdot_url = url
        elif text == 'User Object':
            user_object_url = url
    return session_vdot_url, user_object_url

def unzipfile(zip_path, extract_dir):
    zf = zipfile.ZipFile(zip_path)
    zf.extractall(extract_dir)

def download_file(url, file_path):
    print("Downloading:{}".format(url))
    try:
        dl_file = urllib2.urlopen(url)

        with open(file_path, 'wb') as output:
            while True:
                data = dl_file.read(4096)
                if data:
                    output.write(data)
                else:
                    break
    except:
        print("[404 Error]:{}".format(url))
        return 'NA'

def update_user_list(user_list_path, user_ID, user_name):
    # update gomorerunner_user.csv
    user_ID_list = []
    full_name_list = []

    has_user_ID_tag = -1
    if os.path.exists(user_list_path):
        # open csv
        f = open(user_list_path, 'rU')
        for row in csv.DictReader(f): 
            user_ID_list += [row['user_ID_list']]
            full_name_list += [row['full_name_list']]
        if user_ID == row['user_ID_list']:
            has_user_ID_tag = 1
        f.close()

    if has_user_ID_tag == -1:
        user_ID_list += [user_ID]
        full_name_list += [user_name]

    csv_header = []
    csv_header += ["user_ID_list"]
    csv_header += ["full_name_list"]
    with open(user_list_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(user_ID_list)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

def update_workout_list(user_workout_list_path, workout_dir_s, user_workout_id):
    workout_ID_list = []
    workout_dir_list = []

    has_workout_ID_tag = -1
    print("user_workout_list_path:{}".format(user_workout_list_path))
    if os.path.exists(user_workout_list_path):
        f = open(user_workout_list_path, 'rU')
        for row in csv.DictReader(f):
            workout_ID_list += [row['workout_ID_list']]
            workout_dir_list += [row['workout_dir_list']]

            if user_workout_id == row['workout_ID_list']:
                has_workout_ID_tag = 1
        f.close()

    if has_workout_ID_tag == -1:
        workout_ID_list += [user_workout_id]
        workout_dir_list += [workout_dir_s]

    csv_header = []
    csv_header += ["workout_ID_list"]
    csv_header += ["workout_dir_list"]

    with open(user_workout_list_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(workout_ID_list)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

    return has_workout_ID_tag

def get_workout_description(soup):
    heart_rate_avg = None
    distance_km = None
    file_Route_HR_verified = None
    pace_avg = None
    mission_name = ''

    laDilutionGrade = None # before workout
    aeroCapacity = None
    aeroTotalCapacity = None

    LA_dilution_grade = None # after workout
    aero_capacity = None
    aero_total_capacity = None

    valid_calibration = None

    stamina_max_use = None
    stamina_aerobic_max_use = None
    stamina_anaerobic_max_use = None

    stamina_level = None
    aerobic_level = None
    anaerobic_level = None

    pre_line_key = None

    for td in soup.findAll("pre"):
        lines = str(td).split("\n")
        for line in lines:
            # print type(line)
            #print "line: " + line
            tokens = line.split("=")
            # print "token numbers: " + str(len(tokens))
            if len(tokens) == 2:
                line_key = tokens[0].strip()
                tokens[1] = tokens[1].strip()
                line_value = (tokens[1].split(";"))[1]
                #print("line_key:{}".format(line_key))
                # print "token1: " + tokens[0].strip()
                # print "token2: " + tokens[1].strip()
                if line_key == '[heartrate_avg]':
                    heart_rate_avg = line_value.strip()
                if line_key == '[distance_km]':
                    distance_km = line_value.strip()
                if line_key == '[file_Route_HR_verified]':
                    file_Route_HR_verified = line_value
                if line_key == '[pace_avg]':
                    pace_avg = line_value.strip()
                if line_key == '[mission_name]':
                    mission_name = line_value
                # summary info
                if line_key == '[laDilutionGrade]':
                    laDilutionGrade = line_value.strip()
                if line_key == '[LA_dilution_grade]':
                    LA_dilution_grade = line_value.strip()
                if line_key == '[aeroCapacity]':
                    aeroCapacity = line_value.strip()
                if line_key == '[aeroTotalCapacity]':
                    aeroTotalCapacity = line_value.strip()
                if line_key == '[aero_capacity]':
                    aero_capacity = line_value.strip()
                if line_key == '[aero_total_capacity]':
                    aero_total_capacity = line_value.strip()
                if line_key == '[valid_calibration]':
                    valid_calibration = line_value.strip()
                if line_key == '[stamina_max_use]':
                    stamina_max_use = line_value.strip()
                if line_key == '[stamina_aerobic_max_use]':
                    stamina_aerobic_max_use = line_value.strip()
                if line_key == '[stamina_anaerobic_max_use]':
                    stamina_anaerobic_max_use = line_value.strip()
                # VDOT levels
                if line_key == '[stamina_level]' and pre_line_key != '[force]':
                    stamina_level = line_value.strip()
                    print("get key of stamina_level")
                if line_key == '[aerobic_level]':
                    aerobic_level = line_value.strip()
                if line_key == '[anaerobic_level]':
                    anaerobic_level = line_value.strip()

                # workout around to avoid get duplicated stamina_level
                pre_line_key = line_key


    print("pace_avg:{}".format(pace_avg))
    pace_avg_min = math.floor(float(pace_avg) / 60.0)
    pace_avg_sec = math.floor(float(pace_avg)) - pace_avg_min*60
    pace_avg_min = int(pace_avg_min)
    pace_avg_sec = int(pace_avg_sec)
    print("pace_avg_min:{}".format(pace_avg_min))
    print("pace_avg_sec:{}".format(pace_avg_sec))
    if float(pace_avg) == -1:
        pace_avg_min = 0
        pace_avg_sec = 0

    return heart_rate_avg,distance_km,file_Route_HR_verified,pace_avg,pace_avg_min,pace_avg_sec,mission_name, laDilutionGrade, LA_dilution_grade, aeroCapacity, aero_capacity, aeroTotalCapacity, aero_total_capacity, valid_calibration, stamina_max_use, stamina_aerobic_max_use, stamina_anaerobic_max_use, stamina_level, aerobic_level, anaerobic_level

def get_workout_dict(soup, range_start_date, range_end_date):
    # get workout list
    workout_dict = {}
    for td in soup.findAll("tbody"):
        for row in td.findAll("tr"):
            cells = row.findAll("td")
            print("cells[7].text:{}".format(cells[7].text))

            workout_date = datetime.datetime.strptime(cells[1].text, "%Y-%m-%d %H:%M:%S")
            if (
                range_start_date <= workout_date <= range_end_date
               ):
                if cells[7].text != '-1.00':
                    workout_dict[cells[0].text] = cells[2].text
                else:
                    print("no calculation for workout:{}".format(cells[0].text))

                """
                and
                not('9316' in cells[0].text) and
                not('9348' in cells[0].text) and
                not('9383' in cells[0].text) and
                not('9403' in cells[0].text) # handling no processing issue
                """


        #print("workout_dict:{}".format(workout_dict))
    return workout_dict

def get_user_name(soup):
    for block in soup.findAll("pre"):
        lines = str(block).split("\n")
        for line in lines:
            tokens = line.split("=")
            if len(tokens) == 2:
                #print("tokens:{}".format(tokens))
                #print("tokens[0]:{}".format(tokens[0]))
                key = tokens[0].strip()
                #print("key:{}".format(key))
                #print("tokens[1]:{}".format(tokens[1]))
                tokens[1] = tokens[1].strip()
                value = (tokens[1].split(";"))[1]
                if key == '[user_name]':
                    user_name = value
    user_name = user_name.replace(' ', '_')
    user_name = user_name[1:] # remove first char
    return user_name


def update_server_algorithm_summary_list(user_dir, server_algorithm_summary_list_path, user_workout_list_path):
    workout_date_list = []
    workout_time_sec_list = []
    laDilutionGrade_list = []
    LA_dilution_grade_list = []
    aeroCapacity_list = []
    aero_capacity_list = []
    aeroTotalCapacity_list = []
    aero_total_capacity_list = []
    valid_calibration_list = []
    stamina_max_use_list = []
    stamina_aerobic_max_use_list = []
    stamina_anaerobic_max_use_list = []
    answer_breath_list = []
    answer_muscle_list = []
    answer_RPE_list = []
    w_stamina_end_list = []
    w_stamina_aerobic_end_list = []
    w_stamina_anaerobic_end_list = []
    stamina_level_list = []
    aerobic_level_list = []
    anaerobic_level_list = []


    workout_dir_list = []
    f = open(user_workout_list_path, 'rU')
    for row in csv.DictReader(f): 
        workout_dir = user_dir + '/{}/'.format(row['workout_dir_list'])
        workout_dir_list += [workout_dir]
    f.close()

    for workout_dir in workout_dir_list:
        f = open(workout_dir+'server_algorithm_summary.csv')
        for row in csv.DictReader(f):
            workout_date_list += [row['workout_date']]
            workout_time_sec_list += [row['workout_time_sec']]
            laDilutionGrade_list += [row['laDilutionGrade']]
            LA_dilution_grade_list += [row['LA_dilution_grade']]
            aeroCapacity_list += [row['aeroCapacity']]
            aero_capacity_list += [row['aero_capacity']]
            aeroTotalCapacity_list += [row['aeroTotalCapacity']]
            aero_total_capacity_list += [row['aero_total_capacity']]
            valid_calibration_list += [row['valid_calibration']]
            stamina_max_use_list += [row['stamina_max_use']]
            stamina_aerobic_max_use_list += [row['stamina_aerobic_max_use']]
            stamina_anaerobic_max_use_list += [row['stamina_anaerobic_max_use']]
            answer_breath_list += [row['answer_breath']]
            answer_muscle_list += [row['answer_muscle']]
            answer_RPE_list += [row['answer_RPE']]
            w_stamina_end_list += [row['w_stamina_end']]
            w_stamina_aerobic_end_list += [row['w_stamina_aerobic_end']]
            w_stamina_anaerobic_end_list += [row['w_stamina_anaerobic_end']]
            stamina_level_list += [row['stamina_level']]
            aerobic_level_list += [row['aerobic_level']]
            anaerobic_level_list += [row['anaerobic_level']]

        f.close()

    workout_dir_list = t_sorted(workout_dir_list, workout_time_sec_list)

    workout_date_list = []
    workout_time_sec_list = []
    laDilutionGrade_list = []
    LA_dilution_grade_list = []
    aeroCapacity_list = []
    aero_capacity_list = []
    aeroTotalCapacity_list = []
    aero_total_capacity_list = []
    valid_calibration_list = []
    stamina_max_use_list = []
    stamina_aerobic_max_use_list = []
    stamina_anaerobic_max_use_list = []
    answer_breath_list = []
    answer_muscle_list = []
    answer_RPE_list = []
    w_stamina_end_list = []
    w_stamina_aerobic_end_list = []
    w_stamina_anaerobic_end_list = []
    stamina_level_list = []
    aerobic_level_list = []
    anaerobic_level_list = []


    for workout_dir in workout_dir_list:
        f = open(workout_dir+'server_algorithm_summary.csv')
        for row in csv.DictReader(f):
            workout_date_list += [row['workout_date']]
            workout_time_sec_list += [row['workout_time_sec']]
            laDilutionGrade_list += [row['laDilutionGrade']]
            LA_dilution_grade_list += [row['LA_dilution_grade']]
            aeroCapacity_list += [row['aeroCapacity']]
            aero_capacity_list += [row['aero_capacity']]
            aeroTotalCapacity_list += [row['aeroTotalCapacity']]
            aero_total_capacity_list += [row['aero_total_capacity']]
            valid_calibration_list += [row['valid_calibration']]
            stamina_max_use_list += [row['stamina_max_use']]
            stamina_aerobic_max_use_list += [row['stamina_aerobic_max_use']]
            stamina_anaerobic_max_use_list += [row['stamina_anaerobic_max_use']]
            answer_breath_list += [row['answer_breath']]
            answer_muscle_list += [row['answer_muscle']]
            answer_RPE_list += [row['answer_RPE']]
            w_stamina_end_list += [row['w_stamina_end']]
            w_stamina_aerobic_end_list += [row['w_stamina_aerobic_end']]
            w_stamina_anaerobic_end_list += [row['w_stamina_anaerobic_end']]
            stamina_level_list += [row['stamina_level']]
            aerobic_level_list += [row['aerobic_level']]
            anaerobic_level_list += [row['anaerobic_level']]
        f.close()

    csv_header = []
    csv_header += ["workout_date_list"]
    csv_header += ["laDilutionGrade_list"]
    csv_header += ["LA_dilution_grade_list"]
    csv_header += ["aeroCapacity_list"]
    csv_header += ["aero_capacity_list"]
    csv_header += ["aeroTotalCapacity_list"]
    csv_header += ["aero_total_capacity_list"]
    csv_header += ["valid_calibration_list"]
    csv_header += ["stamina_max_use_list"]
    csv_header += ["stamina_aerobic_max_use_list"]
    csv_header += ["stamina_anaerobic_max_use_list"]
    csv_header += ["answer_breath_list"]
    csv_header += ["answer_muscle_list"]
    csv_header += ["answer_RPE_list"]
    csv_header += ["w_stamina_end_list"]
    csv_header += ["w_stamina_aerobic_end_list"]
    csv_header += ["w_stamina_anaerobic_end_list"]
    csv_header += ["stamina_level_list"]
    csv_header += ["aerobic_level_list"]
    csv_header += ["anaerobic_level_list"]
    csv_header += ["workout_dir_list"]
            
    with open(server_algorithm_summary_list_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(workout_date_list)+1):
            data = []
            if row == 0:
                data = csv_header
            else:
                for col in range(len(csv_header)):
                    data += [eval(csv_header[col])[row-1]]
            writer.writerow(data)
        csvfile.close()

def write_algorithm_summary(server_algorithm_summary_path, laDilutionGrade, LA_dilution_grade, aeroCapacity, aero_capacity, aeroTotalCapacity, aero_total_capacity, valid_calibration, stamina_max_use, stamina_aerobic_max_use, stamina_anaerobic_max_use, workout_date, workout_time_sec, answer_breath, answer_muscle, answer_RPE, w_stamina_end, w_stamina_aerobic_end, w_stamina_anaerobic_end, stamina_level, aerobic_level, anaerobic_level):
    csv_header = []
    csv_header += ["workout_date"]
    csv_header += ["workout_time_sec"]
    csv_header += ["laDilutionGrade"]
    csv_header += ["LA_dilution_grade"]
    csv_header += ["aeroCapacity"]
    csv_header += ["aero_capacity"]
    csv_header += ["aeroTotalCapacity"]
    csv_header += ["aero_total_capacity"]
    csv_header += ["valid_calibration"]
    csv_header += ["stamina_max_use"]
    csv_header += ["stamina_aerobic_max_use"]
    csv_header += ["stamina_anaerobic_max_use"]
    csv_header += ["answer_breath"]
    csv_header += ["answer_muscle"]
    csv_header += ["answer_RPE"]
    csv_header += ["w_stamina_end"]
    csv_header += ["w_stamina_aerobic_end"]
    csv_header += ["w_stamina_anaerobic_end"]
    csv_header += ["stamina_level"]
    csv_header += ["aerobic_level"]
    csv_header += ["anaerobic_level"]

    with open(server_algorithm_summary_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        anlysis_result = []
        for col in range(len(csv_header)):
            anlysis_result += [eval(csv_header[col])]
        writer.writerow(anlysis_result)
        csvfile.close()