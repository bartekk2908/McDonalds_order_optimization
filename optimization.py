from scipy import optimize
import numpy as np
import pickle


def load_pickle_file(file):
    with open(file, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":

    options = load_pickle_file("options.pkl")

    values = np.array(options[2])
    sizes = np.array(options[1])

    # bounds = optimize.Bounds(0, 1)  # 0 <= x_i <= 1
    integrality = np.full_like(values, True)  # x_i are integers

    capacity = 30
    constraints = optimize.LinearConstraint(A=sizes, lb=0, ub=capacity)

    res = optimize.milp(c=-values, constraints=constraints, integrality=integrality)

    cost_sum = 0
    kcal_sum = 0
    for i in range(len(res.x)):
        if res.x[i] >= 0.5:
            print(f"{options[0][i]} x {int(res.x[i])}")
            cost_sum += options[1][i] * int(res.x[i])
            kcal_sum += options[2][i] * int(res.x[i])
    print(f"limit: {capacity} zł")
    print(f"koszt: {cost_sum} zł")
    print(f"{kcal_sum} kcal")
