# This program verifies the discrete crowdsensing game model is group strategyproofed.

import random
import math
from copy import deepcopy
# Let there be 100 users.
n = 100
# Let the upper bound of the users' unit costs be 10.
k_max = 10.0
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
		self.upper_k = self.k + random.uniform(0.01, k_max/2.0)
		self.lower_k = self.k - random.uniform(0.01, k_max/2.0)
		if self.upper_k > k_max:
			self.upper_k = k_max
		if self.lower_k <0:
			self.lower_k = 0.01

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
		if users[j].k > i*d and users[j].k < (i+1)*d:
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
	for i in range(1, m):
		if len(T_k_arr[i])>0 and len(T_k_arr[i])<2:
			changed = True;
			k = 1
			while not len(T_k_arr[i-k]) > 0:
				k = k + 1
			for user in users:
				if user.s < (i+1)*d:
					user.n_tasks = user.n_tasks + k
					user.p = user.p + k*d
			T_k_arr[i-k] = T_k_arr[i-k] + T_k_arr[i]
			T_k_arr[i] = deepcopy(T_k_arr[i-k])
	
###############################################################
# We consider different collusion sizes.
# number of colluded users
n_collusion = 0
# colluded users
colluded_users = []
# Let the maximum perturbation on user strategies when collusion be 5.
max_perturb = 5.0
# There are 1000 test samples.
n_tests = 1000
# new platform utility
new_u_p = R
# The outputs will be stored in the text file ratio_group_con.txt
f = open('ratio_group_dis.txt', 'w')

for n_collusion in range(2, 2*n/3, (n-2)/10):
	# ratio of the loss users
	ratio_loss = 0.0
	# the standard deviation of the ratio above
	dev_ratio = 0.0
	arr_ratio = []
	# loss of platform utility
	u_p_loss = 0.0
	# the standard deviation of the u_p loss above
	dev_u_p = 0.0
	arr_u_p = []
	for i in range(n_tests):
		# deep copy of the user arrays
		copy_users = deepcopy(users)
		new_u_p = R;
		# Initialize the colluded users
		colluded_users = []
		for j in range(n_collusion):
			while True:
				k = random.randint(0, n-1)
				if k not in colluded_users:
					break
			colluded_users.append(k)
		for k in colluded_users:
			# give perturbations on the copied user strategies
			copy_users[k].s = copy_users[k].s + random.uniform(0, 2.0*max_perturb) - max_perturb
			if copy_users[k].s < 0.01:
				copy_users[k].s = 0.01
		# Let us recompute the sensing times and the payments.
		# We also recalculate each user utility and the platform utility.
		for user in copy_users:
			user.n_tasks = m - math.floor(user.s / d)
			if user.n_tasks < 0:
				user.n_tasks = 0
			user.p = d * user.n_tasks * (2*m + 1 - user.n_tasks) / 2.0
			user.u = user.p - user.k * user.n_tasks
			new_u_p = new_u_p - user.p
		# Adjust the partitions.
		changed = True;	# whether exists k s.t. |T_k| < 2 ?
		while changed:
			changed = False;
			for i in range(1, m):
				if len(T_k_arr[i])>0 and len(T_k_arr[i])<2:
					changed = True;
					k = 1
					while not len(T_k_arr[i-k]) > 0:
						k = k + 1
					for user in copy_users:
						if user.s < (i+1)*d:
							user.n_tasks = user.n_tasks + k
							user.p = user.p + k*d
					T_k_arr[i-k] = T_k_arr[i-k] + T_k_arr[i]
					T_k_arr[i] = deepcopy(T_k_arr[i-k])
		# Let us count how many users suffer utility loss
		n_loss = 0
		for j in range(n):
			if copy_users[j].u < users[j].u:
				n_loss = n_loss + 1
		# statistics
		ratio_loss = ratio_loss + n_loss*1.0 / n_collusion
		u_p_loss = u_p_loss - new_u_p + u_p
		# save for later: i.e. variance computation
		arr_ratio.append(n_loss*1.0 / n_collusion)
		arr_u_p.append(u_p - new_u_p)
		
	# Calculate the variances
	for r in arr_ratio:
		dev_ratio = dev_ratio + (r-ratio_loss / n_tests)**2
	for r in arr_u_p:
		dev_u_p = dev_u_p + (r-u_p_loss / n_tests)**2
	# Output the statistical results.
	f.write('{0:f} {1:f} {2:f} {3:f} {4:f}\n'.format(n_collusion, ratio_loss / n_tests, (dev_ratio / n_tests)**0.5, u_p_loss / n_tests, (dev_u_p / n_tests)**0.5))
	
