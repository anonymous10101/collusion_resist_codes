# This program verifies the discrete crowdsensing game model is group strategyproofed.

import random
import math
from copy import deepcopy
# Let there be 100 users.
n = 100
# Let the upper bound of the users' unit costs be 10.
k_max = 10.0
# 1000 test times
n_tests = 1000
# the maximum payment to each user is 100.
Pm = 100
# Total reward of the platform is 10000.
R = 10000
# Platform utility
u_p = R

class SensingUser:
	'''the class for a user participating in sensing.'''
	k = 0;	# the unit cost
	upper_k = 0;	# the upper cost bound
	lower_k = 0;	# the lower cost bound
	s = 0;	# the user strategy
	n_tasks = 0;	# sensing task number of this user
	p = 0;	# payment to this user
	u = 0;	# user utility
	def __init__(self):
		# The initial s_i = kappa_i
		self.s = self.k = random.uniform(0.01, k_max)
		# additionally we have the cost bounds
		self.upper_k = self.k + random.uniform(0.01, k_max/2)
		self.lower_k = self.k - random.uniform(0.01, k_max/2)
		if self.upper_k > k_max:
			self.upper_k = k_max
		if self.lower_k <0:
			self.lower_k = 0.01

f = open('privacy_dis.txt', 'w')
for n in range(100,1100,100):
	# Smallest |T_k|.
	tk_least = 0
	tk_arr = []
	# Smallest |P_k|.
	pk_least = 0
	pk_arr = []
	test_runs = 0
	while test_runs < n_tests:
		test_runs = test_runs + 1	# a new test round
		# Initialize the users.
		users = []
		for i in range(n):
			users.append(SensingUser())

		# Compute the d.
		d = k_max
		for user in users:
			if user.upper_k - user.lower_k < 2*d:
				d = (user.upper_k - user.lower_k)/2

		# Compute the m.
		m = 1
		while (m+1)*(m+2)*d < Pm:
			m = m+1

		# Circumvent some trivial cases. That is there are two few partitions.
		if m<3:
			test_runs = test_runs - 1	# cancel this test round
			continue;
			
		# Recorrect the d
		if m*d > k_max:
			d = k_max / m

		# Initialize the P_k array.
		P_k_arr = []
		for i in range(m):
			P_k = []
			for j in range(n):
				if users[j].upper_k > i*d and users[j].lower_k < (i+1)*d:
					P_k.append(j)
			P_k_arr.append(P_k)

		# Initialize the T_k array.
		T_k_arr = []
		for i in range(m):
			T_k = []
			for j in range(n):
				if users[j].s > i*d and users[j].s < (i+1)*d:
					T_k.append(j)
			T_k_arr.append(T_k)

		# Let us compute the sensing time and the payment for each user.
		# Also we calculate each user utility and the platform utility.
		for user in users:
			user.n_tasks = m - math.floor(user.s / d)
			if user.n_tasks < 0:
				user.n_tasks = 0
			user.p = d * user.n_tasks * (2*m + 1 - user.n_tasks) / 2.0
			user.u = user.p - user.k * user.n_tasks
			u_p = u_p - user.p

		# Adjust the partitions.
		changed = True;	# whether exists k s.t. |T_k| < 2 ?
		while changed:
			changed = False;
			for i in range(0, m):
				if len(T_k_arr[i])>0 and len(T_k_arr[i])<2:
					changed = True;
					k = 1
					while i-k >= 0 and not len(T_k_arr[i-k]) > 0:
						k = k + 1
					if i-k < 0:
						k = -1
						while not len(T_k_arr[i-k])>0:
							k = k - 1
					for user in users:
						if user.s < (i+1)*d:
							user.n_tasks = user.n_tasks + k
							user.p = user.p + k*d
					T_k_arr[i-k] = T_k_arr[i-k] + T_k_arr[i]
					T_k_arr[i] = deepcopy(T_k_arr[i-k])
					P_k_arr[i-k] = P_k_arr[i-k] + P_k_arr[i]
					P_k_arr[i] = deepcopy(P_k_arr[i-k])

		# Find out the the smallest |T_k|.
		Tk_smallest = n
		for item in T_k_arr:
			if len(item) < Tk_smallest and len(item)>0:
				Tk_smallest = len(item)
				
		# Find out the the smallest |P_k|.
		Pk_smallest = n
		for item in P_k_arr:
			if len(item) < Pk_smallest and len(item)>0:
				Pk_smallest = len(item)
			
		tk_least = tk_least + Tk_smallest
		tk_arr.append(Tk_smallest)
		pk_least = pk_least + Pk_smallest
		pk_arr.append(Pk_smallest)
	
	# statistics
	dev_tk = 0
	for i in tk_arr:
		dev_tk = dev_tk + (i - tk_least*1.0 / n_tests)**2
	dev_pk = 0
	for i in pk_arr:
		dev_pk = dev_pk + (i - pk_least*1.0 / n_tests)**2
	# Outputs
	f.write('{0:d} {1:f} {2:f} {3:f} {4:f}\n'.format(n, tk_least*1.0 / n_tests, (dev_tk / n_tests)**0.5, pk_least*1.0 / n_tests, (dev_pk / n_tests)**0.5))

f.close