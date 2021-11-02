import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy import stats
d = 0

t = 10000

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
	
def calculate_cost (a,p) :
	road1_real_traffic = 0
	road2_real_traffic = 0
	road1_observed_traffic = 0
	road2_observed_traffic = 0
	probability_sum = 0
	flow = np.random.geometric(p, size=t)
	cost = 0
	for i in range(t):   
		road1_observed_traffic -= 1 if road1_observed_traffic > 0 else 0
		road1_real_traffic -= 1 if road1_real_traffic > 0 else 0
		road2_observed_traffic -= 1 if road2_observed_traffic > 0 else 0
		road2_real_traffic -= 1 if road2_real_traffic > 0 else 0
		           		
		random_generator = random.randint(0,len(flow)-1)
		current = flow[random_generator]
		flow[random_generator] = flow[len(flow)-1]
		flow.pop()    
		false_num = 0       
		check = random.randint(0,100-1)            # check the traffic
		if check < 100*d : check = 1               
		else: check = 0  
	 
		attack = random.randint(0,100-1)
		if attack < 100*a: attack = 1              # give an attack
		else: attack = 0 
		left_add, right_add = distribute(road1_observed_traffic, road2_observed_traffic, current + attack)
		road1_observed_traffic += left_add
		road2_observed_traffic += right_add
		false_goes_to_left = attack if road1_real_traffic < road2_real_traffic else 0
		road1_real_traffic += left_add - false_goes_to_left
		road2_real_traffic += right_add - (attack - false_goes_to_left)
	
		cost += (road1_real_traffic+road2_real_traffic)/t
	return cost


cost_sequence = []
absolute_cost_sequence = []
no_attack_sequence = []


for i in range(0,11):
	cost = calculate_cost(0.4,0.5+i*0.02)
	no_attack = calculate_cost(0,0.5+i*0.02)
	pure = cost - no_attack
	cost_sequence.append(cost)
	absolute_cost_sequence.append(pure)
	no_attack_sequence.append(no_attack)
	
x = np.linspace(0.6,0.8,11)
plt.plot(x,cost_sequence,'b')
plt.plot(x,absolute_cost_sequence,'y')
plt.plot(x,no_attack_sequence,'r')
plt.title("graph for d = "+str(d)+" and a = "+str(0.4))
plt.show()
	
	
