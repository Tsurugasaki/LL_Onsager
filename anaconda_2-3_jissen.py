import pulp
import pandas as pd

#データの取得
stock_df = pd.read_csv('stocks.csv')
require_df = pd.read_csv('requires.csv')
gain_df = pd.read_csv('gains.csv')

#リストの定義
M = stock_df['m'].tolist()
P = gain_df['p'].tolist()

#定数の定義
stock = {row.m:row.stock for row in stock_df.itertuples()}
require = {(row.p,row.m):row.require for row in require_df.itertuples()}
gain = {row.p:row.gain for row in gain_df.itertuples()}

#線形計画問題の定義
problem = pulp.LpProblem('LP2', pulp.LpMaximize)

#変数の定義
x = pulp.LpVariable.dicts('x', P, cat='Continuous')

#制約式の定義
for p in P:
    problem += x[p] >= 0
for m in M:
    problem += pulp.lpSum(require[p,m] * x[p] for p in P) <= stock[m]

#目的関数の定義
problem += pulp.lpSum(x[p] * gain[p] for p in P)

#求解
status = problem.solve()

#結果の表示
for p in P:
    print(p,x[p].value())
print('obj=',problem.objective.value())