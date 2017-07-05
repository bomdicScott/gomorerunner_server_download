import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.dates as md
import csv
import json
import numpy as np
import os
import dateutil
import datetime
import sys
from math import radians, cos, sin, asin, sqrt
from staticmap.staticmap import *


def get_fig_2D_route(R_lat, R_lng):

    m = StaticMap(500, 500)
    point = []
    for i in range(len(R_lat)):
        if R_lat[i] > 0:
            point.append((R_lng[i],R_lat[i]))
    point = point[::2]
    for count in range(len(point)-1):
        color = (255,0,0)
        width = 2
        line = Line([point[count],point[count+1]], color, width)
        m.add_line(line)
    start_marker = CircleMarker(point[0], 'green', 20)
    end_marker = CircleMarker(point[-1], 'black', 15)
    m.add_marker(start_marker)
    m.add_marker(end_marker)

    fig = m.render()

    return fig

def get_fig_time_speed_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Speed')

    ax.set_title('Speed kmph')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('kmph')
    ax.legend(loc='upper right')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 20:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 21
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_dist_pace_alt(X,Y1,Y2): # km / kmph / m
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # pace transform from kmph
    Y1_pace = []
    for i in range(len(Y1)):
        if (Y1[i] <= 0):
            Y1_pace += [100.0]
        else:
            Y1_pace += [1000.0 / (Y1[i] / 3.6) / 60.0]  
    Y1 = Y1_pace

    ax.plot(X, Y1, 'b', label='Pace')
    ax.set_title('Pace')
    ax.set_xlabel('distance (km)')
    ax.set_ylabel('pace (min)')
    ax.legend(loc='upper right')

    Xlim = max(X)
    Ylim1 = 10.0
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(Ylim1, 0)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_pace_alt(X,Y1,Y2): # km / kmph / m
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # pace transform from kmph
    Y1_pace = []
    for i in range(len(Y1)):
        if (Y1[i] <= 0):
            Y1_pace += [100.0]
        else:
            Y1_pace += [1000.0 / (Y1[i] / 3.6) / 60.0]  
    Y1 = Y1_pace

    ax.plot(X, Y1, 'b', label='Pace')
    ax.set_title('Pace')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('pace (min)')
    ax.legend(loc='upper right')

    Xlim = max(X)
    Ylim1 = 10.0
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(Ylim1, 0)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

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

def get_fig_time_D_lat_D_lng_D2_lat_D2_lng(w_t, D_lat, D_lng, D2_lat, D2_lng, rD2_lat, rD2_lng):
    fig = plt.figure(figsize=[20,15])
    
    ax = fig.add_subplot(611)
    ax.plot(w_t, D_lat, 'b', label='D_lat')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax = fig.add_subplot(612)
    ax.plot(w_t, D_lng, 'b', label='D_lng')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax = fig.add_subplot(613)
    ax.plot(w_t, D2_lat, 'b', label='D2_lat')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax = fig.add_subplot(614)
    ax.plot(w_t, D2_lng, 'b', label='D2_lng')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax = fig.add_subplot(615)
    ax.plot(w_t, rD2_lat, 'b', label='rD2_lat')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax = fig.add_subplot(616)
    ax.plot(w_t, rD2_lng, 'b', label='rD2_lng')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax.set_xlabel('time (sec)')

    return fig

def get_fig_anaerobic_capacity_with_FCP(FCP_080_cap_list, FCP_090_cap_list, FCP_095_cap_list, FCP_100_cap_list):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(np.arange(0.5, 10, 0.5), FCP_080_cap_list, label='FCP = 0.8')
    ax.plot(np.arange(0.5, 10, 0.5), FCP_090_cap_list, label='FCP = 0.9')
    ax.plot(np.arange(0.5, 10, 0.5), FCP_095_cap_list, label='FCP = 0.95')
    ax.plot(np.arange(0.5, 10, 0.5), FCP_100_cap_list, label='FCP = 1.0')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax.set_xlabel('allout time (min)')
    ax.set_ylabel('anaerobic capacity (dcp*sec)')

    return fig



