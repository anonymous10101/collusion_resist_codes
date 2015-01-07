# This program verifies the continuous crowdsensing game model is n-truthful.

import random
import math
from copy import deepcopy
# Let there be 100 users.
n = 100
# Let the upper bound of the users' unit costs be 10.
k_max = 10.0
# Let the upper bound of the revenue coefficients be 20.
lambda_max = 20.0
# Baseline reward of the platform is 100.
R = 100
# Platform utility
u_p = R

class SensingUser:
	'''the class for a user participating in sensing.'''
	k = 0;	# the unit cost
	s = 0;	# the user strategy
	l = 0;	# the revenue coefficient
	t = 0;	# sensing time of this user
	p = 0;	# payment to this user
	u = 0;	# user utility
	def __init__(self):
		# The initial s_i = kappa_i
		self.s = self.k = random.uniform(0.01, k_max)
		self.l = random.uniform(0.01, lambda_max)

# Initialize the users.
users = []
for i in range(n):
	users.append(SensingUser())

# Let us compute the sensing time and the payment for each user.
# Also we calculate each user utility and the platform utility.
for user in users:
	if user.s < user.l:
		user.t = user.l / user.s - 1.0
		user.p = user.l * math.log(user.l / user.s)
		user.u = user.p - user.k * user.t
		u_p = u_p + user.l * math.log(1+user.t) - user.p
	else:
		user.t = user.p = user.u = 0

###############################################################
# We consider different collusion sizes.
# number of colluded users
n_collusion = 0
# colluded users
colluded_users = []
# Let the maximum perturbation on user strategies when collusion be 1.
max_perturb = 1.0
# There are 1000 test samples.
n_tests = 1000
# new platform utility
new_u_p = R
# The outputs will be stored in the text file loss_truthful_con.txt
f = open('loss_truthful_con.txt', 'w')

for n_collusion in range(2, 2*n/3, (n-2)/10):
	# lost utility of the colluded users
	utility_loss = 0.0
	# the standard deviation of the loss above
	dev_u = 0.0
	arr_u = []
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
			copy_users[k].s = copy_users[k].s + random.uniform(0, 2.0* max_perturb) - max_perturb
			if copy_users[k].s < 0.01:
				copy_users[k].s = 0.01
		# Let us recompute the sensing times and the payments.
		# We also recalculate each user utility and the platform utility.
		for user in copy_users:
			if user.s < user.l:
				user.t = user.l / user.s - 1.0
				user.p = user.l * math.log(user.l / user.s)
				user.u = user.p - user.k * user.t
				new_u_p = new_u_p + user.l * math.log(1+user.t) - user.p
			else:
				user.t = user.p = user.u = 0
		# Let us count how much utility the colluded users lose
		u_loss = 0
		for j in colluded_users:
			u_loss = u_loss + users[j].u - copy_users[j].u
		# statistics
		utility_loss = utility_loss + u_loss / n_collusion
		u_p_loss = u_p_loss - new_u_p + u_p
		# save for later: i.e. variance computation
		arr_u.append(u_loss / n_collusion)
		arr_u_p.append(u_p - new_u_p)
		
	# Calculate the variances
	for r in arr_u:
		dev_u = dev_u + (r-utility_loss / n_tests)**2
	for r in arr_u_p:
		dev_u_p = dev_u_p + (r-u_p_loss / n_tests)**2
	# Output the statistical results.
	f.write('{0:f} {1:f} {2:f} {3:f} {4:f}\n'.format(n_collusion, utility_loss / n_tests, (dev_u / n_tests)**0.5, u_p_loss / n_tests, (dev_u_p / n_tests)**0.5))
	
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
# The outputs will be stored in the text file perturb_truthful_con.txt
f = open('perturb_truthful_con.txt', 'w')

for max_perturb in range(1, 11):
	# lost utility of the colluded users
	utility_loss = 0.0
	# the standard deviation of the loss above
	dev_u = 0.0
	arr_u = []
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
			copy_users[k].s = copy_users[k].s + random.uniform(0, 2.0* max_perturb) - max_perturb
			if copy_users[k].s < 0.01:
				copy_users[k].s = 0.01
		# Let us recompute the sensing times and the payments.
		# We also recalculate each user utility and the platform utility.
		for user in copy_users:
			if user.s < user.l:
				user.t = user.l / user.s - 1.0
				user.p = user.l * math.log(user.l / user.s)
				user.u = user.p - user.k * user.t
				new_u_p = new_u_p + user.l * math.log(1+user.t) - user.p
			else:
				user.t = user.p = user.u = 0
		# Let us count how much utility the colluded users lose
		u_loss = 0
		for j in colluded_users:
			u_loss = u_loss + users[j].u - copy_users[j].u
		# statistics
		utility_loss = utility_loss + u_loss / n_collusion
		u_p_loss = u_p_loss - new_u_p + u_p
		# save for later: i.e. variance computation
		arr_u.append(u_loss / n_collusion)
		arr_u_p.append(u_p - new_u_p)
		
	# Calculate the variances
	for r in arr_u:
		dev_u = dev_u + (r-utility_loss / n_tests)**2
	for r in arr_u_p:
		dev_u_p = dev_u_p + (r-u_p_loss / n_tests)**2
	# Output the statistical results.
	f.write('{0:f} {1:f} {2:f} {3:f} {4:f}\n'.format(max_perturb, utility_loss / n_tests, (dev_u / n_tests)**0.5, u_p_loss / n_tests, (dev_u_p / n_tests)**0.5))
	
f.close()