import numpy as np 
import os
import time
import platform

if platform.system() == 'Windows':
    CLEAR_STR = "cls" 
else:
    CLEAR_STR = "clear"
    
    
print(platform.system())

def mat_str(mat, numspace=4 ,trunc=False, large=False):
    # convert matrix in a string, eventually truncating its values (or making them int with
    # trunc = int or trunc = "int". The option large is made to fit any value length ... but it's large ...
    # numspace parameter specify the number of space IN which print the value, or another spacing in large mode
    res = ""
    if isinstance(trunc, int):
        if numspace < trunc + 3:
            numspace = trunc + 4

    if large:
        distances=[]
        for row in mat:
            for i in range(len(row)):
                le = len(str(row[i]))
                if len(distances) < len(row):
                    distances.append(le)
                else:
                    if le > distances[i]:
                        distances[i] = le
    for row in mat:
        res += "["
        for i in range(len(row)):
            e = row[i]
            if trunc == "int" or trunc == int:
                e = int(e)
            elif isinstance(trunc, int) and trunc > 0:
                if e - int(e) >= float('0.'+'9'*trunc):
                    # small correction for x.9999... elements, eg e=x.999314 trunc=3 => e= x+1
                    e = int(e) + 1
                e = truncate(e, trunc)
                # removing the minus if e contains only zeros
                if e.replace('0','') == '-.':
                    e = e[1:]
                # if x.000 => x
                if '.'+'0'*trunc in e:
                    e = e[: -trunc - 1]
                    
            if large:
                res += " "*(distances[i]+ numspace - len(str(e))) + f"{e}"
            else:
                res += " "*(numspace - len(str(e))) + f"{e}"
        res += " "*(2) + "]\n"
    return res

def print_mat(mat, numspace=4 ,trunc=False, large=False):
    # stringify the matrix and print it
    print(mat_str(mat, numspace=numspace, trunc=trunc, large=large))

def truncate(f, n):
    #Truncates/pads a float f to n decimal places without rounding
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def hom_transf_matrix( joint1, joint2 ):
    # compute homogeneous transformation matrix between consecutive joints frame vectors
    # TODO, possible only if implementing joint reference parameters (from which to derive dh parameters)
    return 

def gen_dh_tabel(joint_list):
    # generates the Denavit–Hartenberg parameters table from the joint obj list
    # TABLE ENTRIES: theta, alpha, a, d
    dh_table = []
    for joint in joint_list:
        dh_line = [joint.theta, joint.alpha, joint.a, joint.d]
        dh_table.append(dh_line)
    dh_table = np.array(dh_table)
    return dh_table

def gen_hom_matrix_from_table(index, dh_table):
    # generate homogeneous transformation matrix from dh_table and joint index
    i = index
    hom_mat = np.array([[np.cos(dh_table[i,0]), -np.sin(dh_table[i,0]) * np.cos(dh_table[i,1]), np.sin(dh_table[i,0]) * np.sin(dh_table[i,1]), dh_table[i,2] * np.cos(dh_table[i,0])],
                      [np.sin(dh_table[i,0]), np.cos(dh_table[i,0]) * np.cos(dh_table[i,1]), -np.cos(dh_table[i,0]) * np.sin(dh_table[i,1]), dh_table[i,2] * np.sin(dh_table[i,0])],
                      [0, np.sin(dh_table[i,1]), np.cos(dh_table[i,1]), dh_table[i,3]],
                      [0, 0, 0, 1]])  
    return hom_mat

