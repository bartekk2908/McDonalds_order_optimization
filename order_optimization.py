import json
import pandas as pd


def load_and_transform_data():
    df = pd.read_excel("products.xlsx")

    with open("offers.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    name, cost, kcal, fat, sfa, carbohydrates, sugars, fiber, protein, salt = [], [], [], [], [], [], [], [], [], []
    for dish in data['dishes'].keys():
        print(dish)
        dish_id = data['dishes'][dish].get("id")
        print(dish_id)
        dish_types = data['dishes'][dish]["types"]
        print(dish_types)

        for dish_type in dish_types:
            match dish_type:
                case 0:
                    name.append(dish)
                    cost.append(data['dishes'][dish]["price"])
                    kcal.append(df.iloc[dish_id - 1, 2])
                    fat.append(df.iloc[dish_id - 1, 3])
                    sfa.append(df.iloc[dish_id - 1, 4])
                    carbohydrates.append(df.iloc[dish_id - 1, 5])
                    sugars.append(df.iloc[dish_id - 1, 6])
                    fiber.append(df.iloc[dish_id - 1, 7])
                    protein.append(df.iloc[dish_id - 1, 8])
                    salt.append(df.iloc[dish_id - 1, 9])
                case 1:
                    pass
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

    print(name)
    print(cost)
    print(kcal)
    print(protein)


if __name__ == "__main__":
    load_and_transform_data()
