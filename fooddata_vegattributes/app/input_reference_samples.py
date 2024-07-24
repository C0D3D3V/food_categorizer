import random

from ..abstract_food_store import AbstractFoodStore
from ..category import Category
from ..fdc_app import get_fdc_app_details_url
from ..food import Food
from ..reference_sample import ReferenceSample
from .with_default_paths import default_food_and_reference_sample_stores

shortcut_to_category = {
    "veg": Category.VEGAN,
    "vov": Category.VEGAN_OR_VEGETARIAN,
    "vgt": Category.VEGETARIAN,
    "vgo": Category.VEGAN_OR_OMNI,
    "vvo": Category.VEGAN_VEGETARIAN_OR_OMNI,
    "vto": Category.VEGETARIAN_OR_OMNI,
    "o": Category.OMNI,
}


def print_ingredients(food_store: AbstractFoodStore, food: Food, indent=1):
    for input_food_stub in food.input_food_stubs:
        assert input_food_stub.fdc_id != food.fdc_id
        try:
            input_food = food_store.get_by_ingredient_code(input_food_stub.ingredient_code)
        except KeyError:
            input_food = None
        print(f"{'  '*indent}{input_food_stub.description} ", end="")
        if input_food is not None:
            print(f"(FDC ID: {input_food.fdc_id})")
            print_ingredients(food_store, input_food, indent + 1)
        else:
            print(f"(ingredient code: {input_food_stub.ingredient_code})")


def main():
    with default_food_and_reference_sample_stores(create_ref_store=True) as (food_store, reference_sample_store):
        fdc_ids_with_ref = set(reference_sample_store.iter_all_fdc_ids())
        fdc_ids_without_ref = [fdc_id for fdc_id in food_store.get_all_fdc_ids() if fdc_id not in fdc_ids_with_ref]
        while fdc_ids_without_ref:
            fdc_id = random.choice(fdc_ids_without_ref)
            foods = food_store.get_mapped_by_fdc_ids([fdc_id])
            food = foods[fdc_id]
            print(f"FDC ID: {food.fdc_id}")
            print(f"Description: {food.description}")
            print(f"URL: {get_fdc_app_details_url(food.fdc_id)}")
            if food.input_food_stubs:
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
            elif inp.lower() == "s":
                print()
                continue
            category = shortcut_to_category[inp]
            print(category.name)
            reference_sample = ReferenceSample(
                fdc_id=food.fdc_id,
                expected_category=category,
            )
            print("Appending...", end="")
            reference_sample_store.append(reference_sample)
            fdc_ids_with_ref.add(fdc_id)
            fdc_ids_without_ref.remove(fdc_id)
            print("\n")
        print("no items without reference data remain")
