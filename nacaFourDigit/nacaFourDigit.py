# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 13:58:19 2022

@author: imdat
"""

import math
import matplotlib.pyplot as plt
import xlsxwriter

xCamberPoints = []
yCamberPoints = []
xUpperPoints = []
xLowerPoints = []
yUpperPoints = []
yLowerPoints = []

def welcome():
    hello = """This is a NACA Four-Digit Airfoil Generator.
    The first digit specifies the maximum camber(m) in the percentage of the chord,
    the second digit indicates the position of the maximum camber(p) in tenths of the chord,
    the last two numbers provide the maximum thickness(t) of the airfoil in percentage
    of the chord."""
    global c ,m ,p ,t ,pn
             
    while True:
        try:
            c = float(input("Please enter your chord(airfoil length) in meters:\t"))
            m = int(input("Please enter your maximum camber value in percentage of the chord:\t"))
            p = int(input("Please enter your position of the maximum camber value in tenths of the chord:\t"))
            if p == 0:
                raise Exception()
            t = int(input("Please enter your maximum thickness value in percentage of the chord:\t"))
            pn = float(input("How many points would you like to have?\t"))
            break
        except:
            print(""""Only floating point numbers and integers are allowed.
Also, do not forget the position of the maximum camber 'p' cannot be 0""")
    m /= 100
    p/= 10
    t/= 100

def calculatePoints():
    def calculateSurface():
        xu = (x - (yt * (math.sin(tetha))))
        xUpperPoints.append(xu)
        xl = (x + (yt * (math.sin(tetha))))
        xLowerPoints.append(xl)
        yu = yc + (yt * (math.cos(tetha)))
        yUpperPoints.append(yu)
        yl = yc - (yt * (math.cos(tetha)))
        yLowerPoints.append(yl)
    x = 0
    while x <= c:
        xCamberPoints.append(x)
        yt = (t / 0.2) * ((0.2969 * (x**0.5)) - (0.1260 * x) - (0.3516 * (x**2))
                          + (0.2843 * (x**3)) - (0.1015 * (x**4)))
        if x <= p:
            yc = (m / (p**2) ) * ( (2*p*x) - (x**2) ) 
            yCamberPoints.append(yc)
            tetha = math.atan((m / (p**2)) * ((2*p) - (2*x)))
            calculateSurface()

        elif x > p:
            yc = ( (m / ((1-p)**2)) ) * ((1-2*p) + (2*p*x) - (x**2))
            yCamberPoints.append(yc)
            tetha = math.atan((m / ((1 - p)**2)) * ((2*p)-(2*x)))
            calculateSurface()

        x += c / pn
    xCamberPoints.append(c)
    yCamberPoints.append(0)
    xUpperPoints.append(c)
    yUpperPoints.append(0)
    xLowerPoints.append(c)
    yLowerPoints.append(0)

def show():
    font = {'family':'Calibri','color':'#363945', 'size' : 15}
    
    def graphic():
        plt.figure(figsize = (13.5,10))
        plt.plot(xCamberPoints, yCamberPoints, ls = ":", c = "#D2386C", label = "Camber Line")
        plt.legend()
        plt.plot(xLowerPoints, yLowerPoints, c = "#0072b5", label = "Airfoil Shape")
        plt.legend()
        plt.plot(xUpperPoints, yUpperPoints, c = "#0072b5", label = "Airfoil Shape")
        plt.xlabel("X axis in meters", fontdict=font)
        plt.ylabel("Y axis in meters", fontdict=font)
        
    graphic()
    plt.axis("equal")
    plt.title("NACA {}{}{} AIRFOIL".format(int(m*100),int(p*10),int(t*100)), fontdict=font)
    plt.show()
    plt.savefig("NACA {}{}{}.png".format(int(m*100),int(p*10),int(t*100)))
    
    graphic()
    plt.title("Expanded NACA {}{}{} AIRFOIL".format(int(m*100),int(p*10),int(t*100)), fontdict=font)
    plt.show()
    plt.savefig("Expanded NACA {}{}{}.png".format(int(m*100),int(p*10),int(t*100)))

def excel():
    workbook = xlsxwriter.Workbook("NACA{}{}{}.xlsx".format(int(m*100),int(p*10),int(t*100)))
    worksheet = workbook.add_worksheet("{}{}{}".format(int(m*100),int(p*10),int(t*100)))
    
    bold_format = workbook.add_format({"bold":True})
    
    worksheet.write("A1", "X Camber Points" , bold_format)
    worksheet.write("B1", "Y Camber Points", bold_format)
    worksheet.write("C1", "X Upper Points", bold_format)
    worksheet.write("D1", "Y Upper Points", bold_format)
    worksheet.write("E1", "X Lower Points", bold_format)
    worksheet.write("F1", "Y Lower Points", bold_format)
    
    
    rowIndex = 2
    while rowIndex <= len(xCamberPoints)+1:
        indexNumber = rowIndex-2
        worksheet.write("A"+ str(rowIndex), round(xCamberPoints[indexNumber], 4))
        worksheet.write("B"+ str(rowIndex), round(yCamberPoints[indexNumber], 4))
        worksheet.write("C"+ str(rowIndex), round(xUpperPoints[indexNumber], 4))
        worksheet.write("D"+ str(rowIndex), round(yUpperPoints[indexNumber], 4))
        worksheet.write("E"+ str(rowIndex), round(xLowerPoints[indexNumber], 4))
        worksheet.write("F"+ str(rowIndex), round(yLowerPoints[indexNumber], 4))
        rowIndex += 1
            
    workbook.close()

welcome()
calculatePoints()
show()
excel()