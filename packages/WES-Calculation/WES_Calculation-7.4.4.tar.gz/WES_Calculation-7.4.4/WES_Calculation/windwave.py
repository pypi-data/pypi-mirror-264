'''
Date         : 2022-12-18 12:32:53
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2024-03-21 11:48:06
LastEditors  : <BDFD>
Description  : 
FilePath     : \WES_Calculation\windwave.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''


# For the Wind Generate Wave Python Calculations
import numpy as np
import math
import matplotlib.pyplot as plt

from .ref_func import ww_att as att


def windwave(o1, ad, X, U10k, atm, atr, wdu, o2, beta, slc, o4, o5, xs, d0, Ksb, xlook, o6):
    # Secondary
    tol = 0.0001  # Iteration tolerance

    # legend_font = {'family' : 'Times New Roman'}
    plt.rc('legend', fontsize='small')  # medium

    heading = '---风浪要素和风壅增水的推算---'
    section1 = []
    # section1.extend(['---总说明---'])
    section1.extend(['风浪的定常状态即风距限制情况，风浪的过渡状态即风时限制情况。'])
    section1.extend(['tmin为风浪达到定常状态所需的最小风时，Fmin为过渡状态下按实际风时所得到的风距，d为水深。'])
    section1.extend(['在推算风壅增水时，均未计入波浪增水，也未考虑风时的作用。'])

    # 1. Duration adjustment for required averaging time
    section1.extend(
        ['计算风速为水面以上10 m处的风速(U\u2081\u2080)，其时距取决于实际需要，以及相关规范、标准、手册的要求。'])
    if atm != atr:
        U10a = att(U10k, atm, atr)  # The applied U10
        section1.extend(
            ['已知风速的时距并非指定时距(= ' + str(round(atr, 2)) + ' min)，该已知风速需要适当转换以获取指定时距的计算风速。'])
    else:
        U10a = U10k  # The applied U10

    # if wdu!=atr:
    section1.extend(
        ['在推算风浪要素时，除了SPM 1984以外，均采用指定时距的U\u2081\u2080作为计算风速。这实际上是假设该计算风速为整个风时内的平均风速。如果风时远大于该计算风速的时距，这个假设会比较保守。'])

    # 2. 滨水工的风壅增水推算
    section2 = []
    if o2 == 'Yes' and o1 == 1:
        # section2.extend(['---根据水深剖面逐段近似推算风壅增水的参考方法---'])
        if atm != atr:
            section2.extend(
                ['已知风速的时距并非所需时距，在此采用CEM (2015)中图II-2-1的近似转换方法获取所需时距的风速值作为计算风速，结果见以下CEM部分。'])
        else:
            section2.extend(['已知风速的时距等于所需时距，故已知风速即为计算风速。'])
        if o5 == 'Yes' and o6 == 1:
            if o4 == 1:
                # the initial estimate of the final wind setup
                ws0e = d0[0]*((2*Ksb*U10a**2*math.cos(math.pi *
                              beta/180)*xs[0]/9.81/d0[0]**2+1)**0.5-1)
                # initial estimate of the final wind setup
                ws0 = Ksb*U10a**2*xs[0]*math.log(d0[0]/ws0e)/9.81/(d0[0]-ws0e)
                while abs(ws0-ws0e) > tol:
                    ws0e = ws0
                    ws0 = Ksb*U10a**2*xs[0] * \
                        math.log(d0[0]/ws0e)/9.81/(d0[0]-ws0e)
                dlook = d0[0]*xlook/xs[0]
                wslook = ws0*(xs[0]-xlook)/xs[0]
                section2.extend(
                    ['由水深剖面得到的平均水深（静水位下，无风壅增水）= ' + str(round(d0[0]/2, 3)) + ' m。'])

            if o4 == 2:
                # average water depth for every segment
                d0m = [0 for k in range(len(xs))]
                dd = [0 for k in range(len(xs))]  # wind setup in every segment
                dx = [0 for k in range(len(xs))]

                ta = 0
                for i in range(1, len(xs)):
                    d0m[i] = 0.5*(d0[i]+d0[i-1])
                    dx[i] = xs[i]-xs[i-1]
                    ta = ta+dx[i]*d0m[i]
                # average water depth by bathymetry
                adb = ta/(xs[len(xs)-1]-xs[0])
                section2.extend(
                    ['由水深剖面得到的平均水深（静水位下，无风壅增水）= ' + str(round(adb, 3)) + ' m。'])

                ws0 = 0  # total wave setup
                for j in range(0, len(xs)-1):

                    if xlook == xs[len(xs)-j-1]:
                        dlook = d0[len(xs)-j-1]
                        wslook = ws0
                    if xs[len(xs)-j-2] < xlook < xs[len(xs)-j-1]:
                        dlook = d0[len(xs)-j-2]+(d0[len(xs)-j-1]-d0[len(xs)-j-2]
                                                 )*(xlook-xs[len(xs)-j-2])/dx[len(xs)-j-1]
                        wslook = ws0+0.5*(dlook+d0[len(xs)-j-1])*((2*Ksb*U10a**2*math.cos(math.pi*beta/180)*(
                            xs[len(xs)-j-1]-xlook)/9.81/(0.5*(dlook+d0[len(xs)-j-1]))**2+1)**0.5-1)

                    dd[len(xs)-j-1] = d0m[len(xs)-j-1]*((2*Ksb*U10a**2*math.cos(math.pi *
                                                                                beta/180)*dx[len(xs)-j-1]/9.81/d0m[len(xs)-j-1]**2+1)**0.5-1)
                    ws0 = ws0+dd[len(xs)-j-1]
                    d0m[len(xs)-j-2] = d0m[len(xs)-j-2]+ws0

                if xlook == 0:
                    dlook = 0
                    wslook = ws0

            if xlook > 0:
                section2.extend(['静水位接岸处的风壅增水= ' + str(round(ws0, 3)) + ' m。在距离静水位接岸处' + str(
                    round(xlook, 3)) + ' m的位置，风壅增水= ' + str(round(wslook, 3)) + ' m。'])
            else:
                section2.extend(['在距离静水位接岸处' + str(round(xlook, 3)) +
                                ' m的位置，风壅增水= ' + str(round(wslook, 3)) + ' m。'])

            if ws0 > slc:
                section2.extend(['警告：在该风壅增水作用下，理论上静水位接岸处的水面已超过堤防顶沿。'])
        else:
            section2.extend(['水深剖面数据缺乏或不恰当，无法近似推算风壅增水'])

    # 3. 港口与航道水文规范 (JTS 145-2015)
    section3 = []
    # section3.extend(['---港口与航道水文规范 (JTS 145-2015)---'])
    nn = 0  # order number of notes

    if atr != atm:
        section3.extend(['JTS 145-2015未提供不同时距风速之间的转换方法，故在此无法得以应用。'])
        Hs1 = None
        Ts1 = None
        ws1 = None

    else:
        section3.extend(['已知风速的时距等于所需时距，故已知风速即为计算风速。'])
        section3.extend(['所预报的波高为有效波高(Hs)，所预报的波周期为有效波周期(Ts)。'])

        if ad == None:
            dstate1 = '深水'
            section3.extend(
                ['假设平均水深满足第7.2.1条的判别标准：d/U\u2081\u2080\u00b2>0.2，水域属于深水。'])
        else:
            if ad/U10a**2 > 0.2:
                dstate1 = '深水'
                section3.extend(
                    ['按第7.2.1条的判别标准：d/U\u2081\u2080\u00b2= ' + str(round(ad/U10a**2, 3)) + ' >0.2，故水域属于深水。'])
            else:
                dstate1 = '浅水'
                section3.extend(
                    ['按第7.2.2条的判别标准：d/U\u2081\u2080\u00b2= ' + str(round(ad/U10a**2, 3)) + ' <=0.2，故水域属于浅水。'])
                section3.extend(
                    ['在浅水，原则上风浪状态按公式(7.2.2-3)判别。但该公式涉及到波长，而波长又涉及到波周期。而风浪状态未定的情况下，周期无法合理确定。参照邱大洪(1999)第167页一个算例的作法，在此风浪状态仍在深水条件下判别。'])

        Fmin1 = U10a**2*0.012*(9.81*wdu*60/U10a)**1.3 / \
            9.81  # threshold fetch (m)
        tmin1 = U10a*(9.81*X*1000/.012/U10a**2)**(1/1.3) / \
            9.81/60  # threshold time (min)

        Hsf = 0.0218*U10a**2  # for the fully developed condition
        # Tsf=U10a*(9.81*Hsf/.0135/U10a**2)**(2/3)/9.81
        # for the fully developed condition. Or, =U10a*0.55*34700**(0.35/1.5)/9.81? (Both have some difference in results.)
        Tsf = U10a*0.55*34700**0.233/9.81

        if 9.81*X*1000/U10a**2 >= 34700:  # 充分成长状态
            wstate1 = '充分成长'  # wstate: state of wind wave
            Hs1 = Hsf
            Ts1 = Tsf
            if dstate1 == '深水':
                section3.extend(['按第7.2.1条的判别标准：gF/U\u2081\u2080\u00b2= ' +
                                str(round(9.81*X*1000/U10a**2, 3)) + ' >=34700，故波浪达到充分成长状态。'])
                section3.extend(['在充分成长状态下，按公式(7.2.1-5)求得Hs= ' + str(round(Hsf, 3)) +
                                ' m，根据gF/U\u2081\u2080\u00b2=34700按公式(7.2.1-2)求得Ts= ' + str(round(Tsf, 2)) + ' s'])
        else:
            if X > Fmin1/1000:  # 过渡状态
                Hs1 = U10a**2*0.0055*(9.81*Fmin1/U10a**2)**.35/9.81
                Ts1 = U10a*0.55*(9.81*Fmin1/U10a**2)**.233/9.81
                wstate1 = '过渡'
                section3.extend(['由实际风时和计算风速，按公式(7.2.1-3)求得Fmin= ' + str(round(Fmin1/1000, 1)) +
                                ' km。实际风距>Fmin，故风浪处于过渡状态。由计算风速和Fmin可定义一个定常状态，以推算风浪要素。'])

                if dstate1 == '浅水':
                    section3.extend(
                        ['按公式(7.2.1-1)求得深水的Hs= ' + str(round(Hs1, 3)) + ' m，按公式(7.2.1-2)求得深水的Ts= ' + str(round(Ts1, 2)) + ' s'])
                    Kt = math.tanh(30*(9.81*ad/U10a**2)**0.8 /
                                   (9.81*Fmin1/U10a**2)**0.35)
                    Hs1 = Hs1*Kt
                    Ts1 = Ts1*Kt**(2/3)
                    section3.extend(
                        ['采用Fmin，求得公式(7.2.2-1)中的tanh项，即浅水中的波高折减系数Kt: ' + str(round(Kt, 2))])
                    section3.extend(
                        ['按公式(7.2.2-1)求得Hs= ' + str(round(Hs1, 3)) + ' m，按公式(7.2.2-2)求得Ts= ' + str(round(Ts1, 2)) + ' s'])
                else:
                    section3.extend(
                        ['按公式(7.2.1-1)求得Hs= ' + str(round(Hs1, 3)) + ' m，按公式(7.2.1-2)求得Ts= ' + str(round(Ts1, 2)) + ' s'])

            else:  # 定常状态
                Hs1 = min(U10a**2*0.0055*(9.81*X*1000/U10a**2)**.35/9.81, Hsf)
                Ts1 = min(U10a*0.55*(9.81*X*1000/U10a**2)**.233/9.81, Tsf)
                wstate1 = '定常'
                section3.extend(
                    ['由实际风时和计算风速，按公式(7.2.1-3)求得Fmin= ' + str(round(Fmin1/1000, 1)) + ' km。实际风距<=Fmin，故风浪处于定常状态。'])

                if dstate1 == '浅水':
                    section3.extend(['按公式(7.2.1-1)求得深水的Hs= ' + str(round(Hs1, 3)) +
                                    ' m，按公式(7.2.1-2)求得深水的Ts= ' + str(round(Ts1, 2)) + ' s'])
                    KF = math.tanh(30*(9.81*ad/U10a**2)**0.8 /
                                   (9.81*X*1000/U10a**2)**0.35)
                    Hs1 = Hs1*KF
                    Ts1 = Ts1*KF**(2/3)
                    section3.extend(
                        ['公式(7.2.2-1)中的tanh项即为浅水中的波高折减系数KF: ' + str(round(KF, 2))])
                    section3.extend(
                        ['按公式(7.2.2-1)求得Hs= ' + str(round(Hs1, 3)) + ' m，按公式(7.2.2-2)求得Ts= ' + str(round(Ts1, 2)) + ' s'])
                else:
                    section3.extend(
                        ['按公式(7.2.1-1)求得Hs= ' + str(round(Hs1, 3)) + ' m，按公式(7.2.1-2)求得Ts= ' + str(round(Ts1, 2)) + ' s'])

        if o1 != 1:
            section3.extend(
                ['按第7.2.7条，也可采用《堤防工程设计规范》(GB 50286-2013)中的方法预报平均波高(Ha)和平均波周期(Ta)，结果见下。'])

            if o2 == 'Yes':
                if ad != None:
                    ws1 = 0.5*3.6*U10a**2*X*1000 * \
                        math.cos(math.pi*beta/180)/9.81 / \
                        ad/1000000  # wind setup
                    if ws1 > slc:
                        section3.extend(
                            ['按第7.2.8条，静水位接岸处的风壅增水= ' + str(round(ws1, 3)) + ' m。（警告：在该风壅增水作用下，理论上水面已超过堤防顶沿。）'])
                    else:
                        section3.extend(
                            ['按第7.2.8条，静水位接岸处的风壅增水= ' + str(round(ws1, 3)) + ' m。'])
                else:
                    ws1 = None
                    section3.extend(['水域平均水深未知，故无法按第7.2.8条推算风壅增水。'])
            else:
                ws1 = None

        else:
            ws1 = None
            if o2 == 'Yes':
                section3.extend(['JTS 145-2015未提供推算开敞海域风壅增水的方法。'])

    # 3. 堤防工程设计规范 (GB 50286-2013)
    section4 = []
    # section4.extend(['---堤防工程设计规范 (GB 50286-2013)---'])

    if atr != atm:
        section4.extend(['GB 50286-2013未提供不同时距风速之间的转换方法，故在此无法得以应用。'])
        Ha4 = None
        Ta4 = None

    if atr != 10:
        section4.extend(
            ['GB 50286-2013采用10-min计算风速。由于缺乏10-min计算风速，GB 50286-2013在此无法得以应用。'])
        Ha4 = None
        Ta4 = None

    if ad == None:
        Ha4 = None
        Ta4 = None
        section4.extend(['由于水域的平均水深未知，GB 50286-2013在此无法得以应用。'])

    if atr == atm and ad != None and atr == 10:
        section4.extend(['已知风速的时距和计算风速的时距均为10 min，故已知风速即为计算风速。'])
        section4.extend(['所预报的波高为平均波高(Ha)，所预报的波周期为平均波周期(Ta)。'])

        Ha4 = U10a**2*0.13*math.tanh(0.7*(9.81*ad/U10a**2)**0.7)*math.tanh(0.0018*(
            9.81*X*1000/U10a**2)**0.45/.13/math.tanh(0.7*(9.81*ad/U10a**2)**0.7))/9.81
        Ta4 = U10a*13.9*(9.81*Ha4/U10a**2)**0.5/9.81

        tmin4 = 168*(9.81*Ta4/U10a)**3.45*U10a/9.81/60  # threshold time (min)

        if tmin4 <= wdu:  # a fetch-limited condition occurs
            wstate4 = '定常'
            section4.extend(['由计算风速和推算的Ta，按公式(C.1.2-3)求得tmin= ' +
                            str(round(tmin4/60, 2)) + ' h。实际风时>=tmin，故风浪处于定常状态。'])
            section4.extend(['按公式(C.1.2-1)求得Ha= ' + str(round(Ha4, 3)) +
                            ' m，按公式(C.1.2-2)求得Ta= ' + str(round(Ta4, 2)) + ' s'])

        else:  # a duration-limited condition occurs
            section4.extend(['由计算风速和推算的Ta，按公式(C.1.2-3)求得tmin= ' +
                            str(round(tmin4/60, 2)) + ' h。实际风时<tmin，故风浪处于过渡状态。'])
            wstate4 = '过渡'
            if X <= 100:
                section4.extend(
                    ['按第C.1.1中第4条及其条文说明，由于风距不大于100 km，可假设波浪达到定常状态。于是波浪要素按定常状态给出。'])
                section4.extend(['按公式(C.1.2-1)求得Ha= ' + str(round(Ha4, 3)) +
                                ' m，按公式(C.1.2-2)求得Ta= ' + str(round(Ta4, 2)) + ' s'])
            else:
                Ta4 = (wdu*60*9.81/U10a/168)**(1/3.45)*U10a / \
                    9.81  # /1000 # threshold fetch (m)
                Ha4 = (9.81*Ta4/13.9)**2/9.81
                section4.extend(['由实际风时和计算风速，按公式(C.1.2-3)求得Ta= ' + str(round(Ta4, 2)
                                                                       ) + ' s，按公式(C.1.2-2)求得Ha= ' + str(round(Ha4, 3)) + ' m'])

    if atr == 10:
        ws2 = ws1
    else:
        ws2 = None

    if o2 == 'Yes':
        if atr == atm and ad != None and atr == 10:
            section4.extend(
                ['GB 50286-2013推算风壅增水的方法（见第C.2节）同《港口与航道水文规范》(JTS 145-2015)，结果见上。'])

    # 4. 海堤工程设计规范 (GB/T 51015-2014)
    section5 = []
    # section5.extend(['---海堤工程设计规范 (GB/T 51015-2014)---'])

    if o1 == 1 or o1 == 2:
        section5.extend(
            ['该规范与《堤防工程设计规范》(GB 50286-2013)一样，采用莆田试验站方法推算风浪要素。但按第82页上的第4条，GB/T 51015-2014只考虑定常状态的波浪，不判断风浪的状态。'])

        if atr == atm and ad != None and atr == 10:
            if wstate4 == '定常' or X <= 100:
                Ha5 = Ha4
                Ta5 = Ta4
                section5.extend(['风浪要素推算结果见《堤防工程设计规范》部分。'])
            if wstate4 == '过渡' and X > 100:
                Ha5 = U10a**2*0.13*math.tanh(0.7*(9.81*ad/U10a**2)**0.7)*math.tanh(0.0018*(
                    9.81*X*1000/U10a**2)**0.45/.13/math.tanh(0.7*(9.81*ad/U10a**2)**0.7))/9.81
                Ta5 = U10a*13.9*(9.81*Ha5/U10a**2)**0.5/9.81
                section5.extend(['由实际风时和计算风速，按公式(C.0.4-1)求得Ta= ' + str(round(Ta5, 2)
                                                                       ) + ' s，按公式(C.0.4-2)求得Ha= ' + str(round(Ha5, 3)) + ' m'])

            Ts5 = 1.15*Ta5
            section5.extend(
                ['按公式(C.0.1-2)，Ts = 1.15Ta = ' + str(round(Ts5, 2)) + ' s'])
        else:
            Ha5 = None
            Ta5 = None
            section5.extend(['风浪要素推算结果见《堤防工程设计规范》部分。'])

        if o2 == 'Yes':
            section5.extend(['GB/T 51015-2014未提供推算风壅增水的方法。'])

    else:
        Ha5 = None
        Ta5 = None
        section5.extend(['由于水域为湖泊或水库，GB/T 51015-2014在此不适用。'])

    # 4. Shore Protection Manual (1984)
    section6 = []
    # section6.extend(['---Shore Protection Manual (SPM 1984)---'])

    if atm != atr:
        section6.extend(['按图3-13，1-h时距的U\u2081\u2080= ' + str((round(att(U10k, atm, 60), 3))) +
                        ' m/s，而' + str(round(atr, 1)) + '-min时距的U\u2081\u2080= ' + str(round(U10a, 3)) + ' m/s'])
    U10ae = U10a
    U10aae = 0.71*U10ae**1.23  # wind-stress factor
    tmin2e = atr  # estimated tmin (min)

    if ad == None or (ad != None and ad > 90):

        dstate2 = '深水'
        if ad == None:
            section6.extend(['假设水域为深水条件（按3-66页，平均水深>90 m）。'])
        if ad != None and ad > 90:
            section6.extend(['水域为深水条件（按3-66页，平均水深>90 m）。'])

        section6.extend(
            ['所预报的波高为由波频谱零阶原点矩所估计的有效波高(Hm0)，所预报的波周期为谱峰频率所对应的周期(Tp)。Hm0近似等于Hs，Ts近似等于0.95Tp。'])

        tmin2 = 68.8*(9.81*X*1000/U10aae**2)**(2/3) * \
            U10aae/9.81/60  # threshold time (min)

        while abs(tmin2e-tmin2) > tol:
            tmin2e = tmin2
            if tmin2e <= 1/60:
                U10ae = att(U10k, atm, 1/60)
            if 1/60 < tmin2e < 600:
                U10ae = att(U10k, atm, tmin2e)  # The applied U10
            if tmin2e >= 600:
                U10ae = att(U10k, atm, 600)  # The applied U10
            U10aae = 0.71*U10ae**1.23
            tmin2 = 68.8*(9.81*X*1000/U10aae**2)**(2/3) * \
                U10aae/9.81/60  # threshold time (min)
        U10aa = U10aae

        section6.extend(['由实际风距按公式(3-35)试算求得tmin= ' + str(round(tmin2/60, 2)) +
                        ' h，以此作为时距的U\u2081\u2080= ' + str(round(U10ae, 3)) + ' m/s'])  # （该风速即为计算风速）')

        if tmin2 > wdu:  # a duration-limited condition occurs

            # critical wind speed for the duration-limited condition
            U10ad = att(U10k, atm, wdu)
            U10aad = 0.71*U10ad**1.23
            # /1000 # threshold fetch (m)
            Fmin2 = (wdu*60*(9.81*U10aad)**(1/3)/68.8)**1.5

            # updated fetch to generate a fetch-limited condition (m)
            Xu = Fmin2/1000
            wstate2 = '过渡'
            section6.extend(['实际风时<tmin，故风浪处于过渡状态。'])
            section6.extend(['以实际风时作为时距的风速即为计算风速(= ' + str(round(U10ad, 3)) +
                            ' m/s)。按公式(3-28a)，根据计算风速求得风应力因子Ua= ' + str(round(U10aad, 3))])
            section6.extend(['根据实际风时和Ua按公式(3-35)求得Fmin(= ' + round(Fmin2 /
                            1000, 3) + ' km)。由Ua和Fmin可定义一个定常状态，可按公式(3-33)和(3-34)推算风浪要素。'])

            Hm02f = 0.2433*U10aad**2/9.81  # 充分成长状态下的波高
            Hm02 = 0.0016*U10aad**2*(9.81*Xu*1000/U10aad**2)**0.5/9.81
            if Hm02 > Hm02f:
                Hm02 = Hm02f
                section6.extend(
                    ['按公式(3-33)得到的Hm0大于按公式(3-33)得到的充分成长状态下的Hm0，最终结果取后者。'])

            Tm2f = 8.134*U10aad/9.81  # 充分成长状态下的波周期
            Tm2 = 0.2857*U10aad*(9.81*Xu*1000/U10aad**2)**(1/3)/9.81
            if Tm2 > Tm2f:
                Tm2 = Tm2f
                section6.extend(
                    ['按公式(3-34)得到的Tp大于按公式(3-37)得到的充分成长状态下的Tp，最终结果取后者。'])

        else:  # a fetch-limited condition occurs
            Xu = X
            wstate2 = '定常'
            section6.extend(['实际风时>=tmin，故风浪处于定常状态。'])
            section6.extend(['以tmin为时距的风速即为计算风速(= ' + str(round(U10ae, 3)) +
                            ' m/s)。按公式(3-28a)，根据计算风速求得风应力因子Ua= ' + str(round(U10aa, 3))])
            Hm02f = 0.2433*U10aa**2/9.81  # 充分成长状态下的波高
            Hm02 = 0.0016*U10aa**2*(9.81*Xu*1000/U10aa**2)**0.5/9.81
            if Hm02 > Hm02f:
                Hm02 = Hm02f
                section6.extend(
                    ['按公式(3-33)得到的Hm0大于按公式(3-33)得到的充分成长状态下的Hm0，最终结果取后者。'])
            else:
                section6.extend(
                    ['按公式(3-33)得到的Hm0= ' + str(round(Hm02, 3)) + ' m'])

            Tm2f = 8.134*U10aa/9.81  # 充分成长状态下的波周期
            Tm2 = 0.2857*U10aa*(9.81*Xu*1000/U10aa**2)**(1/3)/9.81
            if Tm2 > Tm2f:
                Tm2 = Tm2f
                section6.extend(
                    ['按公式(3-34)得到的Tp大于按公式(3-37)得到的充分成长状态下的Tp，最终结果取后者。'])
            else:
                section6.extend(
                    ['按公式(3-34)得到的Tp= ' + str(round(Tm2, 2)) + ' s'])

    if ad != None:
        if ad < 1.5:
            dstate2 = '浅水'
            tmin2 = None
            Fmin2 = None
            Hm02 = None
            Tm2 = None
            section6.extend(['平均水深太小(<1.5 m)，SPM 1984不再适用。'])
            # print(nn,'. 平均水深太小(<15 m)，SPM 1984不再适用。')
        if 1.5 <= ad <= 90:
            section6.extend(
                ['假设所预报的波高为由波频谱零阶原点矩所估计的有效波高(Hm0)，且所预报的波周期为谱峰频率所对应的周期(Tp)。Hm0近似等于Hs，Ts近似等于0.95Tp。'])
            Tm2 = U10aae*7.54*math.tanh(0.833*(9.81*ad/U10aae**2)**(3/8))*math.tanh(0.0379*(
                9.81*X*1000/U10aae**2)**(1/3)/math.tanh(0.833*(9.81*ad/U10aae**2)**(3/8)))/9.81
            tmin2 = U10aae*537*(9.81*Tm2/U10aae)**(7/3) / \
                9.81/60  # threshold time (min)
            while abs(tmin2e-tmin2) > tol:
                tmin2e = tmin2
                if tmin2e <= 1/60:
                    U10ae = att(U10k, atm, 1/60)
                if 1/60 < tmin2e < 600:
                    U10ae = att(U10k, atm, tmin2e)  # The applied U10
                if tmin2e >= 600:
                    U10ae = att(U10k, atm, 600)  # The applied U10
                U10aae = 0.71*U10ae**1.23
                Tm2 = U10aae*7.54*math.tanh(0.833*(9.81*ad/U10aae**2)**(3/8))*math.tanh(0.0379*(
                    9.81*X*1000/U10aae**2)**(1/3)/math.tanh(0.833*(9.81*ad/U10aae**2)**(3/8)))/9.81
                tmin2 = U10aae*537*(9.81*Tm2/U10aae)**(7/3) / \
                    9.81/60  # threshold time (min)
            U10aa = U10aae

            section6.extend(['由实际风距按公式(3-40)和(3-41)试算求得tmin= ' + str(round(tmin2/60, 2)) +
                            ' h，以此作为时距的U\u2081\u2080= ' + str(round(U10ae, 3)) + ' m/s'])  # （该风速即为计算风速）')

            if tmin2 > wdu:  # a duration-limited condition occurs
                # critical wind speed for the duration-limited condition
                U10ad = att(U10k, atm, wdu)
                U10aad = 0.71*U10ad**1.23
                U10aa = U10aad
                # ,U10aa*7.54*math.tanh(0.833*(9.81*ad/U10aa**2)**(3/8))/9.81) # actual T (s)
                Tm2lim = U10aa*(wdu*60*9.81/U10aad/537)**(3/7)/9.81

                Fl = 0
                Fr = X
                Fm = 0.5*(Fl+Fr)
                Tm2e = U10aad*7.54*math.tanh(0.833*(9.81*ad/U10aad**2)**(3/8))*math.tanh(0.0379*(
                    9.81*Fm*1000/U10aad**2)**(1/3)/math.tanh(0.833*(9.81*ad/U10aad**2)**(3/8)))/9.81
                while abs(Tm2e-Tm2lim) > tol:
                    if Tm2e >= Tm2lim:
                        Fr = Fm
                    else:
                        Fl = Fm
                    Fm = 0.5*(Fl+Fr)
                    Tm2e = U10aad*7.54*math.tanh(0.833*(9.81*ad/U10aad**2)**(3/8))*math.tanh(0.0379*(
                        9.81*Fm*1000/U10aad**2)**(1/3)/math.tanh(0.833*(9.81*ad/U10aad**2)**(3/8)))/9.81
                Fmin2 = Fm
                Xu = Fmin2
                wstate2 = '过渡'
                Tm2 = Tm2lim
                section6.extend(['实际风时<tmin，故风浪处于过渡状态。'])
                section6.extend(['以实际风时作为时距的U\u2081\u2080即为计算风速(= ' + str(
                    round(U10ad, 3)) + ' m/s)。按公式(3-28a)，根据计算风速求得风应力因子Ua= ' + str(round(U10aad, 3))])
                section6.extend(['由实际风时按公式(3-41)求得Tp= ' + str(round(Tm2, 2)) +
                                's，再结合公式(3-40)求得Fmin(= ' + str(round(Xu, 3)) + ' km)，最后按公式(3-39)求得Hm0。'])

            else:
                Xu = X
                Tm2 = U10aa*7.54*math.tanh(0.833*(9.81*ad/U10aa**2)**(3/8))*math.tanh(0.0379*(
                    9.81*Xu*1000/U10aa**2)**(1/3)/math.tanh(0.833*(9.81*ad/U10aa**2)**(3/8)))/9.81
                wstate2 = '定常'
                section6.extend(['实际风时>=tmin，故风浪处于定常状态。'])
                section6.extend(['以tmin为时距的U\u2081\u2080即为计算风速(= ' + str(round(U10ae, 3)) +
                                ' m/s)。按公式(3-28a)，根据计算风速求得风应力因子Ua= ' + str(round(U10aa, 3))])
                section6.extend(
                    ['由实际风距按公式(3-40)求得Tp= ' + str(round(Tm2, 2)) + ' s，最后按公式(3-39)求得Hm0。'])

            if ad/Tm2**2 > 0.78:
                dstate2 = '深水'
                section6.extend(['水深在[1.5 m,90 m]范围内。按图3-27至图3-36中的标准：d/Tp\u00b2= ' +
                                str(round(ad/Tm2**2, 2)) + ' >0.78。故水域仍属于深水。'])
            else:
                dstate2 = '浅水'
                section6.extend(['. 水深在[1.5 m,90 m]范围内。按图3-27至图3-36中的标准：d/Tp\u00b2= ' +
                                str(round(ad/Tm2**2, 2)) + ' <=0.78。故水域属于浅水。'])
            Hm02 = U10aa**2*0.283*math.tanh(0.53*(9.81*ad/U10aa**2)**0.75)*math.tanh(
                0.00565*(9.81*Xu*1000/U10aa**2)**0.5/math.tanh(0.53*(9.81*ad/U10aa**2)**0.75))/9.81

    if Tm2 != None:
        Ts2 = 0.95*Tm2  # Significant wave period
    else:
        Ts2 = None

    # 4. Coastal Engineering Manual  (CEM 2015)
    section7 = []
    # section7.extend(['---Coastal Engineering Manual (CEM 2015)---'])

    if atm != atr:
        section7.extend(['按图II-2-1，1-h时距的U\u2081\u2080= ' + str(round(att(U10k, atm, 60), 3)) +
                        ' m/s，而' + str(round(atr, 1)) + '-min时距的U\u2081\u2080= ' + str(round(U10a, 3)) + ' m/s（计算风速）'])

    section7.extend(
        ['所预报的波高为由波频谱零阶原点矩所估计的有效波高(Hm0)，所预报的波周期为谱峰频率所对应的周期(Tp)。Hm0近似等于Hs。'])

    # time required to reach the fetch-limited condition (min), by Eq.(II-2-35).
    tmin3 = 77.23*(1000*X)**0.67/9.81**0.33/U10a**0.34/60
    CD = (1.1+0.035*U10a)/1000  # by Eq.(II-2-36)
    Uf = CD**0.5*U10a  # by Eq.(II-2-36)
    section7.extend(['按第II-2-48页，风阻系数CD= ' + str(round(CD, 6)) +
                    '，摩擦风速U*= ' + str(round(Uf, 3)) + ' m/s'])

    Xfl = (wdu*60*9.81**0.33*U10a**0.34/77.23)**1.5 / \
        1000  # by Eq.(II-2-35), in km
    Hm0fl = Uf**2*0.0413*(9.81*X*1000/Uf**2)**0.5/9.81  # by Eq.(II-2-36)
    Tmfl = Uf*0.651*(9.81*X*1000/Uf**2)**(1/3)/9.81  # by Eq.(II-2-36)

    Hinf = 0.27*U10a**2/9.81  # by Eq.(II-2-30)
    XHinf = (9.81*Hinf/Uf**2/0.0413)**2*Uf**2 / \
        9.81/1000  # by Eq.(II-2-36), in km
    TmHinf = Uf*0.651*(9.81*XHinf*1000/Uf**2)**(1/3)/9.81  # by Eq.(II-2-36)
    section7.extend(['限制条件：按公式(II-2-30)，充分成长状态下的上限波高（定义不明）= ' + str(round(Hinf, 3)) +
                    ' m。按公式(II-2-36)，对应的风距= ' + str(round(XHinf, 3)) + ' km，Tp= ' + str(round(TmHinf, 2)) + ' s'])

    Hm0f = 211.5*Uf**2/9.81  # by Eq.(II-2-37)
    Tmf = 239.8*Uf/9.81  # by Eq.(II-2-37)
    section7.extend(['限制条件：按公式(II-2-37)，充分成长状态下的波浪要素：Hm0= ' +
                    str(round(Hm0f, 3)) + ' m，Tp= ' + str(round(Tmf, 2)) + ' s'])

    if ad != None:
        Tmad = 9.78*(ad/9.81)**0.5  # by Eq.(II-2-39)
        Hm0d = 0.5*ad  # On Page II-2-58
        section7.extend(
            ['限制条件：按公式(II-2-39)，水深限制下的最大Tp= ' + str(round(Tmad, 2)) + ' s'])
        section7.extend(
            ['限制条件：按第II-2-58页，水深限制下的最大Hm0 = 0.5d = ' + str(round(Hm0d, 2)) + ' m'])

    if wdu >= tmin3:
        wstate3 = '定常'
        Fa = X  # assumed fetch for the fetch-limited condition
        section7.extend(['由实际风距和计算风速，按公式(II-2-35)求得tmin= ' +
                        str(round(tmin3/60, 2)) + ' h。实际风时>=tmin，故风浪处于定常状态。'])

    else:
        wstate3 = '过渡'
        section7.extend(['由实际风距和计算风速，按公式(II-2-35)求得tmin= ' +
                        str(round(tmin3/60, 2)) + ' h。实际风时<tmin，故风浪处于过渡状态。'])
        if ad != None:
            Tmmin = min(TmHinf, Tmf, Tmad)
        else:
            Tmmin = min(TmHinf, Tmf)
        Fa = min(Xfl, (9.81*Tmmin/Uf/0.651)**3*Uf**2/9.81/1000)

        section7.extend(
            ['由实际风时和计算风速，按公式(II-2-35)求得Fmin= ' + str(round(Xfl, 3)) + ' km'])
        section7.extend(['各种限制条件的Tp中，最小值为' + str(round(Tmmin, 2)) + 's，按公式(II-2-35)求得对应的风距= ' +
                        str(round((9.81*Tmmin/Uf/0.651)**3*Uf**2/9.81/1000, 3)) + ' km'])
        section7.extend(['综上所述，Fmin最终取' + str(round(Fa, 3)) +
                        'km。由计算风速和Fmin可定义一个定常状态，按公式(II-2-36)推算Hm0和Tp。'])

    Hm03 = min(Uf**2*0.0413*(9.81*Fa*1000/Uf**2)**0.5/9.81, Hm0fl, Hinf, Hm0f)
    if ad != None:
        Tm3 = min(Uf*0.651*(9.81*Fa*1000/Uf**2)**(1/3)/9.81, Tmf, Tmad)
    else:
        Tm3 = min(Uf*0.651*(9.81*Fa*1000/Uf**2)**(1/3)/9.81, Tmf)
    section7.extend(['按公式(II-2-36)推算Hm0和Tp，并考虑各种限制条件施加的上限值，最终结果：Hm0= ' +
                    str(round(Hm03, 3)) + ' m，Tp= ' + str(round(Tm3, 2)) + ' s'])

    # More outputs
    section8 = []
    section8_heading = []
    # section8.extend(['---结果汇总---'])

    # table3 = "{0:^10}\t{1:^7}\t{2:^7}\t{3:^7}\t{4:^7}\t{5:^7}\t{6:^7}\t{7:^7}\t{8:^7}\t{9:^7}"
    section8_heading += (("推算方法", "tmin (h)", "Ha (m)", "Hs (m)",
                          'Ta (s)', 'Ts (s)', 'Tp (s)', '风浪状态', '水深条件', '风壅增水 (m)'),)
    if Hs1 != None:
        if ws1 == None:
            section8 += (('JTS 145-2015', str(round(tmin1/60, 2)), '',
                          str(round(Hs1, 3)), '', str(round(Ts1, 1)), '', str(wstate1), str(dstate1), ''),)
        else:
            section8 += (('JTS 145-2015', str(round(tmin1/60, 2)), '',
                          str(round(Hs1, 3)), '', str(round(Ts1, 1)), '', str(wstate1), str(dstate1), str(round(ws1, 3))),)
    else:
        section8 += (('JTS 145-2015', '', '', '', '', '', '', '', '', ''),)

    if Ha4 != None:
        if ws2 == None:
            section8 += (('GB 50286-2013', str(round(tmin4/60, 2)),
                          str(round(Ha4, 3)), '', str(round(Ta4, 1)), '', '', str(wstate4), '无定义', ''),)
        else:
            section8 += (('GB 50286-2013', str(round(tmin4/60, 2)), str(round(Ha4, 3)),
                         '', str(round(Ta4, 1)), '', '', str(wstate4), '无定义', str(round(ws2, 3))),)
    else:
        section8 += (('GB 50286-2013', '', '', '', '', '', '', '', '', ''),)

    if Ha5 != None:
        section8 += (('GB/T 51015-2014', '', str(round(Ha5, 3)), '',
                      str(round(Ta5, 1)), str(round(Ts5, 1)), '', '不判别', '无定义', ''),)
    else:
        section8 += (('GB/T 51015-2014', '', '', '', '', '', '', '', '', ''),)

    if Hm02 != None:
        section8 += (('SPM 1984', str(round(tmin2/60, 2)), '', str(round(Hm02, 3)),
                     '', str(round(Ts2, 1)), str(round(Tm2, 1)), str(wstate2), str(dstate2), ''),)
    else:
        section8 += (('SPM 1984', '', '', '', '', '', '', '', '', ''),)

    if Hm03 != None:
        section8 += (('CEM 2015', str(round(tmin3/60, 2)), '',
                      str(round(Hm03, 3)), '', '', str(round(Tm3, 1)), str(wstate3), '无定义', ''),)
    else:
        section8 += (('CEM 2015', '', '', '', '', '', '', '', '', ''),)

    ending = []
    ending.extend(['---结果展示结束---'])
    print("Finished Wind Generate Wave Function!")
    return heading, section1, section2, section3, section4, section5, section6, section7, section8_heading, section8, ending
