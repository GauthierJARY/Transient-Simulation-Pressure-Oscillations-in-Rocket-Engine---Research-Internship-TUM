# -*- coding: utf-8 -*-
"""
Created on Thu May 25 16:02:28 2023

@author: gauth
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import sys

P0 = 1e5
partial_V = 0
V0 = 0.1**2 * 3.14 * 0.2
rho_in = 1141
T_in = 90
P_in = 100e5
A1 = 0.025**2 * 3.14
A12 = 0.05**2 * 3.14
gamma=1.3
t=0
dt=0.0001
P=[]
P2=[]
P_prev = P0
P_prev2 = P0
beta=50000
C=1
A2 = 0.1**2 * 3.14
n_iteration = int(18e3)
time_simulation = n_iteration * dt
while t<0.05:
    t = t + dt
    Q_in = C/np.sqrt(  (A2/A1)**2-1  ) * A2 * np.sign(-P_prev+P_in) * np.sqrt( 2 * rho_in * np.abs(-P_prev+P_in) )
    # Q_in =200
    partial_V = Q_in * dt + partial_V
    if partial_V >= 1 :
        P_next = P_prev + dt * beta / V0 * Q_in 
        #P_next = P_prev + dt * beta/V0 * C * np.sign(-P_prev+P_in) * A2 / rho_in / (np.sqrt(-1+(A2/A1)**2)) * np.sqrt(2*rho_in*np.abs(P_prev-P_in))
        #P_next2 = P_prev2 + dt * beta/V0 * C * np.sign(-P_prev2+P_in) * A2 / rho_in / (np.sqrt(-1+(A2/A12)**2)) * np.sqrt(2*rho_in*np.abs(P_prev2-P_in))
    else : 
        P_next = P_prev
    
    P_prev = P_next
    P.append(P_next)


    
plt.figure()   
A12=round(A12*1e5)
A1=round(A1*1e5)
plt.plot(P, label=f'{beta} Pa')
plt.title(f'presssure evolution in filling of LOx of a tank of volume ={V0} m^3 with P_in={P_in} Pa \n')
plt.xlabel(r'$time$ (ms)')
plt.legend(title='bulk modulus')
plt.ylabel(r'$Pressure$ (Pa)')
# value for bulk = 5000 are in P4
P4=[100000.0,
 100000.0,
 100000.0,
 335312.68309109355,
 567811.979195795,
 797497.6823085486,
 1024369.5812987094,
 1248427.4597164732,
 1469671.095588868,
 1688100.2612051587,
 1903714.7228909726,
 2116514.2407703907,
 2326498.5685151923,
 2533667.453080373,
 2738020.634424983,
 2939557.8452172508,
 3138278.8105228664,
 3334183.24747521,
 3527270.86492619,
 3717541.363076247,
 3904994.433081939,
 4089629.756639389,
 4271447.005541698,
 4450445.8412082605,
 4626625.914183709,
 4799986.863603997,
 4970528.316626879,
 5138249.887823755,
 5303151.178529548,
 5465231.776146933,
 5624491.25340081,
 5780929.167538507,
 5934545.059470659,
 6085338.4528471595,
 6233308.853061908,
 6378455.746179359,
 6520778.59777502,
 6660276.8516810695,
 6796949.928627193,
 6930797.224765411,
 7061818.11006624,
 7190011.926571822,
 7315377.986489654,
 7437915.570108292,
 7557623.923513689,
 7674502.256081693,
 7788549.7377185095,
 7899765.495816584,
 8008148.611888132,
 8113698.117832389,
 8216412.991785207,
 8316292.153490766,
 8413334.459124347,
 8507538.695482066,
 8598903.573437432,
 8687427.72054497,
 8773109.672646748,
 8855947.864307348,
 8935940.617864734,
 9013086.130836317,
 9087382.46135808,
 9158827.511255572,
 9227419.006242888,
 9293154.472610839,
 9356031.209586458,
 9416046.256305229,
 9473196.352009425,
 9527477.887632456,
 9578886.846291894,
 9627418.729302283,
 9673068.462988451,
 9715830.279594643,
 9755697.562545884,
 9792662.641531164,
 9826716.515084477,
 9857848.465154145,
 9886045.504810603,
 9911291.556628807,
 9933566.172213454,
 9952842.414512685,
 9969083.0686941,
 9982233.074028483,
 9992201.667487761,
 9998805.995167421,
 10001390.222887965,
 9998601.727338875,
 10001398.284313701,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725,
 9998601.715686275,
 10001398.284313725]

