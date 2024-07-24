from contextlib import contextmanager
from os import PathLike
from typing import Iterable, Iterator, Self, Union

from .fooddata import FoodDataDict
from .utils.indexed_jsonable_store import IndexedJsonableStore, IndexSpec


class CompressedIndexedFoodDataJson:
    """
    Compressed, indexed (by FDC ID) FoodData JSON entries stored in a file.
    """

    def __init__(self, compressed_indexed_json: IndexedJsonableStore[FoodDataDict]):
        self.indexed_json = compressed_indexed_json

    @classmethod
    @contextmanager
    def from_path(
        cls,
        path: Union[PathLike, str, bytes],
        mode="r",
    ) -> Iterator[Self]:
        """
        Opens archive for reading or writing depending on the given mode.

        See `CompressedIndexedJson` docs for possible modes.
        """
        with IndexedJsonableStore.from_path(
            path,
            primary_index=IndexSpec("fdc-id", lambda d: str(d["fdcId"])),
            secondary_indices=[
                IndexSpec(
                    "ingredient-code",
                    lambda d: str(d.get("foodCode") or d.get("ndbNumber")),
                ),
                IndexSpec(
                    "fdc-category-description",
                    lambda d: (
                        d.get("wweiaFoodCategory", {}).get("wweiaFoodCategoryDescription")
                        or d.get("foodCategory", {}).get("description")
                    ),
                ),
            ],
            mode=mode,
        ) as compressed_indexed_json:
            yield cls(compressed_indexed_json=compressed_indexed_json)

    def write_fooddata_dicts(self, ds: Iterable[FoodDataDict]):
        self.indexed_json.put_entries(ds)

    def get_fooddata_dict_by_fdc_id(self, fdc_id: Union[int, str]) -> FoodDataDict:
        return self.indexed_json.get_entry("fdc-id", str(fdc_id))

    def get_fooddata_dict_by_ingredient_code(self, ingredient_code: Union[int, str]) -> FoodDataDict:
        return self.indexed_json.get_entry("ingredient-code", str(ingredient_code))

    def get_all_fdc_ids(self) -> Iterable[int]:
        return [int(x) for x in self.indexed_json.iter_index("fdc-id")]

    def get_fooddata_dicts_by_fdc_category(self, fdc_category_description: str) -> Iterable[FoodDataDict]:
        return self.indexed_json.iter_entries("fdc-category-description", fdc_category_description)