def get_fig_delta_sta_distribution(delta_sta_list):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('delta sta distribution')
    ax.hist(delta_sta_list,50)
    ax.grid(True)
    ax.set_xlim(-0.4, 0.1)


    ax.set_xlabel('delta sta')

    return fig

def get_fig_stamina_trimp_consumption_bars(s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc, s1_consume, s2_consume, s3_consume, s4_consume, s5_consume):
    rate_list = [s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc]
    consume_list = [s1_consume, s2_consume, s3_consume, s4_consume, s5_consume]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Stamina Consume and Rate Distribution')
    
    bar_width = 0.2
    ax.bar(np.arange(len(consume_list))+bar_width/2.0,consume_list,align='center',color='r', width=bar_width, label='Stamina Consumption')
    ax.bar(np.arange(len(rate_list))-bar_width/2.0,rate_list,align='center',color='b', width=bar_width, label='Stamina Trimp')
    ax.set_xticks(np.arange(len(consume_list)))
    ax.set_xticklabels(('s1', 's2', 's3', 's4', 's5'))
    ax.grid(True)
    plt.legend(loc='upper left')
    ax.set_ylim(-100, 100)
    ax.set_xlabel('zone')

    return fig

def get_fig_stamina_consumption_bar_by_HRR(z1_consume, z2_consume, z3_consume, z4_consume, z5_consume):
    consume_list = [z1_consume, z2_consume, z3_consume, z4_consume, z5_consume]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Stamina Consume Distribution by HRR')
    ax.bar(np.arange(len(consume_list)),consume_list,align='center')
    ax.set_xticks(np.arange(len(consume_list)))
    ax.set_xticklabels(('s1', 's2', 's3', 's4', 's5'))
    ax.grid(True)
    ax.set_ylim(-50, 100)

    ax.set_xlabel('zone')

    return fig

def get_fig_stamina_consumption_bar(s1_consume, s2_consume, s3_consume, s4_consume, s5_consume):
    consume_list = [s1_consume, s2_consume, s3_consume, s4_consume, s5_consume]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Stamina Consume Distribution')
    ax.bar(np.arange(len(consume_list)),consume_list,align='center')
    ax.set_xticks(np.arange(len(consume_list)))
    ax.set_xticklabels(('s1', 's2', 's3', 's4', 's5'))
    ax.grid(True)
    ax.set_ylim(-50, 100)

    ax.set_xlabel('zone')

    return fig


def get_fig_stamina_trimp_bar(s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc):
    rate_list = [s1_ptc, s2_ptc, s3_ptc, s4_ptc, s5_ptc]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Stamina Trimp Distribution')
    ax.bar(np.arange(len(rate_list)),rate_list,align='center')
    ax.set_xticks(np.arange(len(rate_list)))
    ax.set_xticklabels(('s1', 's2', 's3', 's4', 's5'))
    ax.grid(True)

    ax.set_xlabel('zone')

    return fig

def get_fig_trimp_bar(z1_trimp, z2_trimp, z3_trimp, z4_trimp, z5_trimp):
    trimp_list = [z1_trimp, z2_trimp, z3_trimp, z4_trimp, z5_trimp]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('TRIMP Distribution')
    ax.bar(np.arange(len(trimp_list)),trimp_list,align='center')
    ax.set_xticks(np.arange(len(trimp_list)))
    ax.set_xticklabels(('z1', 'z2', 'z3', 'z4', 'z5'))
    ax.grid(True)

    ax.set_xlabel('zone')

    return fig


