import json
import pandas as pd
import pickle
from itertools import combinations_with_replacement

from print_output import print_choice


products = pd.read_excel("products.xlsx")


def append_options(options, name, price, *args):
    options[0].append(name)
    options[1].append(price)
    for i in range(2, 10):
        macro_sum = 0
        for one_id in args:
            macro_sum += products.iloc[one_id - 1, i]
        options[i].append(round(macro_sum, 2))


def load_and_transform_data(excluded_types=()):
    """
    The function combines McDonald's menu data from .json file and McDonald's macronutrients data from .xlsx file
    and returns placed in lists data of every possible single dish/option you can order at McDonald's.
    """

    with open("offers.json", "r", encoding="utf-8") as f:
        offers_data = json.load(f)

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

    for dish in offers_data['dishes'].keys():
        dish_id = offers_data['dishes'][dish].get("id")
        dish_types = offers_data['dishes'][dish]["types"]

        for dish_type in dish_types:
            if dish_type in excluded_types:
                continue
            match dish_type:

                case 0:     # single
                    append_options(
                        options_data,
                        dish,
                        offers_data['dishes'][dish]["price"],
                        dish_id
                    )

                case 1:     # standard-combo
                    for combo_type in ['standard-combo', 'standard-combo-plus']:
                        for d_id in offers_data[combo_type]['drink']:
                            for s_id in offers_data["fries-sauces"] + offers_data["salad-sauces"]:
                                if s_id in offers_data["fries-sauces"]:
                                    a_id = 174 if combo_type == 'standard-combo' else 175
                                else:
                                    a_id = 143
                                append_options(
                                    options_data,
                                    dish + f" {combo_type} " + products.iloc[a_id - 1, 1] + " " + products.iloc[s_id - 1, 1] + " " + products.iloc[d_id - 1, 1],
                                    offers_data['dishes'][dish]["combo-price"] + 0.00 if combo_type == 'standard-combo' else 3.00,
                                    dish_id, a_id, s_id, d_id
                                )

                case 2:     # 2forU
                    for combo_type in ['2forU', '2forU-plus']:
                        cost = 9.00 if combo_type == "2forU" else 11.00
                        for a_id in offers_data[combo_type]['addition']:
                            if a_id in [173, 174, 175]:
                                for s_id in offers_data["fries-sauces"]:
                                    append_options(
                                        options_data,
                                        dish + f" {combo_type} " + products.iloc[a_id - 1, 1] + " " + products.iloc[s_id - 1, 1],
                                        cost,
                                        dish_id, a_id, s_id
                                    )
                            else:
                                append_options(
                                    options_data,
                                    dish + f" {combo_type} " + products.iloc[a_id - 1, 1],
                                    cost,
                                    dish_id, a_id
                                )

                case 3:     # salad
                    for s_ids in combinations_with_replacement(offers_data["salad-sauces"], offers_data["dishes"][dish]["sauces"]):
                        append_options(
                            options_data,
                            dish + " " + " ".join(map(lambda s_id: products.iloc[s_id - 1, 1], s_ids)),
                            offers_data["dishes"][dish]["price"],
                            dish_id, *s_ids
                        )

                case 4:     # chicken
                    for s_ids in combinations_with_replacement(offers_data["nuggets-sauces"], offers_data["dishes"][dish]["sauces"]):
                        append_options(
                            options_data,
                            dish + " " + " ".join(map(lambda s_id: products.iloc[s_id - 1, 1], s_ids)),
                            offers_data["dishes"][dish]["price"],
                            dish_id, *s_ids
                        )

                case 5:     # chicken box
                    pass

                case 6:     # fries
                    for s_id in offers_data["fries-sauces"]:
                        append_options(
                            options_data,
                            dish + " " + products.iloc[s_id - 1, 1],
                            offers_data["dishes"][dish]["price"],
                            dish_id, s_id
                        )

                case 7:     # happy meal
                    pass

                case 8:     # drink
                    cost = {"small-drink": "price", "medium-drink": "medium-price", "large-drink": "large-price"}
                    for drink_type in ["small-drink", "medium-drink", "large-drink"]:
                        for d_id in offers_data["drink"][drink_type]:
                            append_options(
                                options_data,
                                products.iloc[d_id - 1, 1],
                                offers_data["dishes"][dish][cost[drink_type]],
                                d_id,
                            )

                case _:
                    pass

    return options_data


def pickle_to_file(content, filename):
    with open(filename, "wb") as f:
        pickle.dump(content, f)


if __name__ == "__main__":
    options = load_and_transform_data(excluded_types=[0, 1, 2, 3, 4, 5, 6, 7])

    for i in range(0, 10):
        print(len(options[i]), end=" ")
    print()

    print(options[0])
    print(options[1])
    print(options[2])

    pickle_to_file(options, "options.pkl")
