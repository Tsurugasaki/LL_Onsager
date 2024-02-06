import sympy as sp
import pandas as pd

# シンボルの定義
a, b, c = sp.symbols('a b c')

# 方程式の定義
equation_of_v1_Ne = sp.Eq(-(7*(37461949310515668487745 * a + 48553242843436673925120 * b + 369638850390945411388* a * b + 1154538 * a**2 + 4698288831886838988800))/(703687441776640 * (- 7646940 * a**2 - 12091304 * a * b + 244013957 * a - 6067440 * b**2 + 287125740 * b + 30658859)), 0)

# aの値の範囲を指定（例: 0から10まで0.1刻み）
a_values = [i/1000 for i in range(1, 10001)]

# cの値を指定
c_values = 0

# 結果を格納するリスト
results = []

# 各aに対するbの値を求める
for a_val in a_values:
    solution_of_v1_Ne = sp.solve(equation_of_v1_Ne.subs(a, a_val), b, dict=True)
    if solution_of_v1_Ne:
        positive_solution_of_v1_Ne = [sol[b].evalf() for sol in solution_of_v1_Ne if sol[b].evalf() > 0]
        if positive_solution_of_v1_Ne:
            result_dict = {'LSiSi/LNaNa': a_val, 'v1_Ne': positive_solution_of_v1_Ne}
            results.append(result_dict)

# 結果をデータフレームに変換
df = pd.DataFrame(results)

# 結果をCSVファイルに保存
df.to_csv('solutions_of_v1_Ne_for_LHH=0.csv', index=False)

    