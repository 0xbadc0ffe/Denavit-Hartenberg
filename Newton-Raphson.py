import numpy as np
import os
import platform

if platform.system() == 'Windows':
    CLEAR_STR = "cls" 
else:
    CLEAR_STR = "clear"


def cos(x, deg=False):
    if deg:
        x = np.deg2rad(x)
    return np.cos(x)

def sin(x, deg=False):
    if deg:
        x = np.deg2rad(x)
    return np.sin(x)

def tan(x, deg=False):
    if deg:
        x = np.deg2rad(x)
    return np.tan(x)

def inv( mat):
    mat = np.matrix(mat)
    return mat.I


# Direct kinematics function
# fr examples:  
# fr  = np.array([ L1*cos(q[0]) + L2*cos(q[1])+ L3*cos(q[2]), L1*sin(q[0]) + L2*sin(q[1]) + L3*sin(q[2]), q[2]-q[1]])
def fr(q):
    fr  = np.array([ L1*cos(q[0]) + L2*cos(q[1])+ L3*cos(q[2]), L1*sin(q[0]) + L2*sin(q[1]) + L3*sin(q[2]), q[2]-q[1]])
    fr = fr[np.newaxis].T
    return fr

# Jacobian Matrix
# Jr examples:
# Jr = np.matrix([[ -L1*sin(q[0]), -L2*sin(q[1]), -L3*sin(q[2]) ], [ L1*cos(q[0]), L2*cos(q[1]), L3*cos(q[2]) ], [0, -1, 1]])
def J(q):
    q = np.squeeze(np.asarray(q))
    # Jacobian of fr
    Jr = np.matrix([[ -L1*sin(q[0]), -L2*sin(q[1]), -L3*sin(q[2]) ], [ L1*cos(q[0]), L2*cos(q[1]), L3*cos(q[2]) ], [0, -1, 1]])
    return Jr

def Qnext(q):
    delta = J(q).I @ [rd -fr(q) ]
    qnext = q + delta.T
    #qnext = np.squeeze(np.asarray(qnext))
    return qnext


# Np settings
np.set_printoptions(precision=4, suppress=True)


# Define variables
# intial guess
q = np.array([0, np.pi/2, np.pi/2])
q = q[np.newaxis].T

#v = { 'q1':0, 'q2': np.pi/2, "q3": np.pi/2}
# eg v['q1']

# Define constants and constraints
L1 = 0.4
L2 = 0.3
L3 = 0.2
precision = 0.02

# target
rd = np.array([0.7, 0.5, 0])
rd = rd[np.newaxis].T




os.system(CLEAR_STR)
print("\n######### Starting ...")
print("\nq0: ")
print(q)
print("\nrd: ")
print(rd)
e_norm = precision +1
count = 1
print("\n\n\nEnter to start computation")
while e_norm > precision:
    input("\n\nShow next")
    os.system(CLEAR_STR)
    print(f"\n######### Loop {count}:\n")
    print("\nfr(q): ")
    print(fr(q))
    print("\ne(q): ")
    e = rd -fr(q)
    print(e)
    print("\n||e||:")
    e_norm = np.linalg.norm(e)
    print(e_norm)
    print("\nJr(q): ")
    Jr = J(q)
    print(Jr)
    print("\nDelataq: ")
    print(np.transpose(Jr.I @ [ rd -fr(q) ]))
    print(f"\nq{count}: ")
    q = Qnext(q)
    print(q)
    count += 1

print("\n\nAccuracy achieved\n")

