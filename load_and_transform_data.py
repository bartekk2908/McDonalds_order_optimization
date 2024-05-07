import json
import pandas as pd


def load_and_transform_data(excluded_types=[]):
    """
    The function combines McDonald's menu data from .json file and McDonald's macronutrients data from .xlsx file
    and returns placed in lists data of every possible single dish/option you can order at McDonald's.
    """

    df = pd.read_excel("products.xlsx")

    with open("offers.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    options_data = ([], [], [], [], [], [], [], [], [], [])
    # 0 - name
    # 1 - cost
    # 2 - kcal
    # 3 - fat
    # 4 - sfa
    # 5 - carbohydrates
    # 6 - sugars
    # 7 - fiber
    # 8 - protein
    # 9 - salt

    for dish in json_data['dishes'].keys():
        dish_id = json_data['dishes'][dish].get("id")
        dish_types = json_data['dishes'][dish]["types"]

        for dish_type in dish_types:
            if dish_type in excluded_types:
                continue
            match dish_type:
                case 0:     # single
                    options_data[0].append(dish)
                    options_data[1].append(json_data['dishes'][dish]["price"])
                    for i in range(2, 10):
                        options_data[i].append(df.iloc[dish_id - 1, i])
                case 1:
                    # standard-combo
                    for d_id in json_data['standard-combo']['drink']:
                        for s_id in json_data["fries-sauces"] + json_data["salad-sauces"]:
                            if s_id in json_data["fries-sauces"]:
                                a_id = 174
                            else:
                                a_id = 143

                            options_data[0].append(dish + " standard-combo " + df.iloc[a_id - 1, 1] + " " + df.iloc[s_id - 1, 1] + " " + df.iloc[d_id - 1, 1])
                            options_data[1].append(json_data['dishes'][dish]["combo-price"])
                            for i in range(2, 10):
                                options_data[i].append(df.iloc[dish_id - 1, i] + df.iloc[a_id - 1, i] + df.iloc[s_id - 1, i] + df.iloc[d_id - 1, i])

                    # standard-combo-plus
                    for d_id in json_data['standard-combo-plus']['drink']:
                        for s_id in json_data["fries-sauces"] + json_data["salad-sauces"]:
                            if s_id in json_data["fries-sauces"]:
                                a_id = 175
                            else:
                                a_id = 143

                            options_data[0].append(dish + " standard-combo-plus " + df.iloc[a_id - 1, 1] + " " + df.iloc[s_id - 1, 1] + " " + df.iloc[d_id - 1, 1])
                            options_data[1].append(json_data['dishes'][dish]["combo-price"] + 3.00)
                            for i in range(2, 10):
                                options_data[i].append(df.iloc[dish_id - 1, i] + df.iloc[a_id - 1, i] + df.iloc[s_id - 1, i] + df.iloc[d_id - 1, i])
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case 7:
                    pass
                case 8:
                    pass
                case _:
                    pass

    return options_data


def print_choice(options, choice, full=True):
    print(f"name: {options[0][choice]}")
    print(f"cost: {options[1][choice]}")
    print(f"kcal: {options[2][choice]}")
    if full:
        print(f"fat: {options[3][choice]}")
        print(f"sfa: {options[4][choice]}")
        print(f"carbohydrates: {options[5][choice]}")
        print(f"sugars: {options[6][choice]}")
        print(f"fiber: {options[7][choice]}")
        print(f"protein: {options[8][choice]}")
        print(f"salt: {options[9][choice]}")


if __name__ == "__main__":
    options = load_and_transform_data(excluded_types=[0, 2, 3, 4, 5, 6, 7, 8])

    for i in range(0, 10):
        print(len(options[i]), end=" ")
    print()

    print_choice(options, 48, True)
