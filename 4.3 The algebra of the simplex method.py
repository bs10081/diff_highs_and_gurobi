import highspy
import numpy as np

# 初始化HiGHS
h = highspy.Highs()
h.setOptionValue('output_flag', False)

# 定義問題
inf = highspy.kHighsInf
lp = highspy.HighsLp()

# 設置變量數量和約束數量
lp.num_col_ = 2  # x1, x2
lp.num_row_ = 3  # 三個約束

# 設置目標函數係數 (最大化 3x1 + 5x2，轉換為最小化 -3x1 - 5x2)
lp.col_cost_ = np.array([-3, -5], dtype=np.double)

# 設置變量界限
lp.col_lower_ = np.array([0, 0], dtype=np.double)      # x1>=0, x2>=0
lp.col_upper_ = np.array([4, inf], dtype=np.double)    # x1<=4, x2無上界

# 設置約束界限
lp.row_lower_ = np.array([-inf, -inf, -inf], dtype=np.double)  # 所有約束都是<=
lp.row_upper_ = np.array([4, 12, 18], dtype=np.double)        # 對應三個約束的右側值

# 設置約束矩陣（CSR格式）
lp.a_matrix_.start_ = np.array([0, 1, 3])  # 變量的非零係數起始位置
lp.a_matrix_.index_ = np.array([0, 1, 2])  # 非零係數的行索引
lp.a_matrix_.value_ = np.array([1.0, 2.0, 2.0], dtype=np.double)  # 第一個變量係數為1，第二個變量係數為2

# 修正約束矩陣
lp.a_matrix_.start_ = np.array([0, 2, 4])  # 修正起始位置
lp.a_matrix_.index_ = np.array([0, 2, 1, 2])  # 修正行索引
lp.a_matrix_.value_ = np.array([1.0, 3.0, 2.0, 2.0], dtype=np.double)  # 修正係數值

# 傳遞模型並求解
h.passModel(lp)
h.run()

# 獲取結果
solution = h.getSolution()
info = h.getInfo()
model_status = h.getModelStatus()

# 輸出結果
print('模型狀態 = ', h.modelStatusToString(model_status))
print()
print('最優目標值 = ', -info.objective_function_value)  # 注意轉回最大化問題的值
print('迭代次數 = ', info.simplex_iteration_count)
print('x1 = ', solution.col_value[0])
print('x2 = ', solution.col_value[1])
