from collections import defaultdict

from food_categorizer.categorizer import Categorizer
from food_categorizer.food_database import (
    DEFAULT_DB_PATH,
    load_food_data,
    update_diet_category,
)
from food_categorizer.models import DietCategory, Food
from food_categorizer.reference_samples_csv import DEFAULT_RS_PATH, ReferenceSamplesCsv
from food_categorizer.utils import print_as_table, select_n_random


def main():
    food_store = load_food_data(DEFAULT_DB_PATH)
    foods = list(food_store.values())

    # go through all foods and assign categories
    print("categorizing foods... ", end="")
    foods_in_categories = {category: [] for category in DietCategory}
    fdc_categories_to_foods_in_diet_categories = defaultdict(
        lambda: {veg_category: [] for veg_category in DietCategory}
    )

    with ReferenceSamplesCsv.from_path(DEFAULT_RS_PATH, create=True) as ref_store:
        categorizer = Categorizer(ref_store=ref_store, food_store=food_store)
        print("    ", end="")
        for i, food in enumerate(foods):
            print(f"\b\b\b\b{i/len(foods)*100:>3.0f}%", end="")
            categorization = categorizer.categorize(food)
            food.diet_category = DietCategory(categorization)
            foods_in_categories[categorization].append(food)
            fdc_categories_to_foods_in_diet_categories[food.category][categorization].append(food)
        print("done")

    # update
    update_diet_category(DEFAULT_DB_PATH, foods)

    # stats
    print("numbers:")
    for category in DietCategory:
        n_foods = len(foods_in_categories[category])
        print(f"{n_foods} {category.name}.")
    print("\n")

    # stats per FDC category
    print("numbers by FDC category:\n")
    for fdc_category, veg_categories_items in sorted(
        fdc_categories_to_foods_in_diet_categories.items(), key=lambda x: x[0]
    ):
        print(f"  {fdc_category}")
        for veg_category, items in veg_categories_items.items():
            n_foods = len(items)
            if not n_foods:
                continue
            print(f"    {n_foods} {veg_category.name}.")
        print("")
    print("")

    # output sample
    print("sample:")
    n_samples = 10
    category_samples = {
        category: select_n_random(
            foods_in_categories[category],
            n_samples,
            pad=lambda: Food(
                food_id=-1,
                fdc_id=-1,
                description="",
                diet_category=DietCategory.UNCATEGORIZED,
                category="",
                ingredients=(),
            ),
        )
        for category in DietCategory
    }

    print_as_table(
        [[category.name.replace("_", " ") for category in DietCategory]]
        + [
            # alternate food item description rows and empty rows
            # food item description row
            [desc.description for desc in descs]
            for descs in zip(*(category_samples[category] for category in DietCategory))
        ]
    )