def input_joint_list(joint_list=[]):
    # a simple bash interface used to take the joints parameters in input
    global baseframe, effectorframe, b_e_changed
    print("\nHi, press Enter to start ...\n")
    input()
    os.system(CLEAR_STR)
    #joint_list = []
    while(True):
        ans = { "1": True, "Y": True, "y": True, "yes": True,
                "0": False, "N": False, "n": False, "no": False,
                "2": "status", "S": "status", "s": "status", "status": "status",
                "3": "remove", "R": "remove", "r": "remove", "remove": "remove",
                "4": "baseframe", "B": "baseframe", "b": "baseframe", "baseframe": "baseframe",
                "5": "effectorframe", "E": "effectorframe", "e": "effectorframe", "effectorframe": "effectorframe"
                    }
        
        print(f"\nCurrent number of joints: {len(joint_list)}")
        print("\nWould you like to add a new joint?    \n\n")
        print("1/Y/yes:        yes                   0/N/no:        no, compute  \n\n")
        print("2/S/status:     show status           3/R/remove:    remove joint\n\n")
        print("4/B/baseframe:  change base frame     5/E/effector:  change effector frame\n\n\n")
        inp = input()
        try:
            sw = ans[inp]
            if isinstance(sw, str):
                if sw == "status":
                    os.system(CLEAR_STR)
                    if len(joint_list) > 0:
                        print_joint_list(joint_list)
                    else:
                        print("\nJoint list is empty ...")
                    print("\n\n[Base Frame transformation]:")
                    print_mat(baseframe, trunc=3)
                    print("\n\n[Effector Frame transformation]:")
                    print_mat(effectorframe, trunc=3)
                    input("\n\nPress Enter to return\n\n")
                    os.system(CLEAR_STR)
                    continue
                if sw == "remove":
                    os.system(CLEAR_STR)
                    if len(joint_list) > 0:
                        print_joint_list(joint_list)
                        while True:
                            n = input("\n\nJoint to remove: ")
                            try:
                                n = int(n)
                                if n-1 < len(joint_list):
                                    break
                                else:
                                    print("Joint not in list")
                            except ValueError:
                                print("Wrong Fromat")
                        
                        
                        joint_list.pop(n-1)
                        # renaming joints
                        for i in range(len(joint_list)):
                            joint_list[i].num = i + 1
                        os.system(CLEAR_STR)
                        print("\nJoint successfully removed!")
                        input("\n\nPress Enter to return\n\n")
                        os.system(CLEAR_STR)
                        continue
                            
                    else:
                        print("\nJoint list is empty ...")
                        input("\n\nPress Enter to return\n\n")
                        os.system(CLEAR_STR)
                        continue
                
                if sw == "baseframe":
                    # Takes hom. transformation matrix from baseframe to starting joint in input
                    os.system(CLEAR_STR)
                    print("\nDescribe the homogeneous transformation matrix from base frame to the starting joint\n\n")
                    frame_mat = []
                    for i in range(4):
                        while(True):
                            r_i = input(f"[Row {i+1}]  |  ")
                            ans = input("Enter to confirm, \"r\" to repeat\n")
                            if ans != "r":
                                try:
                                    r_i = r_i.split()
                                    if len(r_i) != 4 :
                                        print("Enter 4 numbers      e.g 1 2.4 0 0.93\n")
                                        continue
                                    frame_mat_line = []
                                    for number in r_i:
                                        frame_mat_line.append(float(number))
                                    frame_mat.append(frame_mat_line)
                                    break
                                except ValueError:
                                    print("Wrong number format\n")
                                    continue

                    baseframe = np.array(frame_mat)
                    b_e_changed = True
                    os.system(CLEAR_STR)
                    print()
                    print_mat(baseframe, trunc=3)
                    input("\nPress Enter to return ...")
                    os.system(CLEAR_STR)
                    continue
                if sw == "effectorframe":
                    # Takes hom. transformation matrix from ending joint to effector frame in input
                    os.system(CLEAR_STR)
                    print("\nDescribe the homogeneous transformation matrix from the ending joint to the effector frame\n\n")
                    frame_mat = []
                    for i in range(4):
                        while(True):
                            r_i = input(f"[Row {i+1}]  |  ")
                            ans = input("Enter to confirm, \"r\" to repeat\n")
                            if ans != "r":
                                try:
                                    r_i = r_i.split()
                                    if len(r_i) != 4 :
                                        print("Enter 4 numbers      e.g 1 2.4 0 0.93\n")
                                        continue
                                    frame_mat_line = []
                                    for number in r_i:
                                        frame_mat_line.append(float(number))
                                    frame_mat.append(frame_mat_line)
                                    break
                                except ValueError:
                                    print("Wrong number format\n")
                                    continue

                    effectorframe = np.array(frame_mat)
                    b_e_changed = True
                    os.system(CLEAR_STR)
                    print()
                    print_mat(effectorframe, trunc=3)
                    input("\nPress Enter to return ...")
                    os.system(CLEAR_STR)
                    continue
                        
            if sw:
                # Addin a joint
                os.system(CLEAR_STR)
                index = len(joint_list) + 1
                print(f"\nJoint n° {index}:\n")
                while True: 
                    try:
                        theta = input(f"\nTheta{index} (degrees): ")
                        theta = float(theta)
                        break
                    except ValueError:
                        print("\nWrong format\n")
                while True: 
                    try:  
                        alpha = input(f"\nAlpha{index} (degrees): ")
                        alpha = float(alpha)
                        break
                    except ValueError:
                        print("\nWrong format\n")
                while True: 
                    try:
                        a = input(f"\nA{index} (cm): ")
                        a = float(a)
                        break
                    except ValueError:
                        print("\nWrong format")
                while True: 
                    try:
                        d = input(f"\nD{index} (cm): ")
                        d = float(d)
                        break
                    except ValueError:
                        print("\nWrong format\n")
                    
                while True:
                    inp = input("\n\nConfirm?   1/Y/yes: yes    0/N/no: no\n\n")
                    try:
                        sw = ans[inp]
                        break
                    except KeyError:
                        print("\n\nPlease use only the given possible answers")
                        continue
                if sw:
                    joint = Joint(index, theta, alpha, a, d)
                    joint_list.append(joint)
                
                os.system(CLEAR_STR)
                continue

            else:
                if not len(joint_list):
                    close()
                else:
                    os.system(CLEAR_STR)
                    return joint_list
        except KeyError:
            os.system(CLEAR_STR)
            print("\nPlease use only the given possible answers\n")
            input("\n\nPress Enter to return\n\n")
            os.system(CLEAR_STR)
            continue
            

