import pandas as pd
import numpy as np
import time
import sympy
from sympy import symbols
sympy.init_printing()
# 化学式中の各成分の係数(式量？)の定義
# Jadeite
n_Jd_Na = 0.973
n_Jd_Al = 1.00
n_Jd_Si = 1.99
n_Jd_H = 0

# Albite
n_Ab_Na = 1.99
n_Ab_Al = 1.06
n_Ab_Si = 2.90
n_Ab_H = 0

# Nepheline
n_Ne_Na = 0.98
n_Ne_Al = 0.98
n_Ne_Si = 0.99
n_Ne_H = 0

# Analcime
n_Anl_Na = 0.99
n_Anl_Al = 1.10
n_Anl_Si = 1.93
n_Anl_H = 2

# n_H2O
n_H2O_H = 2
n_H2O_Na = 0
n_H2O_Si = 0
n_H2O_Sl =0

# Met1 開放系を扱うときは閉鎖しない成分を抜いてください。
n_Met1_Al = 0

# 相係数比
p_Ab = 1
p_Anl = 5.05
p_Ne = 0.422

# mass-balance 解はv_Ab, v_Meta_Na, v_Meta_Si, v_Meta_H が出力されます。
A = sympy.Matrix([
    [n_Ab_Al+n_Anl_Al*p_Anl+n_Ne_Al*p_Ne, 0, 0, 0],
    [n_Ab_Na+p_Anl*n_Anl_Na+p_Ne*n_Ne_Na, 1, 0, 0],
    [n_Ab_Si+p_Anl*n_Anl_Si+p_Ne*n_Ne_Si, 0, 1, 0,],
    [n_Ab_H+p_Anl*n_Anl_H+p_Ne*n_Ne_H, 0, 0, 1]
    ])

B = sympy.cancel(A**(-1))

C = sympy.Matrix([
    [-n_Jd_Al],
    [-n_Jd_Na],
    [-n_Jd_Si],
    [0]
])
# A^-1*AX=A^-1*B
result1 = sympy.cancel(B*C)

# 各行の数値を個別に取り出して変数に格納
v_Ab = result1[0, 0]
v_Meta_Na = result1[1, 0]
v_Meta_Si = result1[2, 0]
v_Meta_H = result1[3, 0]

# MetaをMet1に変換
n_Met1_Na = v_Meta_Na
n_Met1_Si = v_Meta_Si
n_Met1_H = v_Meta_H

# 相互拡散係数の定義(a=LSiSi/LNaNa, b=LSiSI/LAlAl, c=LSiSi/LHH)
a, b, c = symbols('a b c')

# A-coefficientの定義
# A_Ab系
A_AbAb = (n_Ab_Na)**2 * a + (n_Ab_Al)**2 * b + (n_Ab_Si)**2
A_AbNe = (n_Ab_Na) * (n_Ne_Na) * a + (n_Ab_Al) * (n_Ne_Al) * b + (n_Ab_Si) * (n_Ne_Si)
A_AbJd = (n_Ab_Na) * (n_Jd_Na) * a + (n_Ab_Al) * (n_Jd_Al) * b + (n_Ab_Si) * (n_Jd_Si)
A_AbMet1 = (n_Ab_Na) * (n_Met1_Na) * a + (n_Ab_Al) * (n_Met1_Al) * b + (n_Ab_Si) * (n_Met1_Si) + (n_Ab_H) * (n_Met1_H) * c
A_AbAnl = (n_Ab_Na) * (n_Anl_Na) * a + (n_Ab_Al) * (n_Anl_Al) * b + (n_Ab_Si) * (n_Anl_Si) + (n_Ab_H) * (n_Anl_H) * c

# A_Ne系
A_NeAb = (n_Ab_Na) * (n_Ne_Na) * a + (n_Ab_Al) * (n_Ne_Al) * b + (n_Ab_Si) * (n_Ne_Si)
A_NeNe = (n_Ne_Na)**2 * a + (n_Ne_Al)**2 * b + (n_Ne_Si)**2
A_NeJd = (n_Ne_Na) * (n_Jd_Na) * a + (n_Ne_Al) * (n_Jd_Al) * b + (n_Ne_Si) * (n_Jd_Si)
A_NeMet1 = (n_Ne_Na) * (n_Met1_Na) * a + (n_Ne_Al) * (n_Met1_Al) * b + (n_Ne_Si) * (n_Met1_Si) + (n_Ne_H) * (n_Met1_H) * c
A_NeAnl = (n_Ne_Na) * (n_Anl_Na) * a + (n_Ne_Al) * (n_Anl_Al) * b + (n_Ne_Si) * (n_Anl_Si) + (n_Ne_H) * (n_Anl_H) * c

