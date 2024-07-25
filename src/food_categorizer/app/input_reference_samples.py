import random
from typing import Dict

from food_categorizer.food_database import DEFAULT_DB_PATH, load_food_data
from food_categorizer.models import DietCategory, Food, ReferenceSample
from food_categorizer.reference_samples_csv import DEFAULT_RS_PATH, ReferenceSamplesCsv
from food_categorizer.utils import get_fdc_app_details_url

shortcut_to_category = {
    "veg": DietCategory.VEGAN,
    "vov": DietCategory.VEGAN_OR_VEGETARIAN,
    "vgt": DietCategory.VEGETARIAN,
    "vgo": DietCategory.VEGAN_OR_OMNI,
    "vvo": DietCategory.VEGAN_VEGETARIAN_OR_OMNI,
    "vto": DietCategory.VEGETARIAN_OR_OMNI,
    "o": DietCategory.OMNI,
}


def print_ingredients(food_store: Dict[int, Food], food: Food, indent=1):
    for ingredient_id in food.ingredients:
        assert ingredient_id != food.food_id
        input_food = food_store.get(ingredient_id)
        if input_food is not None:
            print(f"{'  '*indent}{input_food.description} ", end="")
            print(f"(FDC ID: {input_food.fdc_id})")
            print_ingredients(food_store, input_food, indent + 1)
        else:
            print(f'Ingredient with id {ingredient_id} could not be found!')


def main():
    with ReferenceSamplesCsv.from_path(DEFAULT_RS_PATH, create=True) as ref_store:
        food_store = load_food_data(DEFAULT_DB_PATH)

        ids_with_ref = set(ref_store.get_all_ids())
        ids_without_ref = [food_id for food_id in food_store if food_id not in ids_with_ref]

        while ids_without_ref:
            food_id = random.choice(ids_without_ref)
            food = food_store.get(food_id)

            print(f"Food ID: {food.food_id}")
            print(f"Description: {food.description}")
            print(f"URL: {get_fdc_app_details_url(food.fdc_id)}")
            if food.ingredients:
                print("Ingredients:")
                print_ingredients(food_store, food)
            print("Category shortcuts:")
            for shortcut, category in shortcut_to_category.items():
                print(f"- {shortcut}: {category.name}")
            try:
                inp = input("Input category or s to skip, q/Ctrl-D to quit: ")
            except EOFError:
                print()
                return
            if inp.lower() == "q":
                return
            if inp.lower() == "s":
                print()
                continue
            category = shortcut_to_category[inp]
            print(category.name)
            reference_sample = ReferenceSample(
                food_id=food_id,
                expected_diet_category=DietCategory(category),
                category=food.category,
                description=food.description,
            )
            print("Appending...", end="")
            ref_store.append_reference_sample(reference_sample)
            ids_with_ref.add(food_id)
            ids_without_ref.remove(food_id)
            print("\n")
        print("no items without reference data remain")
