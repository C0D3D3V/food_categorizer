from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from typing import Iterable, List

from .reference_sample import ReferenceSample


class AbstractReferenceSampleStore(AbstractContextManager, metaclass=ABCMeta):
  @abstractmethod
  def close(self):
      pass

  @abstractmethod
  def get_all(self) -> List[ReferenceSample]:
    pass

  @abstractmethod
  def iter_all_fdc_ids(self) -> Iterable[int]:
    pass

  @abstractmethod
  def reset_and_put_all(self, reference_samples: Iterable[ReferenceSample]):
    pass

  @abstractmethod
  def append(self, reference_sample: ReferenceSample):
    pass
