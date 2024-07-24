from abc import ABCMeta, abstractmethod
from typing import Iterable, Mapping, Sequence

from .reference_sample import ReferenceSample


class AbstractReferenceSampleStore(metaclass=ABCMeta):
    @abstractmethod
    def iter_all(self) -> Iterable[ReferenceSample]: ...

    @abstractmethod
    def get_all_mapped_by_fdc_ids(self) -> Mapping[int, ReferenceSample]: ...

    @abstractmethod
    def iter_all_fdc_ids(self) -> Iterable[int]: ...

    @abstractmethod
    def reset_and_put_all(self, reference_samples: Sequence[ReferenceSample]): ...

    @abstractmethod
    def append(self, reference_sample: ReferenceSample): ...