def get_fig_time_lat_lng(w_t, R_lat, R_lng):
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(w_t, R_lat, 'b', label='R_lat')
    ax.set_ylabel('degree')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax = fig.add_subplot(212)
    ax.plot(w_t, R_lng, 'b', label='R_lng')
    ax.set_ylabel('degree')
    ax.legend(loc='upper left')
    ax.grid(True)

    ax.set_xlabel('time (sec)')

    return fig



def get_fig_time_incline_alt_with_note(X,Y1,Y2, x1, x2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='incline')
    if x2 < len(X):
        ax.plot(X[x1], Y1[x1], 'ro')
        ax.plot(X[x2], Y1[x2], 'ro')

    ax.set_title('incline')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('%')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 15:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 20
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    #ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_incline_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='incline')

    ax.set_title('incline')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('%')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 15:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 20
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    #ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_dist_cadence_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Cadence')

    ax.set_title('Cadence')
    ax.set_xlabel('distance (km)')
    ax.set_ylabel('rpm')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 150:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 200
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_cadence_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Cadence')

    ax.set_title('Cadence')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('rpm')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 150:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 200
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_dist_power_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Power')

    ax.set_title('Power')
    ax.set_xlabel('distance (km)')
    ax.set_ylabel('watts')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 300:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 400
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_power_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Power')

    ax.set_title('Power')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('watts')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 300:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 400
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_dist_HR_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Heartrate')

    ax.set_title('Heartrate')
    ax.set_xlabel('distance (km)')
    ax.set_ylabel('bpm')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 200:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 230
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_HR_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Heartrate')

    ax.set_title('Heartrate')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('bpm')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 200:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 230
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_dist_speed_alt(X,Y1,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='Speed')

    ax.set_title('Speed kmph')
    ax.set_xlabel('distance (km)')
    ax.set_ylabel('kmph')
    ax.legend(loc='upper right')

    Xlim = max(X)
    Y1_max = max(Y1)
    if Y1_max >= 20:
        Ylim1 = max(Y1) * 1.3
    else:
        Ylim1 = 21
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_dist_max_dist_alt(X,Y1_1,Y1_2,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1_2, 'b', label='instant_max_dist_estimation')
    ax.plot(X, Y1_1, '--r', label='run dist')

    ax.set_title('Max Dist')
    ax.set_xlabel('distance (km)')
    ax.set_ylabel('km')
    ax.legend(loc='upper left')

    Xlim = max(X)
    Y1_max = max(Y1_2)
    if Y1_max >= 10:
        Ylim1 = Y1_max * 1.3
    else:
        Ylim1 = 15
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_max_burn_alt(X,Y1_1,Y1_2,Y2):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1_2, 'b', label='instant_max_burn_estimation')
    ax.plot(X, Y1_1, 'r--', label='total_kcal')
    
    ax.set_title('Max Burn')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('kcal')
    ax.legend(loc='upper left')

    Xlim = max(X)
    
    Y1_max = max(Y1_2)
    if Y1_max >= 250:
        Ylim1 = Y1_max * 1.3
    else:
        Ylim1 = 300
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig





def get_fig_time_stamina_WpPtc(w_t, stamina_ptc_list,aerobic_ptc_list, anaerobic_ptc_list, WpPtc_list):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(w_t, aerobic_ptc_list, 'g', label='Aerobic')
    ax.plot(w_t, anaerobic_ptc_list, 'r', label='Anaerobic')
    ax.plot(w_t, stamina_ptc_list, 'b', label='Stamina')
    ax.plot(w_t, WpPtc_list, 'r--', label='Stamina')

    ax.set_xlabel('time (sec)')
    ax.set_ylabel('%')
    ax.legend(loc='lower left')

    ax.grid(True)

    return fig


