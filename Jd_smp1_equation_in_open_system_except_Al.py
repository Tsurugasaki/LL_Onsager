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

print('v_Ab:', v_Ab)
print('v_Meta_Na:', v_Meta_Na)
print('v_Meta_Si:', v_Meta_Si)
print('v_Meta_H:', v_Meta_H)

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

 # 結果を格納するリスト
results = []

c_value = 0  # cの値を定義

# 開始時間を記録
start_time = time.time()

# 条件を満たすa, bの値の組を探索
for a_val in np.logspace(1, 7, num=300):  # aの値を10^-1~10^7まで動かす
    for b_val in np.logspace(0.5, 6.5, num=250):  # bの値を10^-1~10^5まで動かす
        # 各方程式にa, bの値を代入して計算
        coefficients = {
            'LSiSi/LNaNa': a_val,
            'LSiSi/LAlAl': b_val,
            'v1_Ab': v1_Ab.subs({a: a_val, b: b_val, c: c_value}),
            'v1_Ne': v1_Ne.subs({a: a_val, b: b_val, c: c_value}),
            'v2_Ab': v2_Ab.subs({a: a_val, b: b_val, c: c_value}),
            'v2_Ne': v2_Ne.subs({a: a_val, b: b_val, c: c_value}),
            'v2_Anl': v2_Anl.subs({a: a_val, b: b_val, c: c_value}),
            'v3_Anl': v3_Anl.subs({a: a_val, b: b_val, c: c_value}),
            'v3_Ab': v3_Ab.subs({a: a_val, b: b_val, c: c_value}),
            'v4_Anl': v4_Anl.subs({a: a_val, b: b_val, c: c_value}),
            }
        results.append(coefficients)

# 結果をDataFrameに変換
df = pd.DataFrame(results)

# 結果をCSVファイルに保存
df.to_csv('coefficients_of_every_a_and_b_ver2-3.csv', index=False)

# 終了時間を記録
end_time = time.time()

if df.empty:
    print("条件を満たす組み合わせが見つかりませんでした。")

# 計算時間を表示
print(f"計算時間: {end_time - start_time}秒")