# A_Anl系
A_AnlAb = (n_Anl_Na) * (n_Ab_Na) * a + (n_Anl_Al) * (n_Ab_Al) * b + (n_Anl_Si) * (n_Ab_Si)
A_AnlNe = (n_Anl_Na) * (n_Ne_Na) * a + (n_Anl_Al) * (n_Ne_Al) * b + (n_Anl_Si) * (n_Ne_Si)
A_AnlAnl = (n_Anl_Na)**2 * a + (n_Anl_Al)**2 * b + (n_Anl_Si)**2 + (n_Anl_H)**2 * c
A_AnlJd = (n_Anl_Na) * (n_Jd_Na) * a + (n_Anl_Al) * (n_Jd_Al) * b + (n_Anl_Si) * (n_Jd_Si)
A_AnlMet1 = (n_Anl_Na) * (n_Met1_Na) * a + (n_Anl_Al) * (n_Met1_Al) * b + (n_Anl_Si) * (n_Met1_Si) + (n_Anl_H) * (n_Met1_H) * c

# 連立方程式(解はv_1_Ab, v_1_Ne, v_2_Ab, v_2_Ne, v_2_Anl, v_3_Ab, v_3_Anl, v_4_Anl)
D = sympy.Matrix([
    [A_AbAb, A_AbNe, 0, 0, 0, 0, 0, 0],
    [A_NeAb, A_NeNe, 0, 0, 0, 0, 0, 0],
    [A_AbAb, 0, A_AbAb, 0, A_AbAnl, 0, 0, 0],
    [A_AnlAb, 0, A_AnlAb, 0, A_AnlAnl, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, A_AnlAnl, 0, A_AnlAnl, 0],
    [1, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1 ]
])

E = sympy.cancel(D**(-1))

F = sympy.Matrix([
    [-A_AbMet1-A_AbJd],
    [-A_NeMet1-A_NeJd],
    [-A_AbMet1-A_AbJd-A_AbNe*p_Ne*v_Ab],
    [-A_AnlMet1-A_AnlJd-A_AnlNe*p_Ne*v_Ab],
    [p_Ne*v_Ab],
    [-A_AnlMet1-A_AnlJd-A_AnlNe*p_Ne*v_Ab-A_AnlAb*v_Ab],
    [v_Ab],
    [p_Anl*v_Ab]
])

# D^-1*DY=D^-1*F
result2 = sympy.cancel(E*F)

# 各行の数値を個別に取り出して変数に格納
v1_Ab = result2[0, 0]
v1_Ne = result2[1, 0]
v2_Ab = result2[2, 0]
v2_Ne = result2[3, 0]
v2_Anl = result2[4, 0]
v3_Ab = result2[5, 0]
v3_Anl = result2[6, 0]
v4_Anl = result2[7, 0]

# a, b, c の値を設定
a_val = 10**(3)
b_val = 10**(3)
c_value = 0

v1_Ab_value = v1_Ab.subs({a: a_val, b: b_val, c: c_value}).evalf()
v1_Ne_value = v1_Ne.subs({a: a_val, b: b_val, c: c_value}).evalf()
v2_Ab_value = v2_Ab.subs({a: a_val, b: b_val, c: c_value}).evalf()
v2_Ne_value = v2_Ne.subs({a: a_val, b: b_val, c: c_value}).evalf()
v2_Anl_value = v2_Anl.subs({a: a_val, b: b_val, c: c_value}).evalf()
v3_Anl_value = v3_Anl.subs({a: a_val, b: b_val, c: c_value}).evalf()
v3_Ab_value = v3_Ab.subs({a: a_val, b: b_val, c: c_value}).evalf()
v4_Anl_value = v4_Anl.subs({a: a_val, b: b_val, c: c_value}).evalf()

