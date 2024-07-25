#!/usr/bin/env python3
# coding=utf-8

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List


@dataclass
class FoodDataFile:
    file_path: str
    list_name: str
    food_id_key: str
    description_lambda: Callable[[Dict], str]

    def load_data(self) -> List[Dict]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get(self.list_name, [])


# Define file paths and data extraction methods
# FNDDS 10/2022
# https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_survey_food_json_2022-10-28.zip
SURVEY_FOOD = FoodDataFile(
    file_path='FoodData_Central_survey_food_json_2022-10-28.json',
    list_name='SurveyFoods',
    food_id_key='foodCode',
    description_lambda=lambda item: item.get('wweiaFoodCategory', {}).get('wweiaFoodCategoryDescription'),
)

# SR Legacy 4/2018
# https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_json_2018-04.zip
SR_LEGACY_FOOD = FoodDataFile(
    file_path='FoodData_Central_sr_legacy_food_json_2021-10-28.json',
    list_name='SRLegacyFoods',
    food_id_key='ndbNumber',
    description_lambda=lambda item: item.get('foodCategory', {}).get('description'),
)

# Foundation Foods 04/2024
# https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2024-04-18.zip
FOUNDATION_FOOD = FoodDataFile(
    file_path='foundationDownload.json',
    list_name='FoundationFoods',
    food_id_key='ndbNumber',
    description_lambda=lambda item: item.get('foodCategory', {}).get('description'),
)
DATABASE_PATH = 'food_data.db'

# Clean old database first
db_file = Path(DATABASE_PATH)
if db_file.is_file():
    try:
        db_file.unlink()
        print(f"Database file '{DATABASE_PATH}' has been deleted.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file '{DATABASE_PATH}': {e}")
        exit(1)

# Create a new SQLite database (or connect to an existing one)
print("Opening Database")
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Create tables
print("Start Database population")
cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS Food (
    food_id INTEGER PRIMARY KEY,
    fdc_id INTEGER,
    description TEXT,
    category TEXT,
    diet_category TEXT
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS FoodNutrition (
    food_id INTEGER,
    nutrition_id INTEGER,
    amount REAL,
    FOREIGN KEY (food_id) REFERENCES Food(id),
    FOREIGN KEY (nutrition_id) REFERENCES Nutritions(id)
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS FoodIngredients (
    food_id INTEGER,
    ingredient_id INTEGER,
    amount REAL,
    FOREIGN KEY (food_id) REFERENCES Food(id)
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS Nutritions (
    nutrition_id INTEGER PRIMARY KEY,
    name TEXT,
    rank INTEGER,
    unitName TEXT
)
'''
)

# Create indexes for faster searching
cursor.execute('CREATE INDEX IF NOT EXISTS idx_food_category ON Food (category)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_food_ingredients_food_id ON FoodIngredients (food_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_food_diet_category ON Food (diet_category)')


# Function to insert data into the Food table
def insert_food_data(food_file: FoodDataFile):

    cursor.execute('SELECT food_id FROM Food')
    existing_food_ids = {row[0] for row in cursor.fetchall()}

    food_data = food_file.load_data()
    for item in food_data:
        food_id = item.get(food_file.food_id_key)

        if food_id in existing_food_ids:
            continue  # Skip this item if food_id already exists

        fdc_id = item.get('fdcId')
        description = item.get('description')
        category = food_file.description_lambda(item)

        cursor.execute(
            'INSERT INTO Food (food_id, fdc_id, description, category) VALUES (?, ?, ?, ?)',
            (food_id, fdc_id, description, category),
        )

        for nutrient in item.get('foodNutrients', []):
            nutrition_id = nutrient['nutrient']['id']
            nutrition_name = nutrient['nutrient']['name']
            nutrition_rank = nutrient['nutrient']['rank']
            nutrition_unit = nutrient['nutrient']['unitName']
            amount = nutrient.get('amount', 0.0)

            cursor.execute(
                'INSERT OR IGNORE INTO Nutritions (nutrition_id, name, rank, unitName) VALUES (?, ?, ?, ?)',
                (nutrition_id, nutrition_name, nutrition_rank, nutrition_unit),
            )
            cursor.execute(
                'INSERT INTO FoodNutrition (food_id, nutrition_id, amount) VALUES (?, ?, ?)',
                (food_id, nutrition_id, amount),
            )

        for ingredient in item.get('inputFoods', []):
            ingredient_id = ingredient.get('ingredientCode')
            if ingredient_id is None:
                continue
            amount = ingredient.get('amount', 0.0)
            cursor.execute(
                'INSERT INTO FoodIngredients (food_id, ingredient_id, amount) VALUES (?, ?, ?)',
                (food_id, ingredient_id, amount),
            )


# Insert data into the database
insert_food_data(SURVEY_FOOD)
insert_food_data(SR_LEGACY_FOOD)
insert_food_data(FOUNDATION_FOOD)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database population completed successfully")
