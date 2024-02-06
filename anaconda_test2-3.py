import pandas as pd
import pulp

#データの取得
stock_df = pd.read_csv('stocks.csv')
require_df = pd.read_csv('requires.csv')
gain_df = pd.read_csv('gains.csv')

#リストの定義
P = gain_df['p'].tolist()
M = stock_df['m'].tolist()

#定数の定義
stock = {row.m:row.stock for row in stock_df.itertuples()}
gain = {row.p:row.gain for row in gain_df.itertuples()}
require = {(row.p,row.m):row.require for row in require_df.itertuples()}

#数理最適化モデルの定義
problem = pulp.LpProblem('IP2', pulp.LpMaximize)

#変数の定義
x = pulp.LpVariable.dicts('x', P, cat = 'Integer')

#制約式の定義
for p in P:
    problem += x[p] >= 0
for m in M:
    problem += pulp.lpSum([require[p,m] * x[p] for p in P]) <= stock[m]

#目的関数の定義
problem += pulp.lpSum([gain[p] * x[p] for p in P])

#求解
status = problem.solve()
print('Status:', pulp.LpStatus[status])

#計算結果の表示
for p in P:
    print(p,x[p].value())

print('obj=', problem.objective.value())