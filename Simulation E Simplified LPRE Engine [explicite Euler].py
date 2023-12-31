# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 18:27:38 2023

@author: gauth
"""


# =============================================================================
# Imported modules 
# =============================================================================
import scipy as scipy
import numpy as np
import math
import matplotlib.pyplot as plt
import sys
from scipy.optimize import fsolve
import time 

# =============================================================================
# Geometric parametrisation Input 
# =============================================================================

l_tank = 10
d_tank = 1
A_tank = (d_tank/2)**2 * 3.14
V_tank = l_tank * A_tank

l_pipe = 2
d_pipe = 0.01
A_pipe = (d_pipe/2)**2 * 3.14
V_pipe = l_pipe * A_pipe

l_dome = 0.1
d_dome = 0.15
A_dome = (d_dome/2)**2 * 3.14
V_dome = l_dome * A_dome

NI = 5 # number of injectors at the end of injection dome of each species

l_injector = 0.05
d_injector = 0.003
A_injector = (d_injector/2)**2 * 3.14
V_injector = l_injector * A_injector

l_combustor = 0.2
d_combustor = 0.08 
A_combustor = (d_combustor/2)**2 * 3.14
V_combustor =  A_combustor * l_combustor 
A_throat = 0.01

# =============================================================================
# Constant values and parameters
# =============================================================================

R = 8.734
R_cc = R/(29e-3)

T3 = 3500 #K

t = 0 #s
dt = 1e-7

gamma = 1.3

# dynamic viscosity
eta_oxygene = 42e-6
eta_propane = 117e-6 # Pa/s

zeta_geo_1 = 0
zeta_geo_2 = (1-d_pipe/d_dome)**2
zeta_geo_4 = 0
zeta_geo_5 = (1-d_pipe/d_dome)**2
zeta_geo_6 = 30
zeta_geo_7 = 2.85 #(1-d_injector/d_combustor)**2 #2.85
zeta_geo_8 = 30
zeta_geo_9 = 2.85 #2.85

density_oxygene = 1141
density_fuel = 500

bulk_modulus_oxygene = 0.2e9 # bulk modulus species
bulk_modulus_fuel = 0.36e9

material_pipe = 50e9 #Young modulus materail aluminium
material_dome = 50e9
material_injector = 50e9

g = 9.81 # gravity constant 

# =============================================================================
# Initial values of my variables - pre-Initialisation
# =============================================================================

P0i = 40e5 # Pa
P1i = 10e5
P2i = 10e5
P3i = 40e5
P4i = 10e5
P5i = 10e5
P6i = 10e5
P7i = 10e5
P8i = 10e5
P9i = 10e5
m0i = 0.01 # kg/s
m1i = 0.01 # kg/s
m2i = 0.01
m3i = 0.01
m4i = 0.01
m5i = 0.01
m6i = 0.01
m7i = 0.01
m8i = 0.01
m9i = 0.01
m10i = 0.01
T10i = 3000 # K


# =============================================================================
# Initialisation of my variables
# =============================================================================

P0 = P0i + density_oxygene*g*l_tank
P1 = P1i
P2 = P2i
P3 = P3i + density_fuel*g*l_tank
P4 = P4i
P5 = P5i
P6 = P6i
P7 = P7i
P8 = P8i
P9 = P9i
m0 = m0i
m1 = m1i
m2 = m2i
m3 = m3i
m4 = m4i
m5 = m5i
m6 = m6i
m7 = m7i
m8 = m8i
m9 = m9i
m10 = m10i
T10 = T10i

# =============================================================================
# Few functions for calculus
# =============================================================================

def a_sound(density, bulk_modulus,length, material):
    # return ( bulk_modulus / density ) / (1+(diameter/0.02)*(bulk_modulus/material)) # corrected speed of sound
    return  bulk_modulus / density # non corrected speed of sound of water 

def Reynolds(m_flow, length, section, eta):
    m=m_flow
    if m_flow==0:
        m=1e-12
    return (m * length ) / ( section * eta )


# =============================================================================
# Plots lists for saving results
# =============================================================================
list_pressure_0, list_pressure_1, list_pressure_2, list_pressure_3, list_pressure_4, list_pressure_5, list_pressure_6, list_pressure_7, list_pressure_8, list_pressure_9 = [], [], [], [], [], [], [], [], [], []
list_mass_flow_0, list_mass_flow_1, list_mass_flow_2, list_mass_flow_3, list_mass_flow_4, list_mass_flow_5, list_mass_flow_6, list_mass_flow_7, list_mass_flow_8, list_mass_flow_9, list_mass_flow_10 = [], [], [], [], [], [], [], [], [], [], []
list_temperature_10 = []
time_storage = []


# =============================================================================
# MAIN LOOP TO SIMULATE
# =============================================================================

start = time.time() 
print("Start computing") 

while t<0.05: 
    
    # =========================================================================
    # Calculus 
    # =========================================================================
    
    t = t + dt
    # P3n = P3 - dt * m3 *g/A_tank 
    P0n = P0 - dt * ( - a_sound(density_oxygene, bulk_modulus_oxygene,l_pipe, material_pipe) / V_pipe * (m0 - m1) )
    P1n = P1 - dt * ( - a_sound(density_oxygene, bulk_modulus_oxygene,l_pipe, material_pipe) / V_pipe * (m1 - m2)  ) 
    P3n = P3 - dt * ( - a_sound(density_fuel, bulk_modulus_fuel,l_pipe, material_pipe) / V_pipe * (m3 - m4) )
    P4n = P4 - dt * ( - a_sound(density_fuel, bulk_modulus_fuel,l_pipe, material_pipe) / V_pipe * (m4 - m5) )
    zeta_fluid_1 = 64/Reynolds(m1,l_pipe,A_pipe, eta_oxygene)*1/d_pipe *l_pipe
    xi1 = 0.5 * A_pipe**(-2) * ( zeta_fluid_1 + zeta_geo_1 )
    m1n = m1 - dt * ( - A_pipe/l_pipe * (P0 - P1 - xi1 / density_oxygene * m1*np.abs(m1) ) )
    m0n = m1n / ( 1 + ( (V_pipe / a_sound(density_oxygene, bulk_modulus_oxygene,l_pipe, material_pipe) )/ (g/A_tank) ) )
    zeta_fluid_2 = 64/Reynolds(m2,l_pipe,A_pipe, eta_oxygene)*1/d_pipe *l_pipe
    xi2 = 0.5 * A_pipe**(-2) * ( zeta_fluid_2 + zeta_geo_2 )
    m2n = m2 - dt * ( - A_pipe/l_pipe * (P1 - P2 - xi2 / density_oxygene * m2*np.abs(m2) ) )
    zeta_fluid_4 = 64/Reynolds(m4,l_pipe,A_pipe, eta_propane)*1/d_pipe *l_pipe
    xi4 = 0.5 * A_pipe**(-2) * ( zeta_fluid_4 + zeta_geo_4 )
    m4n = m4 - dt * ( - A_pipe/l_pipe * (P3 - P4 - xi4 / density_fuel * m4*np.abs(m4)) )
    m3n = m4n / ( 1 + ( (V_pipe / a_sound(density_fuel, bulk_modulus_fuel,l_pipe, material_pipe) )/ (g/A_tank) ) )
    zeta_fluid_5 = 64/Reynolds(m5,l_pipe,A_pipe, eta_propane)*1/d_pipe *l_pipe
    xi5 = 0.5 * A_pipe**(-2) * ( zeta_fluid_5 + zeta_geo_5 )
    m5n = m5 - dt * ( - A_pipe/l_pipe * (P4 - P5 - xi5 / density_fuel * m5*np.abs(m5)) )
    P2n = P2 - dt * ( - a_sound(density_oxygene, bulk_modulus_oxygene,l_dome, material_dome) / V_dome * (m2 - m6) )
    zeta_fluid_6 = 64/Reynolds(m6,l_dome,A_dome, eta_oxygene)*1/d_dome *l_dome
    xi6 = 0.5 * A_dome**(-2) * ( zeta_fluid_6 + zeta_geo_6 )
    m6n = m6 - dt * ( - A_dome/l_dome * (P2 - P6 - xi6 / density_oxygene * m6*np.abs(m6)) )
    P6n = P6 - dt * ( - a_sound(density_oxygene, bulk_modulus_oxygene,l_injector, material_injector) / V_injector * (m6/NI - m7/NI) )
    zeta_fluid_7 = 64/Reynolds(m7,l_injector,A_injector, eta_oxygene)*1/d_injector *l_injector
    xi7 = 0.5 * A_injector**(-2) * ( zeta_fluid_7 + zeta_geo_7 )
    m7n = m7 - dt * NI * ( - A_injector/l_injector * ( P6 - P7 - xi7 / density_oxygene * m7*np.abs(m7)/NI**2 ) )
    P5n = P5 - dt * ( - a_sound(density_fuel, bulk_modulus_fuel,l_dome, material_dome) / V_dome * (m5 - m8) )
    zeta_fluid_8 = 64/Reynolds(m8,l_dome,A_dome, eta_propane)*1/d_dome *l_dome
    xi8 = 0.5 * A_dome**(-2) * ( zeta_fluid_8 + zeta_geo_8 )
    m8n = m8 - dt * (- A_dome/l_dome * (P5 - P8 - xi8 / density_fuel * m8*np.abs(m8)) )
    P8n = P8 - dt * ( - a_sound(density_fuel, bulk_modulus_fuel,l_injector, material_injector) / V_injector * (m8/NI - m9/NI) )
    zeta_fluid_9 = 64/Reynolds(m9,l_injector,A_injector, eta_propane)*1/d_injector *l_injector
    xi9 = 0.5 * A_injector**(-2) * ( zeta_fluid_9 + zeta_geo_9 )
    m9n = m9 - dt * NI * ( - A_injector/l_injector * ( P8 - P9 - xi9 / density_oxygene * m9*np.abs(m9)/NI**2 ) ) 
    T10n = 3000
    P7n = P7 - dt * (m10 - m9 - m7) * R_cc * T10 / V_combustor
    P9n = P7n
    m10n = - ( - ( np.sqrt(gamma * (2/(gamma+1) )**((gamma+1)/(gamma-1)) ) * A_throat )/(np.sqrt(R_cc * T10n)) * P7n ) 

    # =========================================================================
    # Integrate 
    # =========================================================================
    P0, P1, P2, P3, P4, P5, P6, P7, P8, P9 = P0n, P1n, P2n, P3n, P4n, P5n, P6n, P7n, P8n, P9n
    m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10 = m0n, m1n, m2n, m3n, m4n, m5n, m6n, m7n, m8n, m9n, m10n
    T10 = T10n

    # =========================================================================
    # SAVE 
    # =========================================================================
    
    list_pressure = [list_pressure_0, list_pressure_1, list_pressure_2, list_pressure_3, list_pressure_4, list_pressure_5, list_pressure_6, list_pressure_7, list_pressure_8, list_pressure_9]
    list_mass_flow = [list_mass_flow_0, list_mass_flow_1, list_mass_flow_2, list_mass_flow_3, list_mass_flow_4, list_mass_flow_5, list_mass_flow_6, list_mass_flow_7, list_mass_flow_8, list_mass_flow_9, list_mass_flow_10]
    
    for i in range(10):
        list_pressure[i].append(globals()[f'P{i}'])
        if i == 7:
            list_mass_flow[i].append(globals()[f'm{i}'] / NI)
        elif i == 9:
            list_mass_flow[i].append(globals()[f'm{i}'] / NI)
        else:
            list_mass_flow[i].append(globals()[f'm{i}'])
    
    list_temperature_10.append(T10)
    time_storage.append(t)
    
end = time.time() 
print(f'time of simulation : {end - start}')   


# =============================================================================
# Plots and graphs 
# =============================================================================

plt.figure()
plt.plot(time_storage[::10],list_pressure_0[::10])
plt.plot(time_storage[::10],list_pressure_1[::10])
plt.plot(time_storage[::10],list_pressure_2[::10])
plt.plot(time_storage[::10],list_pressure_6[::10])
plt.plot(time_storage[::10],list_pressure_7[::10])

plt.title(f'Pressure evolution Tank-Pipe-Pipe-Dome-Injectors-Combustor \n Oxygene Line with T3 = {T3}K \n')
plt.xlabel(r'$time$ (s)')
plt.legend(['pipe1','pipe2', 'dome', 'injector', 'combustor'])
plt.ylabel(r'$Pressure$ (Pa)')

plt.figure()
plt.plot(time_storage[::10],list_pressure_3[::10])
plt.plot(time_storage[::10],list_pressure_4[::10])
plt.plot(time_storage[::10],list_pressure_5[::10])
plt.plot(time_storage[::10],list_pressure_8[::10])
plt.plot(time_storage[::10],list_pressure_9[::10])

plt.title(f'Pressure evolution for Tank-Pipe-Pipe-Dome-Injectors-Combustor \n Propane Line with T3 = {T3}K \n')
plt.xlabel(r'$time$ (s)')
plt.legend(['pipe1','pipe2', 'dome', 'injector', 'combustor'])
plt.ylabel(r'$Pressure$ (Pa)')


plt.figure()
plt.plot(time_storage[::10],list_mass_flow_0[::10])
plt.plot(time_storage[::10],list_mass_flow_1[::10])
plt.plot(time_storage[::10],list_mass_flow_2[::10])
plt.plot(time_storage[::10],list_mass_flow_6[::10])
plt.plot(time_storage[::10],list_mass_flow_7[::10])
plt.plot(time_storage[::10],list_mass_flow_10[::10])

plt.title(f'massflow evolution Tank-Pipe-Pipe-Dome-Injectors-Combustor \n Oxygene with T3 = {T3}K  \n')
plt.xlabel(r'$time$ (s)')
plt.legend(['tank','pipe','pipe','dome','injector','combustor out'])
plt.ylabel(r'$mass flow$ (kg/s)')
plt.ylim(0,5)

plt.figure()
plt.plot(time_storage[::10],list_mass_flow_3[::10])
plt.plot(time_storage[::10],list_mass_flow_4[::10])
plt.plot(time_storage[::10],list_mass_flow_5[::10])
plt.plot(time_storage[::10],list_mass_flow_8[::10])
plt.plot(time_storage[::10],list_mass_flow_9[::10])
plt.plot(time_storage[::10],list_mass_flow_10[::10])

plt.title(f'massflow evolution Tank-Pipe-Pipe-Dome-Injectors-Combustor \n Propane Line with T3 = {T3}K  \n')
plt.xlabel(r'$time$ (s)')
plt.legend(['tank','pipe','pipe','dome','injector','combustor out'])
plt.ylabel(r'$mass flow$ (kg/s)')
plt.ylim(0,5)


print(f'Drop of pressure between injection and combustor is equal to : {int((1 - P7/P6)*100)} %')


# =============================================================================
# Fast Fourier Transformation for frequencies analysis 
# =============================================================================

from numpy.fft import fft, fftfreq
# Calcul FFT
x=list_pressure_1
N= len(x)
X = fft(x)  # Transformée de fourier
freq = fftfreq(N, dt)  # Fréquences de la transformée de Fourier
# Calcul du nombre d'échantillon
N= len(x)
# On prend la valeur absolue de l'amplitude uniquement pour les fréquences positives et normalisation
X_abs = np.abs(X[:N//2])*2.0/N
# On garde uniquement les fréquences positives
freq_pos = freq[:N//2]

plt.figure()
plt.plot(freq_pos, X_abs, label="Amplitude absolue")
plt.xlim(0, 500)  # On réduit la plage des fréquences à la zone utile
plt.ylim(0,1e5)
plt.grid()
plt.xlabel(r"Fréquence (Hz)")
plt.ylabel(r"Amplitude $|X(f)|$")
plt.title("Transformée de Fourier")
plt.show()
