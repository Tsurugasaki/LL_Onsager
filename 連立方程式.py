import numpy as np

matrix = np.array([[1, 0, -1, -1, -1],
         [1, 0, -1, -1, -1], 
         [2, 0, -3, -1, -1], 
         [0, 2, 0, 0, -2], 
         [6, 1, -8, -4, -7]])

# 行列の行列式を計算する
determinant = np.linalg.det(matrix)

# 結果を表示する
print("行列式:", determinant)