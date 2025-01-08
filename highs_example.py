"HiGHS must be initialized before making calls to the HiGHS Python library:"""

import highspy
import numpy as np

# Highs h
h = highspy.Highs()

"""Pass a model from a HighsLp instance:"""

inf = highspy.kHighsInf
# Define a HighsLp instance
lp = highspy.HighsLp()
lp.num_col_ = 2;
lp.num_row_ = 3;
lp.col_cost_ = np.array([1, 1], dtype=np.double)
lp.col_lower_ = np.array([0, 1], dtype=np.double)
lp.col_upper_ = np.array([4, inf], dtype=np.double)
lp.row_lower_ = np.array([-inf, 5, 6], dtype=np.double)
lp.row_upper_ = np.array([7, 15, inf], dtype=np.double)
# In a HighsLp instsance, the number of nonzeros is given by a fictitious final start
lp.a_matrix_.start_ = np.array([0, 2, 5])
lp.a_matrix_.index_ = np.array([1, 2, 0, 1, 2])
lp.a_matrix_.value_ = np.array([1, 3, 1, 2, 2], dtype=np.double)
h.passModel(lp)

"""Solve model:"""

h.version()


output_flag = h.getOptionValue("output_flag")
print("output_flag:", output_flag)

output_flag = h.getOptionValue("log_to_console")
print("log_to_console:", output_flag)

output_flag = h.getOptionValue("log_dev_level")
print("log_dev_level:", output_flag)


h.setOptionValue('output_flag',False)

h.setOptionValue('log_dev_level',1)

h.setOptionValue('output_flag',True)

h.run()

"""Print solution information:"""

solution = h.getSolution()
basis = h.getBasis()
info = h.getInfo()
model_status = h.getModelStatus()
print('Model status = ', h.modelStatusToString(model_status))
print()
print('Optimal objective = ', info.objective_function_value)
print('Iteration count = ', info.simplex_iteration_count)
print('Primal solution status = ', h.solutionStatusToString(info.primal_solution_status))
print('Dual solution status = ', h.solutionStatusToString(info.dual_solution_status))
print('Basis validity = ', h.basisValidityToString(info.basis_validity))