def get_fig_time_stamina_alt(X,Y1,Y1_1,Y1_2,Y2,T1,T2,T3,T4,T5,T6):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1_1, 'g', label='Aerobic')
    ax.plot(X, Y1_2, 'r', label='Anaerobic')
    ax.plot(X, Y1, 'b', label='Stamina')

    ax.set_title('Stamina'+', Breath:{}'.format(T1)+', Muscle:{}'.format(T2)+', RPE:{}'.format(T3)+', FCali:{}'.format(T4)+', G:{}'.format(T5)+', C:{}'.format(int(float(T6))))
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('%')
    ax.legend(loc='lower left')

    Xlim = max(X)
    Y1_max = max(Y1)
    Ylim1 = 100
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_time_vdot_alt(X,Y1,Y2,T1,T2,T3,T4,T5,T6):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(X, Y1, 'b', label='instant vdot')

    ax.set_title('instant vdot'+', Breath:{}'.format(T1)+', Muscle{}:'.format(T2)+', RPE:{}'.format(T3)+', FCali:{}'.format(T4)+', G:{}'.format(T5)+', C:{}'.format(int(float(T6))))
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('VDOT')
    ax.legend(loc='lower left')

    Xlim = max(X)
    Y1_max = max(Y1)
    Ylim1 = 100
    
    Y2_max = max(Y2)
    if Y2_max >= 250:
        Ylim2 = Y2_max * 1.3
    else:
        Ylim2 = 300

    ax.set_xlim(0, Xlim)
    ax.set_ylim(0, Ylim1)
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
    ax2.set_ylabel('altitude(m)')
    ax2.set_xlim(0, Xlim)
    ax2.set_ylim(0, Ylim2)

    return fig

def get_fig_vdot_curve_vs_target(vdot_3km, vdot_5km, vdot_10km, vdot_15km, vdot_half_marathon, vdot_25km, vdot_30km, vdot_35km, vdot_full_marathon, target_dist_km, VDOT_target):

    dist_list = []
    dist_list += [3.0]
    dist_list += [5.0]
    dist_list += [10.0]
    dist_list += [15.0]
    dist_list += [21.0975]
    dist_list += [25.0]
    dist_list += [30.0]
    dist_list += [35.0]
    dist_list += [42.195]

    vdot_list = []
    vdot_list += [vdot_3km]
    vdot_list += [vdot_5km]
    vdot_list += [vdot_10km]
    vdot_list += [vdot_15km]
    vdot_list += [vdot_half_marathon]
    vdot_list += [vdot_25km]
    vdot_list += [vdot_30km]
    vdot_list += [vdot_35km]
    vdot_list += [vdot_full_marathon]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(dist_list, vdot_list, 'b', label="VDOT")
    ax.plot(target_dist_km, VDOT_target, 'ro', label="Target", markersize=10)
    
    ax.set_ylim([10.0, 80.0])
    ax.yaxis.set_ticks(range(10,80,5))
    ax.set_xlim([0,42])
    ax.set_ylabel('VDOT')
    ax.set_xlabel('km')
    ax.set_title('VDOT Curve vs. Target VDOT:{:.2f}'.format(VDOT_target))
    ax.legend(loc='lower left')
    ax.grid(True, which='both')

    return fig

