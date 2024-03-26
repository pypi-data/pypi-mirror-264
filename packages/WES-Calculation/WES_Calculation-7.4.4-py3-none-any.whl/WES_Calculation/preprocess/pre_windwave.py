'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2024-03-25 11:07:00
LastEditors  : <BDFD>
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_windwave.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata.format import convint as s2int, convfloat as s2dec
from ..windwave import windwave

# def windwave_calculation():


def pre_windwave(original_input):
    """
        function name:Waterfront Engineering Studio Windspeed
        input function:wes.windwave(o1, ad, X, U10k, atm, atr, wdu, o2, beta, slc, o5, o4, xs, d0, Ksb, xlook)
        Keyword arguments: 
            o1 水域, ad 水域平均水深, X 风距, 
            U10k 已知风速U10, atm U10的时距, 
            atr 风速的时距, wdu 计算风时, 
            o2风壅增水, beta 风向入射角, slc 堤防距静水高, 
            o5风壅增水为零, o4 水域底坡特点, 
            xs 水深剖面水深点的位置 , d0 水深剖面的水深, 
            Ksb 综合摩阻系数, xlook 查看风壅增水的位置
        argument -- description
        Return Description: heading, section1, section2, section2_note, section3, section4, section5, section6, section7, ending
    """
    # print("original_input before process",original_input)
    function_input = ({"o1": None, "ad": None, "X": None, "U10k": None,
                       "atm": None, "atr": None, "wdu": None, "o2": None,
                       "beta": None, "slc": None, "o4": None, "o5": None,
                       "xs": None, "d0": None, "Ksb": None, "xlook": None,
                       "o6": None})

    o1 = original_input["o1"]
    o1 = s2int(o1)
    ad = original_input["ad"]
    if ad == "None":
        ad = None
        function_input.update({"ad": ad})
    else:
        ad = s2dec(ad)
        function_input.update({"ad": ad})
    X = original_input["X"]
    X = s2dec(X)
    U10k = original_input["U10k"]
    U10k = s2dec(U10k)
    atm = original_input["atm"]
    atm = s2dec(atm)
    atr = original_input["atr"]
    atr = s2dec(atr)
    wdu = original_input["wdu"]
    wdu = s2dec(wdu)
    function_input.update({"o1": o1, "X": X, "U10k": U10k,
                           "atm": atm, "atr": atr, "wdu": wdu})

    o2 = original_input["o2"]
    if o2 == '1':
        o2 = 'Yes'
        function_input.update({"o2": o2})
    else:
        o2 = 'No'
        function_input.update({"o2": o2})
    if o2 == 'Yes':
        # the angle of incidence (from the shoreline normal). 0 means that the incident wave is pertenticular to the shoreline.
        beta = original_input["beta"]
        beta = s2dec(beta)
        # height of shore land crest from still water level (m)
        slc = original_input["slc"]
        slc = s2dec(slc)
        function_input.update({"beta": beta, "slc": slc})

        if o1 == 1:
            # is a depth profile available until the zero-setup location (such as shelf edge)? Yes or No
            o5 = original_input["o5"]
            if o5 == '1':
                o5 = 'Yes'
                function_input.update({"o5": o5})
            else:
                o5 = 'No'
                function_input.update({"o5": o5})
            function_input.update({"o5": o5})
            if o5 == 'Yes':
                # type os bed profile, 1 for a cosntant slope, and 2 for the other
                o4 = original_input["o4"]
                if o4 == '1':
                    o4 = 1
                    function_input.update({"o4": o4})
                else:
                    o4 = 2
                    function_input.update({"o4": o4})
                xs = original_input["xs"]  # location of shelf edge(m)
                # print('xs type is,',type(xs))
                res = xs.split(",")
                xs = list(map(float, res))
                # print(xs)
                d0 = original_input["d0"]  # water depth at the shelf
                # print('d0 type is,',type(d0))
                res_2 = d0.split(",")
                d0 = list(map(float, res_2))
                # print(res_2)
                # print(type(res_2))
                # xs=[2750,4590,22930,45860,48150,82550,100890,107710,121530,144460,181150,190320]# distance to shore (m)
                # d0=[7.31,10.05,13.72,14.62,20.12,23.97,25.60,27.43,36.57,54.86,73.15,91.43]# original water depth (m)
                xlook = original_input["xlook"]  # where to loot up wind setup
                xlook = s2dec(xlook)
                function_input.update({"xs": xs, "d0": d0, "xlook": xlook})
                # combined surface and bottom stress coefficient, 仅用于滨水工的计算。（两个规范中有自己的取值） Input a value or 'None'.
                Ksb = original_input["Ksb"]
                if Ksb == "None":
                    Ksb = 3.6/1000000
                    function_input.update({"Ksb": Ksb})
                else:
                    Ksb = s2dec(Ksb)
                    function_input.update({"Ksb": Ksb})
                if o4 == 1:
                    if len(xs) != 1 or len(d0) != 1:
                        # print('test2')
                        o6 = 0  # not able to proceed
                        function_input.update({"o6": o6})
                    else:
                        # print('test2')
                        o6 = 1  # able to proceed
                        function_input.update({"o6": o6})
                else:
                    if len(xs) < 1 or len(d0) < 1 or len(xs) != len(d0):
                        # print('test3')
                        o6 = 0  # not able to proceed
                        function_input.update({"o6": o6})
                    else:
                        # print('test4')
                        o6 = 1  # able to proceed
                        xs.insert(0, 0)
                        d0.insert(0, 0)
                        function_input.update({"xs": xs, "d0": d0, "o6": o6})
    print("function input is:", function_input)
    result = windwave(function_input["o1"], function_input["ad"], function_input["X"], function_input["U10k"],
                      function_input["atm"], function_input["atr"], function_input["wdu"], function_input["o2"],
                      function_input["beta"], function_input["slc"], function_input["o4"], function_input["o5"],
                      function_input["xs"], function_input["d0"], function_input["Ksb"], function_input["xlook"],
                      function_input["o6"])
    heading = result[0]
    # print(heading)
    # print(" ")
    section1 = result[1]
    # print(section1)
    # print(" ")
    section2 = result[2]
    print(section2)
    section3 = result[3]
    # print(section3)
    # print(" ")
    section4 = result[4]
    # print(section4)
    # print(" ")
    section5 = result[5]
    # print(section5)
    # print(" ")
    section6 = result[6]
    # print(section6)
    # print(" ")
    section7 = result[7]
    # print(section7)
    # print(" ")
    section8_heading = result[8]
    section8 = result[9]
    # print(section8)
    # print(" ")
    ending = result[10]
    # print(ending)
    # print(" ")
    return heading, section1, section2, section3, section4, section5, section6, section7, section8_heading, section8,  ending
