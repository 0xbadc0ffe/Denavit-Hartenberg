# Denavit-Hartenberg
dhtable.py: A small program able to give the homogeneous transformation matrix from the end effector frame of a robot arm to its base frame, using Denavit-Hartenberg parameters

euler_angles.py: compute generic Euler angles transformations given the representation (e.g. "ZYZ", "ZYX") and the angles values.

Newton-Raphson.py: compute Newthon-Raphson inverse kinematics. The kinematics, its Jacobian and the other parameters are hardcoded, so you need to change it manually into the code to resolve your version of the problem.



## Requirements

1. Python3 
	
	https://www.python.org/downloads/
	https://docs.python-guide.org/starting/install3/linux/
	
2. numpy library

	https://numpy.org/install/
	
	On Windows, if you get errors from the numpy module this could be
	due to some Windows bugs with numpy. In that case I suggest installing
	an older version, such as:
	
	pip uninstall numpy
	
	pip install numpy==1.19.3
	

he 
