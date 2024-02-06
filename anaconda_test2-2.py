import pulp


problem = pulp.LpProblem('LP', pulp.LpMaximize)

x = pulp.LpVariable('x', cat = 'Continuous')
y = pulp.LpVariable('y', cat = 'Continious')

problem += 1 * x + 3 * y <= 30
problem += 2 * x + 1 * y <= 40
problem += x >= 0
problem += y >= 0
problem += 1 * x + 2 * y

status = problem.solve()

print('Ststus:', pulp.LpStatus[status])
print('x=', x.value(), 'y=', y.value(), 'obj=', problem.objective.value())