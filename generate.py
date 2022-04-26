from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
import json
from monotable import mono
from pathlib import Path
import random
import re

class AutoStrEnum(Enum):
  def _generate_next_value_(name, start, count, last_values):
    return name

class Category(AutoStrEnum):
  VEGAN = auto()
  VEGAN_OR_VEGETARIAN = auto()
  VEGETARIAN = auto()
  VEGAN_VEGETARIAN_OR_OMNI = auto()
  OMNI = auto()
  UNCATEGORIZED = auto()

vegan_tokens = {
  'agave', 'almond', 'almond milk', 'amaranth',
  'apple', 'apricot', 'artichoke', 'asparagus', 'aubergine', 'avocado',
  'banana', 'barley', 'basil', 'bean', 'beet',
  'berries', 'berry', 'beer', 'black russian', 'bread',
  'broccoli', 'bulgur', 'bruschetta',
  'cabbage', 'cactus', 'canola', 'cantaloupe', 'carrot', 'cashew', 'celery',
  'chard', 'cherry', 'cherries', 'chive', 'cider', 'cilantro',
  'cocoa', 'coffee', 'cola', 'collard', 'corn', 'couscous',
  'cress', 'cucumber', 'currant',
  'daiquiri', 'dasheen', 'date', 'dill',
  'edamame', 'eggplant',
  'energy drink',
  'falafel', 'fennel', 'fig', 'flour', 'flower', 'fries', 'fruit',
  'jam', 'juice',
  'garlic', 'gimlet', 'gin', 'ginger',
  'grain', 'grape', 'greens', 'guacamole', 'guava', 'gum',
  'hard candy', 'hummus',
  'kale', 'ketchup', 'kidney bean', 'kohlrabi', 'kumquat',
  'leaf', 'leaves', 'leek', 'lemon', 'lentil', 'lettuce',
  'lime', 'liqueur', 'luffa', 'lychee',
  'macadamia', 'malt', 'mango',
  'margarine', 'margarita', 'marmalade', 'martini', 'melon',
  'millet', 'mimosa', 'mint', 'miso', 'molasses', 'mushroom', 'mustard',
  'natto', 'nectarine', 'noodle', 'nut', 'nut butter',
  'oat', 'oat milk', 'old fashioned', 'olive', 'onion', 'orange',
  'pakora', 'papaya', 'parsley', 'parsnip', 'pasta',
  'pea', 'pecan', 'peel', 'pepper', 'persimmon',
  'pickle', 'pimiento', 'pita',
  'plant', 'plantain', 'plum', 'pomegranate', 'potato',
  'pretzel', 'prune', 'pumpkin',
  'quinoa',
  'radicchio', 'radish', 'raisin', 'rhubarb', 'rice', 'rice cake',
  'roll', 'root', 'rum',
  'sauerkraut', 'screwdriver', 'seed', 'seitan', 'sesame', 'shoot',
  'soy', 'soy milk', 'spinach',
  'soda', 'soft drink', 'sports drink', 'sprout', 'squash', 'sugar', 'syrup',
  'tabbouleh', 'tahini', 'tamarind', 'tangerine', 'tannier', 'tea', 'tequila',
  'tempeh', 'tofu', 'tomato', 'tortilla', 'truffle', 'turnip',
  'vegetable', 'vinegar', 'vodka',
  'wasabi', 'water', 'weed', 'wheat', 'whiskey',
  'yam', 'yeast',
  'zucchini', 'zwieback',
}

vegan_or_vegetarian_tokens = {
  'bar',
  'candy, nfs', 'chutney', 'cocktail, nfs', 'cracker', 'crouton',
  'dip',
  'formula',
  'nougat',
  'pesto', 'pop', 'porridge',
  'scone', 'strudel',
}

vegetarian_tokens = {
  'baklava', 'banana split', 'biscuit', 'borscht', 'butter',
  'cake', 'cappuccino', 'caramel', 'chocolate', 'cheese', 'cookie',
  'cream', 'creme', 'crepe', 'croissant', 'custard',
  'egg',
  'frost', 'french toast', 'fudge',
  'gelato',
  'honey',
  'icing',
  'kefir',
  'latte',
  'macchiato', 'mayonnaise', 'milk', 'mocha', 'mousse', 'mozzarella', 'muffin',
  'paneer', 'pastry', 'pie', 'pizza', 'praline', 'pudding',
  'ranch',
  'tiramisu', 'toffee', 'trifle', 'tzatziki',
  'waffle', 'whey', 'whipped', 'white russian',
  'yogurt',
}

vegan_vegetarian_or_omni_tokens = {
  'dumpling',
  'fat, nfs',
  'jelly',
  'kimchi',
  'ravioli, ns',
  'sandwich, nfs', 'soup, nfs', 'stew, nfs', 'sushi, nfs',
  'wine',
}

