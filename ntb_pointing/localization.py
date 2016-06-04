import numpy as np
from global_var_config import anchor_coor
from scipy.optimize import fsolve
from numpy import linalg as la
from global_var_config import anchor_coor

DATA_TYPE = np.float64
x_limits = [-5.88, 3.055]
y_limits = [0, 2.434]
z_limits = [-4.124, 4.069]

range_ray = []


def find(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]

def equations(vs, node1, nodei, nodej, idx, i, j):
	x, y, z = vs
	return ((x-node1[0]) ** 2 + (y-node1[1]) ** 2 + (z-node1[2]) ** 2 - range_ray[idx] ** 2, \
			(x-nodei[0]) ** 2 + (y-nodei[1]) ** 2 + (z-nodei[2]) ** 2 - range_ray[i] ** 2, \
			(x-nodej[0]) ** 2 + (y-nodej[1]) ** 2 + (z-nodej[2]) ** 2 - range_ray[j] ** 2)

def inBtw(value, limits):
	return value >= limits[0] and value <= limits[1]

def localization(ranges):
	global range_ray
	# range = [4.777,3.916,4.269,5.47,2.001,2.512,3.29,6.01]
	# range = [4.41,3.062,4.593,5.539,1.414,2.6,3.349,100]
	# range = [4.41,3.062,4.593,5.539,1.414,2.6,3.349,5.332]
	range_ray = []

	for i in range(8):
		r = ranges[i]
		if len(r) < 9:
			range_ray.append(0)
		else:
			range_ray.append(sum(r[:6]) / 5)

	valid_range_index = find(range_ray, lambda x: x != 0)
	# print valid_range_index
	if len(valid_range_index) < 3:
		# rospy.loginfo("Less than three ranges obtained. Cannot perform localization")
		return []

	counter=0
	counter_loop = 0
	loc1 = np.array([0,0,0])
	A = []
	b = []
	node1 = anchor_coor[valid_range_index[0],:]
	for i in valid_range_index[0:1]:
		for j in valid_range_index[1:]:
			counter_loop = counter_loop + 1
			nodei = anchor_coor[i,:]
			nodej = anchor_coor[j,:]
			sx,sy,sz = fsolve(equations, (0,1.25,0), args=(node1, nodei, nodej,valid_range_index[0],i,j))
			loc_candidate = np.array([float(sx),float(sy),float(sz)])
			# print "loc_candidate=", loc_candidate
			if inBtw(loc_candidate[0],x_limits) \
				and inBtw(loc_candidate[1], y_limits) \
				and inBtw(loc_candidate[2], z_limits):

				loc1 = loc1 + loc_candidate
				counter = counter+1

				for n_num in xrange(0,8):
					n = anchor_coor[n_num,:] - loc_candidate
					A.append(n)
					b.append(loc_candidate.dot(n))
	# return loc_candidate

	loc1 = loc1/counter
	loc2 = np.dot(la.pinv(np.array(A)), np.array(b))
	# print "loc1=", loc1, "loc2=",loc2

	print "[Localization] Initial Location is ", loc1+loc2/2

	return loc1+loc2/2
