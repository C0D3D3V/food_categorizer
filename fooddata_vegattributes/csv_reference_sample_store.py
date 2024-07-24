from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Sequence

from .abstract_food_store import AbstractFoodStore
from .abstract_reference_sample_store import AbstractReferenceSampleStore
from .category import Category
from .reference_sample import ReferenceSample
from .reference_samples_csv import ReferenceSampleDict, ReferenceSamplesCsv


@dataclass
class CsvReferenceSampleStore(AbstractReferenceSampleStore):
    reference_samples_csv: ReferenceSamplesCsv
    food_store: AbstractFoodStore

    @classmethod
    @contextmanager
    def from_path_and_food_store(cls, path, food_store, create=False):
        mode = "a+" if create else "r+"
        with ReferenceSamplesCsv.from_path(path, mode) as reference_samples_csv:
            if create:
                reference_samples_csv.write_header_if_empty()
            yield cls(
                reference_samples_csv=reference_samples_csv,
                food_store=food_store,
            )

    def iter_all(self) -> Iterable[ReferenceSample]:
        return (
            ReferenceSample(
                fdc_id=d["fdc_id"],
                expected_category=(Category[d["expected_category"]]),
                known_failure=d["known_failure"],
            )
            for d in self._read_all_reference_sample_dicts()
        )

    def get_all_mapped_by_fdc_ids(self) -> Mapping[int, ReferenceSample]:
        return {reference_sample.fdc_id: reference_sample for reference_sample in self.iter_all()}

    def iter_all_fdc_ids(self) -> Iterable[int]:
        return (d["fdc_id"] for d in self._read_all_reference_sample_dicts())

    def reset_and_put_all(self, reference_samples: Sequence[ReferenceSample]):
        fdc_ids = set(sample.fdc_id for sample in reference_samples)
        foods_by_fdc_id = self.food_store.get_mapped_by_fdc_ids(fdc_ids)
        self.reference_samples_csv.reset_and_write_reference_sample_dicts(
            _reference_sample_to_dict(
                reference_sample,
                description=(
                    foods_by_fdc_id[reference_sample.fdc_id].description
                    if reference_sample.fdc_id in foods_by_fdc_id
                    else None
                ),
            )
            for reference_sample in reference_samples
        )

    def append(self, reference_sample: ReferenceSample):
        self.reference_samples_csv.append_reference_sample_dict(
            _reference_sample_to_dict(
                reference_sample,
                description=(self.food_store.get_by_fdc_id(reference_sample.fdc_id).description),
            )
        )

    def _read_all_reference_sample_dicts(self) -> Iterable[ReferenceSampleDict]:
        "Convenience/shortcut method"
        return self.reference_samples_csv.read_all_reference_sample_dicts()


def _reference_sample_to_dict(reference_sample: ReferenceSample, description: Optional[str]) -> ReferenceSampleDict:
    return {
        "fdc_id": reference_sample.fdc_id,
        "expected_category": reference_sample.expected_category.name,
        "known_failure": reference_sample.known_failure,
        "description": description,
    }
