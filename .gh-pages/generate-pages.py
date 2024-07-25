from collections import defaultdict
from os import environ
from pathlib import Path
from typing import Dict, List

from food_categorizer.food_database import DEFAULT_DB_PATH, load_food_data
from food_categorizer.models import DietCategory, Food
from food_categorizer.utils import get_fdc_app_details_url


def main():

    food_store = load_food_data(DEFAULT_DB_PATH)
    all_foods = list(food_store.values())

    food_by_diet_category: Dict[DietCategory, List[Food]] = defaultdict(lambda: [])
    for food in all_foods:
        food_by_diet_category[food.diet_category].append(food)

    output_dir = Path(environ.get("OUTPUT_DIR") or ".gh-pages/content")
    output_dir.mkdir(exist_ok=True)

    lists_output_dir = output_dir / "category-lists"
    lists_output_dir.mkdir(exist_ok=True)

    with (output_dir / "categories-toc.md").open("w") as toc_f:
        for category in DietCategory:
            name = category.name
            foods = food_by_diet_category[name]
            md_name = name.lower().replace("_", "-")
            toc_f.write(f"- [{name}](category-lists/{md_name}) ({len(foods)} entries)\n")

            list_md_path = (lists_output_dir / md_name).with_suffix(".md")
            with list_md_path.open("w") as list_f:
                for food in sorted(foods, key=lambda x: x.description):
                    fdc_id = food.fdc_id
                    description = food.description
                    url = get_fdc_app_details_url(fdc_id)
                    list_f.write(f"- {description} (fdcId: [{fdc_id}]({url}))\n")


if __name__ == "__main__":
    main()