J1_Si = -(-(n_Jd_Si + v1_Ne_value*n_Ne_Si + v1_Ab_value*n_Ab_Si))
J1_Al = -(-(n_Jd_Al + v1_Ne_value*n_Ne_Al + v1_Ab_value*n_Ab_Al))
J1_Na = -(-(n_Jd_Na + v1_Ne_value*n_Ne_Na + v1_Ab_value*n_Ab_Na))
J1_H = -(-(n_Jd_H + v1_Ne_value*n_Ne_H + v1_Ab_value*n_Ab_H))
J2_Si = J1_Si - (-(v2_Ne_value*n_Ne_Si + v2_Ab_value*n_Ab_Si + v2_Anl_value*n_Anl_Si))
J2_Al = J1_Al- (-(v2_Ne_value*n_Ne_Al +  v2_Ab_value*n_Ab_Al + v2_Anl_value*n_Anl_Al))
J2_Na = J1_Na- (-(v2_Ne_value*n_Ne_Na + v2_Ab_value*n_Ab_Na + v2_Anl_value*n_Anl_Na))
J2_H = J1_H - (-(v2_Ne_value*n_Ne_H + v2_Ab_value*n_Ab_H + v2_Anl_value*n_Anl_H))
J3_Si = J2_Si - (-(v3_Ab_value*n_Ab_Si + v3_Anl_value*n_Anl_Si + n_Met1_Si))
J3_Al = J2_Al - (-(v3_Ab_value*n_Ab_Al + v3_Anl_value*n_Anl_Al))
J3_Na = J2_Na - (-(v3_Ab_value*n_Ab_Na + v3_Anl_value*n_Anl_Na + n_Met1_Na))
J3_H = J2_H - (-(v3_Ab_value*n_Ab_H + v3_Anl_value*n_Anl_H))
J4_Si = J3_Si - (-(v4_Anl_value*n_Anl_Si))
J4_Al = J3_Al - (-(v4_Anl_value*n_Anl_Al))
J4_Na = J3_Na - (-(v4_Anl_value*n_Anl_Na))
J4_H = J3_H - (-(v4_Anl_value*n_Anl_H+n_Met1_H))

print(f'v1_Ab: {v1_Ab_value}')
print(f'v1_Ne: {v1_Ne_value}')
print(f'v2_Ab: {v2_Ab_value}')
print(f'v2_Ne: {v2_Ne_value}')
print(f'v2_Anl: {v2_Anl_value}')
print(f'v3_Ab: {v3_Ab_value}')
print(f'v3_Anl: {v3_Anl_value}')
print(f'v4_Anl: {v4_Anl_value}')
print(f'J1_Si: {J1_Si}')
print(f'J1_Al: {J1_Al}')
print(f'J1_Na: {J1_Na}')
print(f'J1_H: {J1_H}')
print(f'J2_Si: {J2_Si}')
print(f'J2_Al: {J2_Al}')
print(f'J2_Na: {J2_Na}')
print(f'J2_H: {J2_H}')
print(f'J3_Si: {J3_Si}')
print(f'J3_Al: {J3_Al}')
print(f'J3_Na: {J3_Na}')
print(f'J3_H: {J3_H}')
print(f'J4_Si: {J4_Si}')
print(f'J4_Al: {J4_Al}')
print(f'J4_Na: {J4_Na}')
print(f'J4_H: {J4_H}')

LSiSi = 1
LAlAl = LSiSi/100
LNaNa = LSiSi/10**(1.5)
LHH = 10**3

dmu_dx_1_Si = -J1_Si/LSiSi
dmu_dx_1_Al = -J1_Al/LAlAl
dmu_dx_1_Na = -J1_Na/LNaNa
dmu_dx_1_H = -J1_H/LHH
dmu_dx_2_Si = -J2_Si/LSiSi
dmu_dx_2_Al = -J2_Al/LAlAl
dmu_dx_2_Na = -J2_Na/LNaNa
dmu_dx_2_H = -J2_H/LHH
dmu_dx_3_Si = -J3_Si/LSiSi
dmu_dx_3_Al = -J3_Al/LAlAl
dmu_dx_3_Na = -J3_Na/LNaNa
dmu_dx_3_H = -J3_H/LHH

print(f'v_Meta_Si: {v_Meta_Si}')
print(f'v_Meta_Na: {v_Meta_Na}')
print(f'v_Meta_H: {v_Meta_H}')
print(f'dmu_dx_1_Si: {dmu_dx_1_Si}')
print(f'dmu_dx_1_Si: {dmu_dx_1_Si}')
print(f'dmu_dx_1_Al: {dmu_dx_1_Al}')
print(f'dmu_dx_1_Na: {dmu_dx_1_Na}')
print(f'dmu_dx_1_H: {dmu_dx_1_H}')
print(f'dmu_dx_2_Si: {dmu_dx_2_Si}')
print(f'dmu_dx_2_Al: {dmu_dx_2_Al}')
print(f'dmu_dx_2_Na: {dmu_dx_2_Na}')
print(f'dmu_dx_2_H: {dmu_dx_2_H}')
print(f'dmu_dx_3_Si: {dmu_dx_3_Si}')
print(f'dmu_dx_3_Al: {dmu_dx_3_Al}')
print(f'dmu_dx_3_Na: {dmu_dx_3_Na}')
print(f'dmu_dx_3_H: {dmu_dx_3_H}')
