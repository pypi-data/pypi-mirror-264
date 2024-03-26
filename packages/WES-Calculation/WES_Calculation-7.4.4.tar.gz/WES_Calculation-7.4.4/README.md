<!--
 * @Author: BDFD
 * @Date: 2021-10-27 18:39:19
 * @LastEditTime: 2022-04-26 11:42:56
 * @LastEditors: BDFD
 * @Description: In User Settings Edit
 * @FilePath: \5.2-PyPi-WES_Calculation\README.md
-->

# Package Name

Package function description

## Installation

`pip install WES-Calculation`

## Function and Requirements

`import WES_Calculation as wes`

## Currently Implement Three Function Include: GreenAmpt, Gumbel, Wave Function

### 01. GreenAmpt Function Usage

`wes.greenampt(thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3)`

```
常用测试数据用例
土体初始体积含水率(thetai)： 0.28
土体孔隙率(thetas)：0.4
土体吸力水头(psi)：0.22
土体渗透系数(k)：0.3
时间步长(dti)：5
总时间步长(nin)：12
是否需要生成净雨过程(iyesno)：1(是)
初期填洼量(dd): 2.5
降雨强度测试用例\*4
用例 1：降雨强度(i): 20, 20, 20, 50, 50, 50, 30, 30, 30, 20, 20, 20
用例 2：降雨强度(i): 0,0,0,0
用例 3：降雨强度(i): 10,25,0,2,0,5,15,30
用例 4：降雨强度(i): 10,0,15
```

Reference: test_01greenampt.py

### 02. Gumbel Function Usage

`wes.gumbel(result, unitt, unitx, i1, i2, i3)`

```
常用测试数据用例
样本数据单位(unitx)：Inch
时间间距(unitt)：year
样本数据(result)：1.55, 1.4, 1.35, 1.26, 1.2, 1.16, 1.1, 1.05, 1.01, 0.97, 0.88, 0.86, 0.82, 0.8, 0.75
概率分析的类型(i1)：最大值
概率空间是否截尾(i2)：否
估计办法(i3)：Gringorten
```

Reference: test_02gumbel.py

### 03. Wave Spectra Function Usage

`wes.wave(c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp)`

```
常用测试数据用例 1:
c1 = 1
水深 m(d):3.5
风矩 km(X):30
风速 m/s(U):10
风速位置距水面的高度 m(el):12
JONSWAP 谱中的峰形系数 γ(gamma)5:3.3
有效波高 H1/3m(Hs)6:2
平均周期 s(Tz):5
有效波周期 T1/3s(Ts):5.5
谱峰周期 s(Tp):0
```

```
常用测试数据用例 2:
c2 = 2
水深 m(d):0
风矩 km(X):370
风速 m/s(U):10
风速位置距水面的高度 m(el):12
JONSWAP 谱中的峰形系数 γ(gamma)5:3.3
有效波高 H1/3m(Hs)6:2
平均周期 s(Tz):5
有效波周期 T1/3s(Ts):5.5
谱峰周期 s(Tp):6
```

Reference: test_03wave.py

### 04. Wind Speed Function Usage

`wes.wind(o2, zw, Xlat, X, Rg, U, atm, Ta, zt, Tw, TaaC, wdu, zu)`

```
常用测试数据用例 1:
水域的大气表面层风速 o2 = 1
U的高度位置 zm(m) = 12
现场水域的地理纬度-Xlat = None
场地离岸的距离 X(km) = None
CEM中的 Rg = None
U的时距 U(m/s) = 21/11
U的时距 atm(min) = 3
现场水域已知气温 Ta = 20
改已知气温距水面的高度 zt(m) = 20
表面水温 Tw = 16
大气表面层的平均气温 Taac = 16/6.6667/0/None
所求风速的时距 wdu = 10
风速查看的高度范围 zu = 50
```

```
常用测试数据用例 2:
水域的大气表面层风速 o2 = 2
U的高度位置 zm(m) = 12
现场水域的地理纬度-Xlat = None
场地离岸的距离 X(km) = 25
CEM中的 Rg = None
U的时距 U(m/s) = 21/11
U的时距 atm(min) = 3
现场水域已知气温 Ta = 20
改已知气温距水面的高度 zt(m) = 20
表面水温 Tw = 16
大气表面层的平均气温 Taac = 16/6.6667/0/None
所求风速的时距 wdu = 10
风速查看的高度范围 zu = 50
```

```
常用测试数据用例 3:
水域的大气表面层风速 o2 = 3
U的高度位置 zm(m) = 12
现场水域的地理纬度-Xlat = 45
场地离岸的距离 X(km) = 25
CEM中的 Rg = None
U的时距 U(m/s) = 21/11
U的时距 atm(min) = 3
现场水域已知气温 Ta = 20
改已知气温距水面的高度 zt(m) = 20
表面水温 Tw = 16
大气表面层的平均气温 Taac = 16/6.6667/0/None
所求风速的时距 wdu = 10
风速查看的高度范围 zu = 50
```

```
常用测试数据用例 4:
水域的大气表面层风速 o2 = 4
U的高度位置 zm(m) = None
现场水域的地理纬度-Xlat = 45
场地离岸的距离 X(km) = None
CEM中的 Rg = 0.7
U的时距 U(m/s) = 21/11
U的时距 atm(min) = 3
现场水域已知气温 Ta = 20
改已知气温距水面的高度 zt(m) = 20
表面水温 Tw = 16
大气表面层的平均气温 Taac = 16/6.6667/0/None
所求风速的时距 wdu = 10
风速查看的高度范围 zu = 50
```

Reference: test_04wind.py

## License

copyright @ 2021 BDFD

This repository is licensed under the MIT license. See LICENSE for details.

### References

https://github.com/bdfd/5.2-PyPi-WES_Calculation

```

```

```

```
