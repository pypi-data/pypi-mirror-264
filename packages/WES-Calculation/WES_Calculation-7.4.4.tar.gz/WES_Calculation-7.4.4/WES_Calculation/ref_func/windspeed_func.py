'''
Date         : 2023-01-24 11:31:55
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd

LastEditTime : 2024-03-17 23:52:04
LastEditors  : <BDFD>
Description  : 
FilePath     : f:\GitHub Project\bdfd\Section5.2-PyPi-WES_Calculation\WES_Calculation\ref_func\windspeed_func.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
import numpy as np
import math

# default value
gammap = 18
phi1u = 5
phi1l = 0.0
tol = 0.0001

# Functions


# a function of solving phi (phi^4-gammap*phi^3*z/L'=1), in which x=L'.
def ws_phi1fo(z, x):
    le = phi1l  # the upper end of phi range
    ue = phi1u  # the lower end of phi range
    mp = 0.5*(le+ue)  # the mid point between both ends
    while abs(mp**4-gammap*mp**3*z/x-1) > tol:
        if mp**4-gammap*mp**3*z/x-1 > 0:
            ue = mp
        else:
            le = mp
        mp = 0.5*(le+ue)
    return mp


# a function of solving phi (phi^4-gammap*phi^3*(z-z0)/L'=1), in which x=L'.
def ws_phi1f(z, x):
    aphi = 0.5  # an assumed phi1
    uphi = (3*aphi**4-2*gammap*aphi**3*z/x+1)/(4*aphi**3-3*gammap *
                                               aphi**2*z/x)  # an updated phi1 by the Newton-Raphson method
    while abs(uphi-aphi) > tol:
        aphi = uphi
        # an updated phi1 by the Newton-Raphson method
        uphi = (3*aphi**4-2*gammap*aphi**3*z/x+1) / \
            (4*aphi**3-3*gammap*aphi**2*z/x)
    return uphi


def ws_psi1f(x):  # the psi function in terms of phi (for KEYPS Model)
    y = 1-x-3*math.log(x)+2*math.log(0.5+0.5*x)+2 * \
        math.atan(x)-0.5*math.pi+math.log(0.5+0.5*x**2)
    return y


def ws_psi2f(x):  # the psi function in terms of phi (for B-D Model)
    y = math.log((1+x)**2*(1+x**2)/8)-2*math.atan(x)+0.5*math.pi
    return y


def ws_psi3f(x):  # the psi-h function (for B-D Model)
    y = 2*math.log((1+x)/2)
    return y


def ws_A(x):  # A function in the ABL resistance law
    if x <= 0:
        Af = 1.1+3.7241*math.log(1-0.02*x)
    else:
        Af = 1.1-6.364*math.log(1+0.02*x)
    return Af


def ws_B(x):  # B function in the ABL resistance law
    if x <= 0:
        Bf = 4.3-(4.3-0.23)*(1-math.exp(0.03*x))
    else:
        Bf = 4.3+0.7*x**0.5
    return Bf


def ws_att(u1, t1, t2):  # a function transforming widnspeeds between different averaging times (AT) by the CEM method
    # u1: windspeed (m/s) at AT t1 (min), u2: windspeed (m/s) at AT t2 (min)
    if 1/60 < t1 <= 60:
        if 1/60 < t2 <= 60:
            if t2 == 60:
                u2 = np.array(u1)/(1.277+0.296*math.tanh(0.9 *
                                                         math.log10(45/t1/60)))*(t1 != 60)+np.array(u1)*(t1 == 60)
            else:
                u2 = (1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)/(1.277+0.296*math.tanh(0.9*math.log10(
                    45/t1/60)))*(t1 != 60)+(1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)*(t1 == 60)
        if 60 < t2 < 600:
            u2 = (1.5334-0.15*math.log10(t2*60))*np.array(u1)/(1.277+0.296*math.tanh(0.9 *
                                                                                     math.log10(45/t1/60)))*(t1 != 60)+(1.5334-0.15*math.log10(t2*60))*np.array(u1)*(t1 == 60)
    if 60 < t1 < 600:
        if 1/60 < t2 <= 60:
            if t2 == 60:
                u2 = np.array(u1)/(1.5334-0.15*math.log10(t1*60))
            else:
                u2 = (1.277+0.296*math.tanh(0.9*math.log10(45/t2/60))) * \
                    np.array(u1)/(1.5334-0.15*math.log10(t1*60))
        if 60 < t2 < 600:
            Up1 = (1.5334-0.15*math.log10(t2*60)) * \
                np.array(u1)/(1.5334-0.15*math.log10(t1*60))
    return u2
