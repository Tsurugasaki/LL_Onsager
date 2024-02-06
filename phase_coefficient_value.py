import pandas as pd
import numpy as np
import time
from sympy import symbols

# 関数内で使用するためのシンボルを定義
a, b, c = symbols('a b c')  # この行を追加
# 関数内でlog10を使用するためのシンボルを定義
log_a, log_b = symbols('log_a log_b')

# 条件を満たす拡散係数を判断する関数
def suitable_coefficients_for_corona_formation(equation_of_v1_Ab, equation_of_v1_Ne, equation_of_v2_Ab, equation_of_v2_Anl, equation_of_v2_Ne, equation_of_v3_Anl, equation_of_v3_Ab, equation_of_v4_Anl):
    # 開始時間を記録
    start_time = time.time()
    
    # 結果を格納するリスト
    results = []

    # 各相互拡散係数の値を定義(LSiSi/LNaNa=a, LSiSi/LAlAl=b, LSiSi/LHH=c)
    a, b, c = symbols('a b c')

    c_value = 0  # cの値を定義

    # 条件を満たすa, bの値の組を探索
    for a_val in np.logspace(-1, 3, num=400):  # aの値を10^-1~10^3まで動かす
        for b_val in np.logspace(-1, 2, num=300):  # bの値を10^-1~10^2まで動かす
            # 各方程式にa, bの値を代入して計算
            coefficients = {
                'LSiSi/LNaNa': a_val,
                'LSiSi/LAlAl': b_val,
                'v1_Ab': equation_of_v1_Ab.subs({a: a_val, b: b_val, c: c_value}),
                'v1_Ne': equation_of_v1_Ne.subs({a: a_val, b: b_val, c: c_value}),
                'v2_Ab': equation_of_v2_Ab.subs({a: a_val, b: b_val, c: c_value}),
                'v2_Ne': equation_of_v2_Ne.subs({a: a_val, b: b_val, c: c_value}),
                'v2_Anl': equation_of_v2_Anl.subs({a: a_val, b: b_val, c: c_value}),
                'v3_Anl': equation_of_v3_Anl.subs({a: a_val, b: b_val, c: c_value}),
                'v3_Ab': equation_of_v3_Ab.subs({a: a_val, b: b_val, c: c_value}),
                'v4_Anl': equation_of_v4_Anl.subs({a: a_val, b: b_val, c: c_value}),
                }
            results.append(coefficients)

    # 終了時間を記録
    end_time = time.time()

    # 計算時間を表示
    print(f"計算時間: {end_time - start_time}秒")

    # 結果をDataFrameに変換
    df = pd.DataFrame(results)

    # 結果をCSVファイルに保存
    df.to_csv('coefficients_of_every_a_and_b.csv', index=False)

    if df.empty:
        print("条件を満たす組み合わせが見つかりませんでした。")

equation_of_v1_Ab = -(3*(1908736622310711861642435*a + 5110338757287776148217530*b + 596916622298961994014272*a*b - 195426112*a**2 + 5878125))/(90071992547409920*(76020961*a + 321341476*b + 83064996*a*b))
equation_of_v1_Ne = -(25904060782184847996959540*b - 6170671421863215226552735*a + 11395173146432521784071296*a*b + 2381007936*a**2 - 103312500)/(180143985094819840*(76020961*a + 321341476*b + 83064996*a*b))
equation_of_v2_Ab = (197720350987500000000*c - 27187311120112687500*b - 2725445733950671875*a + 3685423282464706397683539939204354850*a*b + 41168961853137494376982218882981000000*a*c + 74527435921797906376076812880316000000*b*c + 2679051933812160160691281091739699232*a*b**2 + 1447052691981226564554634703501560912*a**2*b - 93693944023947501696*a**3*b + 19385636841214001221993374092878600000*a**2*c - 3095318221746347520000*a**3*c + 9957078121490148645063059420516800000*b**2*c + 1150770498722507033956142219826624445*a**2 - 37240951707622476000*a**3 + 2900441293529289809033022644536664280*b**2 - 196525335706825556409987186861484032*a**2*b**2 + 35503154760355986406342889952808400000*a*b*c - 680119751612085850906499918407680000*a*b**2*c - 2397064994979550372429787861913600000*a**2*b*c)/(300209951160517263360*(76020961*a + 321341476*b + 83064996*a*b)*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v2_Ne = (63183140961865535437992610820*b - 26044735395181248493566761755*a + 31994648336529487254181373568*a*b + 7935899450688*a**2 - 344340562500)/(600419902321034526720*(76020961*a + 321341476*b + 83064996*a*b))
equation_of_v2_Anl = -(3620767850772348758649673280*a + 5041151810817147273698958180*b + 129533433202355680051200000000*c + 5000699643996736217950640448*a*b + 60994690704476662136832000000*a*c + 17306036331292133425152000000*b*c + 968438799768*a**2 - 40777171875)/(75052487790129315840*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v3_Ab = (3396621287400*b - 4502561399880*a + 31200557000000*c - 35822117760*a*b + 3393816000000*a*c - 963572273136*a**2 + 54275821875)/(150104975580258631680*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v3_Anl = -((19701*a + 11660*b + 55970)*(3396621287400*b - 4502561399880*a + 31200557000000*c - 35822117760*a*b + 3393816000000*a*c - 963572273136*a**2 + 54275821875))/(150104975580258631680*(9801*a + 12100*b + 40000*c + 37249)*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v4_Anl = (91119336*a + 518142985)/(150104975580258631680*(9801*a + 12100*b + 40000*c + 37249))

# 関数を呼び出し
suitable_coefficients_for_corona_formation(equation_of_v1_Ab, equation_of_v1_Ne, equation_of_v2_Ab, equation_of_v2_Anl, equation_of_v2_Ne, equation_of_v3_Anl, equation_of_v3_Ab, equation_of_v4_Anl)
