from eulerangles import euler2matrix, EulerAngleConvention
import numpy as np
import os
import platform

if platform.system() == 'Windows':
    CLEAR_STR = "cls" 
else:
    CLEAR_STR = "clear"

os.system(CLEAR_STR)
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
#rotation_matrix = np.matrix(rotation_matrix)
print()
print(base_matrix @ rotation_matrix)
print()



