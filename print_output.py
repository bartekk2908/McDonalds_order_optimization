
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