omni_tokens = {
  'adobo', 'anchovy', 'animal',
  'bacon', 'barracuda', 'bass', 'bear', 'beaver', 'beef',
  'bison', 'bologna', 'brain', 'burger',
  'caribou', 'carp', 'casserole', 'chicken', 'chorizo', 'clam',
  'cobbler', 'cod', 'crab', 'croaker',
  'deer', 'dog', 'dove', 'duck',
  'eel',
  'fish', 'flounder', 'frog',
  'gelatin', 'gizzard', 'goat', 'goulash', 'gravy', 'ground hog',
  'haddock', 'halibut', 'herring', 'ham', 'jerky',
  'kidney',
  'lamb', 'lard', 'liver', 'lobster',
  'mackerel', 'marshmallow', 'matzo', 'meat', 'meringue',
  'moose', 'mortadella', 'mullet', 'mussel',
  'nacho',
  'octopus', 'okra', 'opossum', 'ostrich', 'oyster', 'ox',
  'pad thai', 'pastrami', 'pepperoni', 'pepperpot', 'perch',
  'pig', 'pike', 'pheasant', 'porgy', 'pork', 'pot roast', 'potato skins',
  'quail',
  'rabbit', 'raccoon', 'ray', 'roe',
  'salami', 'salmon', 'sardine', 'sausage', 'scallop', 'seafood',
  'shark', 'shrimp', 'snail', 'souffle', 'squid', 'squirrel',
  'steak', 'sturgeon',
  'thuringer', 'tilapia', 'tongue', 'tripe', 'trout',
  'tuna', 'turkey', 'turtle',
  'veal', 'venison',
  'whiting', 'wurst',
}


all_tokens = (
  vegan_tokens | vegan_or_vegetarian_tokens | vegetarian_tokens |
  vegan_vegetarian_or_omni_tokens | omni_tokens
)


class MaxiMunchTokenFinder:
  def __init__(self, tokens):
    self.regex = re.compile(
      "("
      +
      "|".join(
        re.escape(token) for token in sorted(tokens, key=len, reverse=True)
      )
      +
      ")"
    )

  def find_all(self, s: str):
    return self.regex.findall(s)


all_tokens_finder = MaxiMunchTokenFinder(all_tokens)


def categorize(description) -> Category:
  names_in_desc = all_tokens_finder.find_all(description.lower())

  contains_vegan_tokens = any(
    name in vegan_tokens for name in names_in_desc
  )
  contains_vegan_or_vegetarian_tokens = any(
    name in vegan_or_vegetarian_tokens for name in names_in_desc
  )
  contains_vegetarian_tokens = any(
    name in vegetarian_tokens for name in names_in_desc
  )
  contains_vegan_vegetarian_or_omni_tokens = any(
    name in vegan_vegetarian_or_omni_tokens for name in names_in_desc
  )
  contains_omni_tokens = any(
    name in omni_tokens for name in names_in_desc
  )

  if contains_omni_tokens:
    return Category.OMNI
  elif contains_vegan_vegetarian_or_omni_tokens:
    return Category.VEGAN_VEGETARIAN_OR_OMNI
  elif contains_vegetarian_tokens:
    return Category.VEGETARIAN
  elif contains_vegan_or_vegetarian_tokens:
    return Category.VEGAN_OR_VEGETARIAN
  elif contains_vegan_tokens:
    return Category.VEGAN
  return Category.UNCATEGORIZED

@dataclass(frozen=True)
class Food:
  description: str
  fdc_id: int

  @cached_property
  def category(self):
    return categorize(self.description)

  @classmethod
  def from_fdc_food_dict(cls, d: dict):
    description = d["description"]
    fdc_id = d["fdcId"]
    return cls(description=description, fdc_id=fdc_id)

  def as_fdc_like_dict(self, include_description=False):
    return {
      **({
        "description": self.description
      } if include_description else {} ),
      "fdcId": self.fdc_id,
      "vegCategory": self.category.name
    }


def select_n_random(items, n, criterion=None):
  indices_todo = list(range(len(items)))
  selected = []
  while len(selected) < n:
    if not indices_todo:
      if criterion is not None:
        error_msg = (
          "not enough items fulfilling criterion in given sequence"
          if criterion is not None else "not enough items in given sequence"
        )
      raise ValueError(error_msg)
    i = random.choice(indices_todo)
    indices_todo.remove(i)
    item = items[i]
    if criterion is not None and not criterion(item):
      continue
    else:
      selected.append(item)
  return selected


def main():
  input_path = Path("FoodData_Central_survey_food_json_2021-10-28.json")
  with input_path.open() as f:
    d = json.load(f)

  food_ds = d["SurveyFoods"]

  foods = [Food.from_fdc_food_dict(food_d) for food_d in food_ds]

  # go through all foods and assign categories
  foods_in_categories = {
    category: [] for category in Category
  }
  for food in foods:
    foods_in_categories[food.category].append(food)

  # stats
  print("numbers:")
  for category in Category:
    n_foods = len(foods_in_categories[category])
    print(f"{n_foods} {category.name}.")

  # export JSON
  for debug in ['debug_', '']:
    output_path = (
      input_path.parent/f"{debug}VegAttributes_for_{input_path.name}"
    )
    with output_path.open("w") as f:
      json.dump(
        [
          food.as_fdc_like_dict(include_description=bool(debug))
          for food in foods
        ],
        f
      )

  # output sample
  print("sample:")
  n_samples = 10
  category_samples = {
    category: select_n_random(foods_in_categories[category], n_samples)
    for category in Category
  }

  print(mono(
    [category.name.replace("_", " ") for category in Category],
    ['(width=20;wrap)' for category in Category],
    [
      # alternate food item description rows and empty rows
      x for y in
      zip(
        # food item description row
        [
          [desc.description for desc in descs]
          for descs
          in zip(*(category_samples[category] for category in Category))
        ],
        # empty row
        [
          [ '' for category in Category ] for _ in range(n_samples)
        ]
      )
      for x in y
    ]
  ))


if __name__ == "__main__":
  main()
