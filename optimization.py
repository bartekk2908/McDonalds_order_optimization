from scipy import optimize
import numpy as np

from load_and_transform_data import load_and_transform_data


options = load_and_transform_data(excluded_types=[2, 3, 4, 5, 6, 7, 8])


if __name__ == "__main__":

    values = np.array(options[2])
    sizes = np.array(options[1])

    bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
    integrality = np.full_like(values, True)  # x_i are integers

    capacity = 40
    constraints = optimize.LinearConstraint(A=sizes, lb=0, ub=capacity)

    res = optimize.milp(c=-values, constraints=constraints, integrality=integrality, bounds=bounds)

    for i in range(len(res.x)):
        if res.x[i] >= 0.5:
            print(options[0][i])
            print(options[1][i])
            print(options[2][i])
            print()
