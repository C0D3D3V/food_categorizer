import sqlite3
from typing import Dict, List

from food_categorizer.models import Food

DEFAULT_DB_PATH = 'food_data.db'


def load_food_data(database_path: str) -> Dict[int, Food]:
    """Function to load all entries in the Food table along with their ingredients"""

    print("Loading all foods from Database... ", end="")

    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Fetch all entries from the Food table
    cursor.execute('SELECT food_id, fdc_id, description, category, diet_category FROM Food')
    food_records = cursor.fetchall()

    # Fetch all ingredients from the FoodIngredients table
    cursor.execute('SELECT food_id, ingredient_id FROM FoodIngredients')
    ingredients_records = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Map food_id to Food dataclass instances
    food_map = {}
    for food_id, fdc_id, description, category, diet_category in food_records:
        food_map[food_id] = Food(
            food_id=food_id,
            fdc_id=fdc_id,
            description=description,
            category=category,
            diet_category=diet_category,
            ingredients=[],
        )

    # Map ingredients to corresponding Food objects
    for food_id, ingredient_id in ingredients_records:
        if food_id in food_map:
            food_map[food_id].ingredients.append(ingredient_id)

    print("done")
    return food_map


def update_diet_category(database_path: str, foods: List[Food]):
    print("Updateing diet categories")
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Update the diet_category for each food entry
    for food in foods:
        cursor.execute(
            '''
            UPDATE Food
            SET diet_category = ?
            WHERE food_id = ?
        ''',
            (food.diet_category.value, food.food_id),
        )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Diet categories updated successfully")
