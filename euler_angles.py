from eulerangles import euler2matrix, EulerAngleConvention, matrix2euler
import eulerangles
import numpy as np
import os
import sys
import platform

if platform.system() == 'Windows':
    CLEAR_STR = "cls" 
else:
    CLEAR_STR = "clear"


def cos(x, deg=True):
    if deg:
        x = np.deg2rad(x)
    return np.cos(x)

def sin(x, deg=True):
    if deg:
        x = np.deg2rad(x)
    return np.sin(x)




os.system(CLEAR_STR)


if len(sys.argv) > 1:
    if sys.argv[1] == "-i":
        matrix = []
        np.set_printoptions(precision=4, suppress=True)
        conv = input("\nchoose convetion [eg ZYX]: ")    
        try:
            inp = input("\nrow 1 : ").split()
            row = []
            for i in inp:
                row.append(float(i))
            matrix.append(row)
            inp = input("\nrow 2 : ").split()
            row = []
            for i in inp:
                row.append(float(i))
            matrix.append(row)
            inp = input("\nrow 3 : ").split()
            row = []
            for i in inp:
                row.append(float(i))
            matrix.append(row)
        except:
            print("\nFailure in matrix submission")
            exit()
        #matrix = np.matrix(matrix)
        #print(matrix)
        #eulers = matrix2euler([matrix], target_axes=conv, target_intrinsic=True, target_positive_ccw=True)
        try:
            eulers = matrix2euler(matrix, target_axes=conv, target_intrinsic=True, target_positive_ccw=True)
        except:
            print("failure")
        print(eulers)
        exit()

    if sys.argv[1] == "-aa":
        r = []
        try:
            r.append(float(input("\nr1 : ")))
            r.append(float(input("\nr2 : ")))
            r.append(float(input("\nr3 : ")))
            ang = float(input("\nangle (degrees) : "))

            R = [ [r[0]**2*(1-cos(ang))+cos(ang), r[0]*r[1]*(1-cos(ang))-r[2]*sin(ang), r[0]*r[2]*(1-cos(ang))+r[1]*sin(ang)], [ r[0]*r[1]*(1-cos(ang))+r[2]*sin(ang),r[1]**2*(1-cos(ang))+cos(ang), r[1]*r[2]*(1-cos(ang))-r[0]*sin(ang)],[r[0]*r[2]*(1-cos(ang))-r[1]*sin(ang), r[1]*r[2]*(1-cos(ang))+r[0]*sin(ang), r[2]**2*(1-cos(ang))+cos(ang)]]
            print()
            print(np.matrix(R))
            print()
        except:
            print("\nFailure in data submission")
        
        exit()


        


np.set_printoptions(precision=4, suppress=True)

conv = input("\nchoose convetion [eg ZYX]: ")

eulers=[]

eulers.append(float(input("\nangle 1 (degrees): ")))
eulers.append(float(input("\nangle 2 (degrees): ")))
eulers.append(float(input("\nangle 3 (degrees): ")))

try:
    rotation_matrix = euler2matrix(eulers, axes=conv, extrinsic=True, positive_ccw=True)
except ValueError:
    print("\nWrong Euler angles convetion "+conv)
    exit()

base_matrix= np.matrix([[1,0,0],[0,1,0],[0,0,1]])
print()
print(base_matrix @ rotation_matrix)
print()




