import json
from contextlib import contextmanager
from os import PathLike
from typing import Generic, Iterable, Iterator, Self, Tuple, TypeVar, Union

from .caching_zipped_indexable_linkable_bytes_store import (
    CachingZippedIndexableLinkableBytesStore,
)
from .zipped_indexable_linkable_bytes_store import (
    ZIP_DEFLATED,
    LinkTargets,
    ZippedIndexableLinkableBytesStore,
)

T = TypeVar("T")  # JSONable


class ZippedIndexableLinkableJsonableStore(Generic[T]):
    def __init__(self, bytes_store: ZippedIndexableLinkableBytesStore):
        self.bytes_store = bytes_store

    @classmethod
    @contextmanager
    def from_path(
        cls,
        path: Union[PathLike, str, bytes],
        mode="r",
        compression=ZIP_DEFLATED,
        compresslevel=None,
        caching=True,
    ) -> Iterator[Self]:
        """
        Opens store for reading or writing depending on the given mode.
        """
        bytes_store_cls = CachingZippedIndexableLinkableBytesStore if caching else ZippedIndexableLinkableBytesStore
        with bytes_store_cls.from_path(
            path,
            mode=mode,
            compression=compression,
            compresslevel=compresslevel,
        ) as bytes_store:
            yield cls(bytes_store=bytes_store)

    def put_entries(self, index_name: str, index_values_and_data: Iterable[Tuple[str, T]]):
        self.bytes_store.put_entries(
            index_name,
            ((index_value, json.dumps(jsonable).encode("utf-8")) for index_value, jsonable in index_values_and_data),
        )

    def put_links(
        self,
        index_name: str,
        index_values_and_targets: Iterable[Tuple[str, LinkTargets]],
    ):
        """
        Targets have the semantics `(target_index_name, target_index_value)`.
        """
        self.bytes_store.put_links(index_name, index_values_and_targets)

    def get_entry(self, index_name: str, index_value: str) -> T:
        entry_bytes = self.bytes_store.get_entry(index_name, index_value)
        return json.loads(entry_bytes)

    def iter_entries(self, index_name: str, index_value: str) -> Iterable[bytes]:
        return (json.loads(entry_bytes) for entry_bytes in self.bytes_store.iter_entries(index_name, index_value))

    def iter_index(self, index_name: str) -> Iterable[str]:
        return self.bytes_store.iter_index(index_name)
