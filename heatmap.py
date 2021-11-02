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
		
	return cost*p + d - a
		
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
		heatmap[10-i][k] = cost/100
	#plt.plot(x,cost_sequence,label = "a = "+ str(a))

ax = sns.heatmap(heatmap,xticklabels=False, yticklabels=False,cmap="YlGnBu",vmax=2.5)
ax.set_xlabel("d",fontsize = 15)
ax.set_ylabel("a",fontsize = 15)
plt.savefig("heatmap" + '.png', dpi=300)
#plt.legend()
#plt.show()
'''
start_a = 5 # a = 3*0.05
start_d = 5 # d = 5*0.05
initial_cost = heatmap[start_a][start_d]
time = 100
while time :
	time -= 1
	line = heatmap[start_a]
	d_max = 10
	d_loc = 0
	for i in range(21):
		if line[i] == 0:
			continue
		if line[i] < d_max :
			d_loc = i
			d_max = line[i]	
	a_min = 0
	a_loc = 0
	line = heatmap[:,d_loc]
	for i in range(11):
		if line[i] > a_min :
			a_loc = i
			a_min = line[i]
	print(d_loc)
	print(a_loc)
	print(heatmap[a_loc][d_loc])
	if (abs(heatmap[a_loc][d_loc] - heatmap[start_a][start_d]) < 0.01*(heatmap[a_loc][d_loc] + heatmap[start_a][start_d])) :
		print("d is "+str(0.05*start_d))
		print("a is "+str(0.05*start_a))
		print("initial cost is "+str(initial_cost))
		print("cost after game is "+str(heatmap[a_loc][d_loc]))
		break
	start_a = a_loc
	start_d = d_loc
	'''
	
