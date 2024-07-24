from contextlib import contextmanager
from os import PathLike
from typing import Iterator, Self, Union

from .abstract_indexed_fooddata import AbstractIndexedFoodDataJson
from .fooddata import FoodDataDict
from .utils.indexed_jsonable_store import IndexedJsonableStore, IndexSpec


class CompressedIndexedFoodDataJson(AbstractIndexedFoodDataJson):
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
