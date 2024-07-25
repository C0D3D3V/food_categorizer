import csv
from contextlib import contextmanager
from os import PathLike
from typing import Generator, Iterable, Iterator, Mapping, Optional, Self, Union

from food_categorizer.models import ReferenceSample

DEFAULT_RS_PATH = 'reference_samples.csv'


class ReferenceSamplesCsv:
    """
    CSV file containing reference samples.
    """

    def __init__(
        self,
        file,
        csv_reader: Optional[csv.DictReader] = None,
        csv_writer: Optional[csv.DictWriter] = None,
    ):
        self.file = file
        self.csv_reader = csv_reader
        self.csv_writer = csv_writer

    @classmethod
    @contextmanager
    def from_path(
        cls,
        path: Union[PathLike, str, bytes],
        create=False,
    ) -> Iterator[Self]:
        """
        Opens CSV file for reading and/or writing depending on the given mode.
        """
        mode = "a+" if create else "r+"
        with open(path, mode, encoding='utf-8') as file:
            csv_writer = None
            if any(m in mode for m in "wa+"):
                csv_writer = csv.DictWriter(
                    file,
                    ['food_id', 'expected_diet_category', 'category', 'description'],
                    lineterminator="\n",
                )

            csv_reader = None
            if any(m in mode for m in "r+"):
                csv_reader = csv.DictReader(file)

            if csv_reader is None and csv_writer is None:
                raise ValueError("invalid mode: {repr(mode)}")

            result_store = cls(file=file, csv_reader=csv_reader, csv_writer=csv_writer)
            if create:
                result_store.write_header_if_empty()
            yield result_store

    def _reset_and_write_header(self):
        assert self.csv_writer is not None
        self.file.seek(0)
        self.file.truncate()
        self.csv_writer.writeheader()

    def write_reference_sample(self, sample: ReferenceSample):
        assert self.csv_writer is not None
        self.csv_writer.writerow(sample.as_dict())

    def write_header_if_empty(self):
        if self._is_empty():
            self._reset_and_write_header()

    def _is_empty(self):
        is_empty = False
        orig_pos = self.file.tell()
        self.file.seek(0)
        if not self.file.read(1):
            is_empty = True
        self.file.seek(orig_pos)
        return is_empty

    def append_reference_sample(self, d: ReferenceSample):
        assert self.csv_writer is not None
        self.file.seek(0, 2)  # set cursor to end of file
        self.write_reference_sample(d)

    def read_all_reference_samples(self) -> Generator[ReferenceSample, None, None]:
        """
        Read all reference sample dicts from the beginning to the end of the file.
        """
        assert self.csv_reader is not None
        self.file.seek(0)
        for row in self.csv_reader:
            yield ReferenceSample.from_dict(row)

    def get_all_mapped_by_ids(self) -> Mapping[int, ReferenceSample]:
        return {sample.food_id: sample for sample in self.read_all_reference_samples()}

    def get_all_ids(self) -> Iterable[int]:
        return (sample.food_id for sample in self.read_all_reference_samples())
