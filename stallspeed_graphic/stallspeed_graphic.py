# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 19:44:15 2022

@author: imdatozdagci
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def requirement():
    global stall_speed, cruise_speed, weight, wing_area, ceiling, mean_aero_chord
    
    stall_speed = float(input("What is stall speed value in meters/second?\t")) # m/s
    cruise_speed = float(input("What is cruise speed value in meters/second?\t"))#m/s
    weight = float(input("What is weight value in Newtons\t")) #N
    wing_area = float(input("What is wing area value in square meters\t")) #m^2
    ceiling = float(input("What is maximum altitude value in meters\t")) #m
    mean_aero_chord = float(input("What is mean aerodynamic chord value in meters\t")) #m


def calculate_CLandRN():
    global datas, density
    datas = pd.DataFrame()
    velocities = [_ for _ in np.arange(stall_speed - 3,cruise_speed+10,0.5)]
    datas.insert(0, "velocities", velocities )
    
    h = 0
    i = 1
    while h <= ceiling:
        if 0 <= h < 11000:
            T = 15.04 - 0.00649 * h
            p = ( (101.29) * ( ( (T+273.1) / (288.0) )**5.256 ) )
        elif 11000 <= h <= 25000:
            T = -56.46
            p = ( (22.65) * (math.exp(1.73-0.000157 * h)) )
        else:
            T = ( (-131.21) + (0.00299 * h) )
            p = ( (2.488) * ( ( (T+273.1) / (216.6) )**-11.388 ) )
        density = ( (p) / ( (0.2869) * (T +273.1)) )
        dynamic_viscosity = ( ( (1.458 * (10**-6)) * ((T+273)**(1.5)) ) / ((T+273) + (110.4)) )
        v = stall_speed - 3
        temp = []
        temp2 = []
        while v < (cruise_speed + 10) :
            CL = ( (2 * weight) / (density * (v**2) * wing_area) )
            temp.append(CL)
            RN = ( (density * v * mean_aero_chord) / (dynamic_viscosity) )
            temp2.append(RN)
            v += 0.5
        datas.insert(i,"CL at {}".format(h), temp)
        datas.insert(i+1,"RN at {}".format(h), temp2)
        h += 500
        i += 2
        
    index_cruise_speed = 2*((cruise_speed)-(stall_speed-3))
    nec = datas.iloc[int((index_cruise_speed-2)):int((index_cruise_speed+3)),2::2]
    nec2 = datas.iloc[6:,1::2]

    print("Your Recommend Reynolds Number Value:\t", nec.mean().mean())
    print("Your Required Lift Coefficient Value:\t", nec2.max().max())


def CL_velocityGraphic():
    from shapely.geometry import LineString
    CL_max = [float(input("Please enter you CL max value:\t"))]
    CL_max *=  len(datas.iloc[:,0:1])
    
    
    plt.figure(figsize = (13.5,10))
    plt.plot(datas.iloc[:,0:1],CL_max,"r:", label = "Maximum $C_L$ value")
    plt.legend() 
    
    _ = 1
    while _ < len(datas.columns):
        plt.plot(datas.iloc[:,0:1],datas.iloc[:,_:_+1:] ,c = np.random.rand(3,),
                  label = "values of {}".format(datas.columns[_]))
        plt.legend()
        _ += 2
    
    font = {'family':'Calibri','color':'#363945', 'size' : 15}
    plt.xlabel("Velocity Values (m/s)", fontdict=font)
    plt.ylabel(r"$C_L$ Values", fontdict=font)
    plt.title(r"$C_L$ Values at Different Speeds", fontdict=font)
    
    
    first_line  = LineString(np.column_stack((datas.iloc[:,0:1],CL_max)))
    second_line = LineString(np.column_stack((datas.iloc[:,0:1],datas.iloc[:,1:2:] )))
    third_line  = LineString(np.column_stack(((datas.iloc[:,0:1],datas.iloc[:,-2:-1:] ))))
    intersection = first_line.intersection(second_line)
    intersection2 = first_line.intersection(third_line)
    
    if intersection.geom_type == 'MultiPoint':
        plt.plot(*LineString(intersection).xy, 'o')
        plt.plot(*LineString()(intersection2).xy, "o")
        x1, y1 = np.array(LineString(intersection).xy)
        x2, y2 = np.array(LineString(intersection).xy)
    elif intersection.geom_type == 'Point':
        plt.plot(*intersection.xy, 'o')
        plt.plot(*intersection2.xy, 'o')
        x1, y1 = np.array(intersection.xy)
        x2, y2 = np.array(intersection2.xy)
    
    plt.show()
    print(f"\nYour stall speed at sea level is {x1[0]:.4f}")
    print(f"Your stall speed at {datas.columns[-2][-5:-1]} meters is {x2[0]:.4f}")
    
    WoverS = (0.5) * (density) * (x2[0]**2) * (CL_max[0])
    S_min = weight / WoverS
    print(f"Your minimum wing area should be {S_min:.4f} meters square.")

requirement()
calculate_CLandRN()
CL_velocityGraphic()