f.close()



###############################################################
# We consider different strategies' perturbation sizes.
# Let the number of colluded users be half of n.
n_collusion = n/2+1
# colluded users
colluded_users = []
# The perturbation sizes on user strategies when collusion.
max_perturb = 1.0
# There are 1000 test samples.
n_tests = 1000
# new platform utility
new_u_p = R
# The outputs will be stored in the text file perturb_group_con.txt
f = open('perturb_group_dis.txt', 'w')

for max_perturb in range(1, 11):
	# ratio of the loss users
	ratio_loss = 0.0
	# the standard deviation of the ratio above
	dev_ratio = 0.0
	arr_ratio = []
	# loss of platform utility
	u_p_loss = 0.0
	# the standard deviation of the u_p loss above
	dev_u_p = 0.0
	arr_u_p = []
	for i in range(n_tests):
		# deep copy of the user arrays
		copy_users = deepcopy(users)
		new_u_p = R;
		# Initialize the colluded users
		colluded_users = []
		for j in range(n_collusion):
			while True:
				k = random.randint(0, n-1)
				if k not in colluded_users:
					break
			colluded_users.append(k)
		for k in colluded_users:
			# give perturbations on the copied user strategies
			copy_users[k].s = copy_users[k].s + random.uniform(0, 2.0*max_perturb) - max_perturb
			if copy_users[k].s < 0.01:
				copy_users[k].s = 0.01
		# Let us recompute the sensing times and the payments.
		# We also recalculate each user utility and the platform utility.
		for user in copy_users:
			user.n_tasks = m - math.floor(user.s / d)
			if user.n_tasks < 0:
				user.n_tasks = 0
			user.p = d * user.n_tasks * (2*m + 1 - user.n_tasks) / 2.0
			user.u = user.p - user.k * user.n_tasks
			new_u_p = new_u_p - user.p
		# Adjust the partitions.
		changed = True;	# whether exists k s.t. |T_k| < 2 ?
		while changed:
			changed = False;
			for i in range(1, m):
				if len(T_k_arr[i])>0 and len(T_k_arr[i])<2:
					changed = True;
					k = 1
					while not len(T_k_arr[i-k]) > 0:
						k = k + 1
					for user in copy_users:
						if user.s < (i+1)*d:
							user.n_tasks = user.n_tasks + k
							user.p = user.p + k*d
					T_k_arr[i-k] = T_k_arr[i-k] + T_k_arr[i]
					T_k_arr[i] = deepcopy(T_k_arr[i-k])
		# Let us count how many users suffer utility loss
		n_loss = 0
		for j in range(n):
			if copy_users[j].u < users[j].u:
				n_loss = n_loss + 1
		# statistics
		ratio_loss = ratio_loss + n_loss*1.0 / n_collusion
		u_p_loss = u_p_loss - new_u_p + u_p
		# save for later: i.e. variance computation
		arr_ratio.append(n_loss*1.0 / n_collusion)
		arr_u_p.append(u_p - new_u_p)
		
	# Calculate the variances
	for r in arr_ratio:
		dev_ratio = dev_ratio + (r-ratio_loss / n_tests)**2
	for r in arr_u_p:
		dev_u_p = dev_u_p + (r-u_p_loss / n_tests)**2
	# Output the statistical results.
	f.write('{0:f} {1:f} {2:f} {3:f} {4:f}\n'.format(max_perturb, ratio_loss / n_tests, (dev_ratio / n_tests)**0.5, u_p_loss / n_tests, (dev_u_p / n_tests)**0.5))
	
f.close()