def get_fig_cardio_training_effect_on_CP_curve(total_hour_list, speed_kmph_list, Cardio_training_effect_ptc_list, speed_kmph_ptc_list, E_speed_kmph,M_speed_kmph,T_speed_kmph,I_speed_kmph,H_speed_kmph, target_dist_km, target_finish_time_sec):

    target_speed_kmph = target_dist_km / (target_finish_time_sec / 3600.0)
    target_finish_time_hr = target_finish_time_sec / 3600.0

    alpha_rate_up = 75.0
    alpha_plot = 0.3

    fig = plt.figure()
    ax = fig.add_subplot(111)

    total_hour_list_plot = []
    speed_kmph_list_plot = []
    for i in range(len(total_hour_list)):
        if total_hour_list[i] > 0:
            total_hour_list_plot += [total_hour_list[i]]
            speed_kmph_list_plot += [speed_kmph_list[i]]

    ax.plot(total_hour_list_plot, speed_kmph_list_plot, label="CP curve")
    ax.plot(target_finish_time_hr, target_speed_kmph, 'ro', label="Target", markersize=10)

    # add cardio training effect notation
    for i in range(len(Cardio_training_effect_ptc_list)):
        if Cardio_training_effect_ptc_list[i] > 0:
            if Cardio_training_effect_ptc_list[i] > alpha_rate_up:
                alpha_rate = 1.0
            else:
                alpha_rate = Cardio_training_effect_ptc_list[i] / alpha_rate_up
            ax.plot(total_hour_list[i], speed_kmph_list[i], 'r>', alpha=alpha_rate, markersize=20)

    ax.add_patch(Rectangle((0, M_speed_kmph), 5.0, (T_speed_kmph - M_speed_kmph), facecolor="blue", edgecolor="none", alpha = alpha_plot))
    ax.add_patch(Rectangle((0, T_speed_kmph), 5.0, (I_speed_kmph - T_speed_kmph), facecolor="orange", edgecolor="none", alpha = alpha_plot))
    ax.add_patch(Rectangle((0, I_speed_kmph), 5.0, (H_speed_kmph - I_speed_kmph), facecolor="red", edgecolor="none", alpha = alpha_plot))
    ax.set_xlabel('Speed Kmph')

    ax.set_ylim([6.0, max(speed_kmph_list)*1.2])
    ax.set_xlim([0,4.5])
    ax.set_ylabel('km/hr')
    ax.set_xlabel('hours')
    ax.set_title('CP Curve')
    ax.legend(loc='lower left')

    return fig

def get_fig_cardio_training_effect_distribution(speed_kmph_list, Cardio_training_effect_ptc_list, speed_kmph_ptc_list, E_speed_kmph,M_speed_kmph,T_speed_kmph,I_speed_kmph,H_speed_kmph):

    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.set_title("Cardio Training Effect Analysis")
    ax.plot(speed_kmph_list, Cardio_training_effect_ptc_list, label="Cardio training effect")
    ax.set_ylabel('%')
    ax.legend(loc='upper left')   
    ax.set_xlim([0, max(speed_kmph_list)])
    ax.set_ylim([0,100])

    # add definition of training zone
    alpha_plot = 0.3
    ax.add_patch(Rectangle((M_speed_kmph, 0), (T_speed_kmph - M_speed_kmph), 150, facecolor="blue", edgecolor="none", alpha = alpha_plot))
    ax.add_patch(Rectangle((T_speed_kmph, 0), (I_speed_kmph - T_speed_kmph), 150, facecolor="orange", edgecolor="none", alpha = alpha_plot))
    ax.add_patch(Rectangle((I_speed_kmph, 0), (H_speed_kmph - I_speed_kmph), 150, facecolor="red", edgecolor="none", alpha = alpha_plot))


    ax = fig.add_subplot(212)
    #print("sum(speed_kmph_ptc_list):{}".format(sum(speed_kmph_ptc_list)))
    ax.plot(speed_kmph_list, speed_kmph_ptc_list, label="speed distribution")
    ax.set_ylabel('%')
    ax.legend(loc='upper left')   
    ax.set_xlim([0, max(speed_kmph_list)])
    ax.set_ylim([0,100])
    # add definition of training zone
    ax.add_patch(Rectangle((M_speed_kmph, 0), (T_speed_kmph - M_speed_kmph), 150, facecolor="blue", edgecolor="none", alpha = alpha_plot))
    ax.add_patch(Rectangle((T_speed_kmph, 0), (I_speed_kmph - T_speed_kmph), 150, facecolor="orange", edgecolor="none", alpha = alpha_plot))
    ax.add_patch(Rectangle((I_speed_kmph, 0), (H_speed_kmph - I_speed_kmph), 150, facecolor="red", edgecolor="none", alpha = alpha_plot))
    ax.set_xlabel('Speed Kmph')


    return fig




