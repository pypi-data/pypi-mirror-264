'''
Date         : 2023-01-24 11:31:55
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd

LastEditTime : 2024-03-18 14:33:58
LastEditors  : <BDFD>
Description  : 
FilePath     : \WES_Calculation\ref_func\windwave_func.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
import numpy as np
import math

# Functions


def ww_att(u1, t1, t2):  # a function transforming widnspeeds between different averaging times (AT) by the CEM method
    # u1: windspeed (m/s) at AT t1 (min), u2: windspeed (m/s) at AT t2 (min)
    if 1/60 < t1 <= 60:
        if 1/60 < t2 <= 60:
            if t2 == 60:
                u2 = np.array(u1)/(1.277+0.296*math.tanh(0.9 *
                                                         math.log10(45/t1/60)))*(t1 != 60)+np.array(u1)*(t1 == 60)
            else:
                u2 = (1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)/(1.277+0.296*math.tanh(0.9*math.log10(
                    45/t1/60)))*(t1 != 60)+(1.277+0.296*math.tanh(0.9*math.log10(45/t2/60)))*np.array(u1)*(t1 == 60)
        if 60 < t2 <= 600:  # <=600! Check the windspeed routine!!
            u2 = (1.5334-0.15*math.log10(t2*60))*np.array(u1)/(1.277+0.296*math.tanh(0.9*math.log10(
                45/t1/60)))*(t1 != 60)+(1.5334-0.15*math.log10(t2*60))*np.array(u1)*(t1 == 60)
    if 60 < t1 <= 600:
        if 1/60 < t2 <= 60:
            if t2 == 60:
                u2 = np.array(u1)/(1.5334-0.15*math.log10(t1*60))
            else:
                u2 = (1.277+0.296*math.tanh(0.9*math.log10(45/t2/60))) * \
                    np.array(u1)/(1.5334-0.15*math.log10(t1*60))
        if 60 < t2 <= 600:  # <=600! Check the windspeed routine!!
            # Up1=(1.5334-0.15*math.log10(t2*60))*np.array(u1)/(1.5334-0.15*math.log10(t1*60)) # wrong! Up1 should be u2. Check the windspeed routine!!
            u2 = (1.5334-0.15*math.log10(t2*60)) * \
                np.array(u1)/(1.5334-0.15*math.log10(t1*60))
    return u2
