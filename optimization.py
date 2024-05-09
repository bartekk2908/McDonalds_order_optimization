from scipy import optimize
import numpy as np
import pickle


def load_pickle_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def solve_knapsack_problem(values, sizes, capacity):
    # bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
    integrality = np.full_like(values, True)  # x_i are integers
    constraints = optimize.LinearConstraint(A=sizes, lb=0, ub=capacity)
    res = optimize.milp(c=-values, constraints=constraints, integrality=integrality)
    return res.x


if __name__ == "__main__":

    options = load_pickle_file("options.pkl")

    money_limit = 30
    results = solve_knapsack_problem(options[2], options[1], money_limit)

    cost_sum = 0
    kcal_sum = 0
    for i in range(len(results)):
        if results[i] >= 0.5:
            print(f"{options[0][i]} x {int(results[i])}")
            cost_sum += options[1][i] * int(results[i])
            kcal_sum += options[2][i] * int(results[i])
    print(f"limit: {money_limit} zł")
    print(f"cost: {cost_sum} zł")
    print(f"{kcal_sum} kcal")
