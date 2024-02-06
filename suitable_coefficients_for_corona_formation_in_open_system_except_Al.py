import pandas as pd
import numpy as np
import time  # 追加

from sympy import symbols

# 関数内でlog10を使用するためのシンボルを定義
log_a, log_b = symbols('log_a log_b')

# 条件を満たす拡散係数か判断をするテスト関数
def suitable_coefficients_for_corona_formation(equation_of_v1_Ab, equation_of_v1_Ne, equation_of_v2_Ab, equation_of_v2_Anl, equation_of_v2_Ne, equation_of_v3_Anl, equation_of_v3_Ab, equation_of_v4_Anl):
    # 開始時間を記録
    start_time = time.time()
    
    # 結果を格納
    results = []

    # 各相互拡散係数の値を定義(LSiSi/LNaNa=a, LSiSi/LAlAl=b, LSiSi/LHH=c)
    a, b, c = symbols('a b c')

    c_value = 0 # cの値を定義

    # log10 a, log10 b の値を格納するリスト
    log_a_values = []
    log_b_values = []
    
    #  条件を満たすa, bの値の組をリストに追加
    for a_val in [10**(((i-1)/100)-1) for i in range(1, 402)]: # aの値を10^-1~10^3まで動かす
        for b_val in [10**(((i-1)/100)-1) for i in range(1, 302)]: # bの値を10^-1~10^2まで動かす
            coefficient_of_v1_Ab = equation_of_v1_Ab.subs({a: a_val, b: b_val})
            coefficient_of_v1_Ne = equation_of_v1_Ne.subs({a: a_val, b: b_val})
            coefficient_of_v2_Ab = equation_of_v2_Ab.subs({a: a_val, b: b_val, c: c_value})
            coefficient_of_v2_Anl = equation_of_v2_Anl.subs({a: a_val, b: b_val, c: c_value})
            coefficient_of_v2_Ne = equation_of_v2_Ne.subs({a: a_val, b: b_val})
            coefficient_of_v3_Anl = equation_of_v3_Anl.subs({a: a_val, b: b_val, c: c_value})
            coefficient_of_v3_Ab = equation_of_v3_Ab.subs({a: a_val, b: b_val, c: c_value})
            coefficient_of_v4_Anl = equation_of_v4_Anl.subs({a: a_val, b: b_val, c: c_value})
            if (coefficient_of_v1_Ab<0 
                and coefficient_of_v2_Ab<0 
                and coefficient_of_v1_Ne<0 
                and coefficient_of_v2_Ne>0
                and coefficient_of_v2_Anl<0 
                and coefficient_of_v3_Anl>0 
                and coefficient_of_v3_Ab<0 
                and coefficient_of_v4_Anl<0):
                results_dict = {'LSiSi/LNaNa':a, 'LSiSi/LNaNa':b, 'LSiSi/LHH':c}
                results.append(results_dict)
                # log10 a, log10 b の値を計算し、リストに追加
                log_a_val = np.log10(a_val)
                log_b_val = np.log10(b_val)
                log_a_values.append(log_a_val)
                log_b_values.append(log_b_val)

    # 終了時間を記録
    end_time = time.time()

    # 計算時間を表示
    elapsed_time = end_time - start_time
    print(f"計算時間: {elapsed_time}秒")

    if not results:
        print("条件を満たす組み合わせが見つかりませんでした。")
    else:
        # 結果をDataFrameに変換
        df = pd.DataFrame(results)

        # log10 a, log10 b の値をDataFrameに追加
        df['log_a'] = log_a_values
        df['log_b'] = log_b_values

        # 結果をCSVファイルに保存
        df.to_csv('solutions_of_stable_Ne_Anl_layer_and_LHH=0_many_value_with_logs.csv', index=False)

# 相係数の定義
a, b, c = symbols('a b c')
equation_of_v1_Ab = -(3*(1908736622310711861642435*a + 5110338757287776148217530*b + 596916622298961994014272*a*b - 195426112*a**2 + 5878125))/(90071992547409920*(76020961*a + 321341476*b + 83064996*a*b))
equation_of_v1_Ne = -(25904060782184847996959540*b - 6170671421863215226552735*a + 11395173146432521784071296*a*b + 2381007936*a**2 - 103312500)/(180143985094819840*(76020961*a + 321341476*b + 83064996*a*b))
equation_of_v2_Ab = (197720350987500000000*c - 27187311120112687500*b - 2725445733950671875*a + 3685423282464706397683539939204354850*a*b + 41168961853137494376982218882981000000*a*c + 74527435921797906376076812880316000000*b*c + 2679051933812160160691281091739699232*a*b**2 + 1447052691981226564554634703501560912*a**2*b - 93693944023947501696*a**3*b + 19385636841214001221993374092878600000*a**2*c - 3095318221746347520000*a**3*c + 9957078121490148645063059420516800000*b**2*c + 1150770498722507033956142219826624445*a**2 - 37240951707622476000*a**3 + 2900441293529289809033022644536664280*b**2 - 196525335706825556409987186861484032*a**2*b**2 + 35503154760355986406342889952808400000*a*b*c - 680119751612085850906499918407680000*a*b**2*c - 2397064994979550372429787861913600000*a**2*b*c)/(300209951160517263360*(76020961*a + 321341476*b + 83064996*a*b)*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v2_Ne = (63183140961865535437992610820*b - 26044735395181248493566761755*a + 31994648336529487254181373568*a*b + 7935899450688*a**2 - 344340562500)/(600419902321034526720*(76020961*a + 321341476*b + 83064996*a*b))
equation_of_v2_Anl = -(3620767850772348758649673280*a + 5041151810817147273698958180*b + 129533433202355680051200000000*c + 5000699643996736217950640448*a*b + 60994690704476662136832000000*a*c + 17306036331292133425152000000*b*c + 968438799768*a**2 - 40777171875)/(75052487790129315840*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v3_Ab = (3396621287400*b - 4502561399880*a + 31200557000000*c - 35822117760*a*b + 3393816000000*a*c - 963572273136*a**2 + 54275821875)/(150104975580258631680*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v3_Anl = (205572492754867008957410742562329*a + 286216125091901038814544555936684*b + 7354382234924052240305105894000000*c + 545234133394342455748179192815480*a*b + 7197380335810807220476086561240000*a*c + 5131843708137237006032418996640000*b*c + 160184816954450887547398446909440*a*b**2 + 144166335259005810357725545200576*a**2*b + 1758430150804451287527115688640000*a**2*c + 554355282117982862888177945600000*b**2*c + 104383960051694144116915952922744*a**2 + 18983337353052336*a**3 + 161480600224561391002861657011360*b**2 + 2452731032577797153014893040640000*a*b*c - 3037817750343750)/(150104975580258631680*(9801*a + 12100*b + 40000*c + 37249)*(94031809*a + 130919364*b + 3364000000*c + 129868816*a*b + 1584040000*a*c + 449440000*b*c))
equation_of_v4_Anl = -(1110092012073212298964680*a + 1233435568970235988982240*b + 2186201615613570821512271)/(150104975580258631680*(9801*a + 12100*b + 40000*c + 37249))

# 条件を満たす拡散係数の取得
results = suitable_coefficients_for_corona_formation(equation_of_v1_Ab, equation_of_v1_Ne, equation_of_v2_Ab, equation_of_v2_Anl, equation_of_v2_Ne, equation_of_v3_Anl, equation_of_v3_Ab, equation_of_v4_Anl)

# 結果をDataFrameに変換
df = pd.DataFrame(results)

# 結果をCSVファイルに保存
df.to_csv('solutions_of_LHH=0.csv', index=False)