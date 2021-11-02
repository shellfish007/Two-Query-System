import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns; 
import cv2

t = 1000

def cost_fun(length, arrival):
	return (2*length + arrival)*arrival/2/t

def distribute (left,right,quant):
	left_add = 0
	right_add = 0
	if (abs(left-right) > quant):
		left_add = quant if left < right else 0
		right_add = quant if left > right else 0
	elif (left+right+quant)%2:  # is odd
	    coin = random.randint(0,1)
	    left_add = (-left+right+quant-1)/2 + coin
	    right_add = (left-right+quant-1)/2 + 1-coin
	else:
		left_add = (-left+right+quant)/2 
		right_add = (left-right+quant)/2
	return left_add,right_add

flow = np.random.poisson(1/0.7, size=t)
def calculate_cost(d,a,p):
	road1_real_traffic = 0
	road2_real_traffic = 0
	road1_observed_traffic = 0
	road2_observed_traffic = 0
	cost = 0
	#d = 0.4 # probability of checking
	#a = 0 # probalibity of attack
	#p = 0.7  # probality of geometrical distribution 
	for i in range(t):
		current = flow[i]		
		attack = random.randint(0,100-1)
		if attack < 100*a: attack = 1              # give an attack
		else: attack = 0 
		check = random.randint(0,100-1)            # check the traffic
		if check < 100*d : attack = 0               
		left_add, right_add = distribute(road1_observed_traffic, road2_observed_traffic, current + attack)
		road1_observed_traffic += left_add
		road2_observed_traffic += right_add
		false_goes_to_left = attack if road1_real_traffic < road2_real_traffic else 0
	
		cost += cost_fun(road1_real_traffic,left_add - false_goes_to_left) + cost_fun(road2_real_traffic,right_add - (attack - false_goes_to_left))
	
		road1_observed_traffic -= 1 if road1_observed_traffic >0 else 0
		road1_real_traffic -= 1 if road1_real_traffic >0 else 0
		road2_observed_traffic -= 1 if road2_observed_traffic >0 else 0
		road2_real_traffic -= 1 if road2_real_traffic >0 else 0
	
		road1_real_traffic += left_add - false_goes_to_left
		road2_real_traffic += right_add - (attack - false_goes_to_left)
		
	return cost*p

x = np.linspace(0,1,21)
heatmap = np.zeros((11,21))
for i in range(0,11):
	cost_sequence = []
	a = 0.03*i
	for k in range(21):
		cost = 0
		d = k*0.05
		for j in range(100):
			cost += calculate_cost(d,a,0.7)
		cost_sequence.append(cost/100)
		heatmap[i][k] = cost/100
	#plt.plot(x,cost_sequence,label = "a = "+ str(a))

def balance(c1,c2): 
	curmap = np.zeros((11,21))
	for i in range(11):
		a = 0.03*i
		for k in range(21):
			d = k*0.05
			curmap[i][k] = heatmap[i][k] + c1*d - c2*a	
	start_a = 10 # a = 3*0.03
	start_d = 0 # 
	time = 100
	balanced = 0
	while time :
		time -= 1
		line = curmap[start_a]
		d_min = 100
		d_loc = 0
		# defender move. 
		for i in range(3):
			if start_d - 1 + i > 20  or start_d -1 + i < 0 or line[start_d -1 + i] == 0:
				continue
			if line[start_d -1 + i] < d_min :
				d_loc = start_d - 1 + i
				d_min = line[d_loc]	
		if d_loc == start_d :
			balanced = 1
		a_max = 0 
		a_loc = 0
		line = curmap[:,d_loc]
		for i in range(3):
			if start_a -1 + i < 0 or start_a - 1 + i > 10 or line[start_a -1 + i] == 0:
				continue
			if line[start_a-1 + i] > a_max :
				a_loc = start_a - 1 + i
				a_max = line[a_loc]
		if time == 0:
			return -1,-1
		if a_loc == start_a and balanced == 1:
			return start_a,start_d
		balanced = 0
		start_a = a_loc
		start_d = d_loc
	return start_a,start_d
	
length = 20
locmap = np.zeros((1+length,1+length))
d_graph = np.zeros((1+length,1+length))
a_graph = np.zeros((1+length,1+length))

for i in range(1+length) :
	c1 = 1/length*i
	for j in range(1+length) :
		c2 = 1/length*j
		best_a,best_d = balance(c1,c2)
		d_graph[length-i][j] = best_d
		a_graph[length-i][j] = best_a
		if best_a == -1 and best_d == -1 :
			locmap[length-i][j] = 1
		elif best_a < 5 and best_d < 10 :
			locmap[length-i][j] = 2
		elif best_a < 5 and best_d >= 10 :
			locmap[length-i][j] = 3
		elif best_a >= 5 and best_d < 10 :
			locmap[length-i][j] = 4
		elif best_a >= 5 and best_d >= 10 :
			locmap[length-i][j] = 5
ax = sns.heatmap(locmap,xticklabels=False, yticklabels=False,cmap="YlGnBu")
ax.set_xlabel("d",fontsize = 15)
ax.set_ylabel("a",fontsize = 15)
plt.savefig("SingleStep_locmap" + '.png', dpi=300)
print(locmap)



