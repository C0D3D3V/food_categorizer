# from food_categorizer.combined_heuristic
import logging
from typing import Dict, Set

from food_categorizer.description_based_categorizer import (
    description_based_heuristic_categorize,
)
from food_categorizer.models import DietCategory, Food
from food_categorizer.reference_samples_csv import ReferenceSamplesCsv


class Categorizer:
    def __init__(self, ref_store: ReferenceSamplesCsv, food_store: Dict[int, Food]):
        self.ref_store = ref_store
        self.reference_samples_by_id = self.ref_store.get_all_mapped_by_ids()
        self.food_store = food_store

    def categorize(self, food: Food) -> DietCategory:
        ref = self.reference_samples_by_id.get(food.food_id)
        if ref is not None:
            # Force Category from reference
            return ref.expected_diet_category
        return self.combined_heuristic_categorize(food)

    def combined_heuristic_categorize(self, food: Food):
        ingredient_based_category = self.ingredient_based_heuristic_categorize(food)
        if ingredient_based_category == DietCategory.UNCATEGORIZED:
            return description_based_heuristic_categorize(food.description)
        return ingredient_based_category

    def ingredient_based_heuristic_categorize(self, food: Food):
        logging.debug(
            "Begin ingredient-based heuristic for %r (fdc ID: %s)",
            food.description,
            food.food_id,
        )

        input_food_categories: Set[DietCategory] = set()
        for ingredient_id in food.ingredients:
            input_food = self.food_store.get(ingredient_id)
            if input_food is None:
                logging.debug("No food data entry found for input food with id %r", ingredient_id)
                continue

            assert ingredient_id != food.food_id
            logging.debug("Processing input food  %r with id %r", ingredient_id, input_food.description)

            input_food_category = self.categorize(input_food)
            logging.debug("input food categorized as %s", input_food_category.name)

            input_food_categories.add(input_food_category)

        if DietCategory.OMNI in input_food_categories:
            return DietCategory.OMNI
        if DietCategory.VEGETARIAN_OR_OMNI in input_food_categories:
            return DietCategory.VEGETARIAN_OR_OMNI
        if DietCategory.VEGAN_VEGETARIAN_OR_OMNI in input_food_categories:
            if DietCategory.VEGETARIAN in input_food_categories:
                return DietCategory.VEGETARIAN_OR_OMNI
            return DietCategory.VEGAN_VEGETARIAN_OR_OMNI
        if DietCategory.VEGAN_OR_OMNI in input_food_categories:
            if DietCategory.VEGETARIAN in input_food_categories:
                return DietCategory.VEGETARIAN_OR_OMNI
            return DietCategory.VEGAN_OR_OMNI
        if DietCategory.VEGETARIAN in input_food_categories:
            return DietCategory.VEGETARIAN
        if DietCategory.VEGAN_OR_VEGETARIAN in input_food_categories:
            return DietCategory.VEGAN_OR_VEGETARIAN
        if DietCategory.VEGETARIAN in input_food_categories:
            return DietCategory.VEGETARIAN
        if DietCategory.VEGAN in input_food_categories:
            return DietCategory.VEGAN
        return DietCategory.UNCATEGORIZED
