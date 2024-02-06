import numpy as np

# 連立方程式の係数行列と定数ベクトル
A = np.array([[2, 1],
              [1, -3]])
B = np.array([8, 1])

# 行列を拡張
augmented_matrix = np.column_stack((A, B))

# 行基本変形を実行
rref_matrix, pivot_columns = np.linalg.qr(augmented_matrix, mode='r')

# デバッグ: rref_matrixの中身を確認
print("rref_matrix:", rref_matrix)

# ガウスの消去法を実行
rank = np.linalg.matrix_rank(A)
if rank == rref_matrix.shape[1] - 1:  # 連立方程式が一意の解を持つ場合
    solution = np.linalg.solve(A, B)
    print("一意の解:", solution)
else:  # 連立方程式が解の空間を持つ場合
    print("解の空間を持つ")

    # 自由変数の数
    num_free_variables = A.shape[1] - rank

    # パラメーターのシンボル
    parameters = np.array([f'param_{i+1}' for i in range(num_free_variables)])

    # 解のパラメーター表示
    solution = {f'x_{i+1}': val for i, val in enumerate(np.linalg.lstsq(A, B, rcond=None)[0])}
    for i, param in enumerate(parameters):
        solution[param] = f"param_{i+1}"

    print("解のパラメーター表示:", solution)