def close(timesl=1):
    # close the program
    os.system(CLEAR_STR)
    print("\n\n\n           Bye         ,(è >è)/\n\n\n")
    time.sleep(timesl)
    os.system(CLEAR_STR)
    exit()

def print_joint_list(joint_list):
    # print the joint list
    print("\nJoint List:\n")
    for j in joint_list:
        print()
        print(j)
        print()

def compute_all(joint_list, trunc=3, large=False):
    # Firstly it computes all the relative frames hom. transformation [Ai-1->i]
    # Then it generate the final transformation from the starting joint frame to the last joint frame
    # IF a baseframe or an effectorframe are given this function also computes the Hom transformation between 
    # base and effector frames
    print_joint_list(joint_list)
    input("\n\nPress Enter to compute all homogeneous transformation matrices\n\n")
    os.system(CLEAR_STR)
    hom_list = []
    for j in joint_list:
        print(f"\nMatrix A{j.num - 1}->{j.num}(q{j.num})\n")
        print_mat(j.hom_mat, trunc=trunc, large=large)
        hom_list.append(j.hom_mat)
        input("\nPress Enter to show next ...\n")   
        os.system(CLEAR_STR)
    
    print(f"\nTransformation Frame {0} -> Frame {len(joint_list)}:\n")
    hom_0_n = hom_list[0]
    for h in hom_list[1:]:
        hom_0_n = hom_0_n @ h
    print_mat(hom_0_n, trunc=trunc, large=large)
    
    global baseframe, effectorframe, b_e_changed
    if b_e_changed:
        input("\nPress Enter to show next ...\n")   
        os.system(CLEAR_STR)
    
        print(f"\nTransformation base frame -> effector frame:\n")
        hom_b_e = baseframe @ hom_0_n @ effectorframe
        print_mat(hom_b_e, trunc=trunc, large=large)
        return hom_b_e
    
    return hom_0_n




class Joint():
    # This class define the joint characteristics given by the D-H parameters

    def __init__(self, num, theta, alpha, a, d, give_deg2rad=True):
        self.num = num                          # joint number
        if give_deg2rad:
            self.theta = np.deg2rad(theta)      # angle from xi-1 and xi around zi, from degrees
            self.alpha = np.deg2rad(alpha)      # angle from zi-1 and zi around xi, from degrees
        else:
            self.theta = theta                  # angle from zi-1 and zi around xi
            self.alpha = alpha                  # angle from zi-1 and zi around xi
        self.a = a                              # distance of origin of frame i-1 to origin of frame i along xi-1
        self.d = d                              # distance of origin of frame i-1 to origin of frame i along zi-1
        self.hom_mat = None                     # homogeneous transformation matrix from frame i-1 to frame i
        self.gen_hom_matrix()


    def gen_hom_matrix(self):
        # generate the homogeneous transformation matrix
        hom_mat = np.array([[np.cos(self.theta), -np.sin(self.theta) * np.cos(self.alpha), np.sin(self.theta) * np.sin(self.alpha), self.a * np.cos(self.theta) ],
                      [np.sin(self.theta), np.cos(self.theta) * np.cos(self.alpha), -np.cos(self.theta) * np.sin(self.alpha), self.a * np.sin(self.theta) ],
                      [0, np.sin(self.alpha), np.cos(self.alpha), self.d ],
                      [0, 0, 0, 1]])  
        self.hom_mat = hom_mat
        return hom_mat

    def __str__(self):
        # string representation
        th = truncate(self.theta, 4)
        al = truncate(self.alpha, 4)
        a = truncate(self.a, 1)
        d = truncate(self.d, 1)
        res = f"[Joint {self.num}]  Theta: {th} [rad]   Alpha: {al} [rad]   A: {a} [cm]   D: {d} [cm]"
        return res




'''
Another way to compute stuff

# create a Joint obj
joint1 = Joint(1, 90, 90, 0, 2)

# print a matrix truncating at 3rd decimal
print_mat(joint1.hom_mat, trunc=3)

# adding joint to joint list
joint_list = [joint1]

# generate dh table
dh_table = gen_dh_tabel(joint_list)
print(dh_table)

# generate and print the homogeneous transf. matrix from the dh table and the hom_mat field of the Joint objects
print_mat(gen_hom_matrix_from_table(0, dh_table), trunc=3)            
'''



###### MAIN

if __name__ == "__main__":
    
    # Initializing Base and Effector frames
    baseframe = np.identity(4)
    effectorframe = np.identity(4)
    # b_e_changed keeps track of baseframe or effectorframe changes
    b_e_changed = False 

    # generate joint list and data
    joint_list = input_joint_list()
    
    # compute all transformations
    hom_0_n = compute_all(joint_list, trunc=3)
    
    input("\nPress Enter to exit\n\n")
    close()


    
