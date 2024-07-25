from dataclasses import dataclass, field
from enum import auto
from typing import Dict, List, Self

from food_categorizer.utils import AutoStrEnum


class TokenCategory(AutoStrEnum):
    # "dummy" to block false positives, see below
    BLOCK = auto()

    # tokens that have precedence over the suggestions below
    NULLIFIES_OMNI = auto()
    NULLIFIES_OMNI_AND_VEGETARIAN = auto()

    # tokens that suggest certain categories
    SUGGESTS_VEGAN = auto()
    SUGGESTS_VEGAN_OR_VEGETARIAN = auto()
    SUGGESTS_VEGETARIAN = auto()
    SUGGESTS_VEGAN_OR_OMNI = auto()
    SUGGESTS_VEGAN_VEGETARIAN_OR_OMNI = auto()
    SUGGESTS_VEGETARIAN_OR_OMNI = auto()
    SUGGESTS_OMNI = auto()


class DietCategory(AutoStrEnum):
    VEGAN = auto()
    VEGAN_OR_VEGETARIAN = auto()
    VEGETARIAN = auto()
    VEGAN_OR_OMNI = auto()
    VEGAN_VEGETARIAN_OR_OMNI = auto()
    VEGETARIAN_OR_OMNI = auto()
    OMNI = auto()
    UNCATEGORIZED = auto()


@dataclass
class Food:
    food_id: int
    fdc_id: int
    description: str
    category: str
    diet_category: DietCategory
    ingredients: List[int] = field(default_factory=list)


@dataclass
class ReferenceSample:
    food_id: int
    expected_diet_category: DietCategory
    category: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(
            food_id=data['food_id'],
            expected_diet_category=DietCategory(data['expected_diet_category']),
            category=data['category'],
            description=data['description'],
        )

    def as_dict(self) -> Dict:
        return {
            'food_id': self.food_id,
            'expected_diet_category': self.expected_diet_category.value,
            'category': self.category,
            'description': self.description,
        }
