import os
import random
import re
from dataclasses import asdict
from enum import Enum
from textwrap import wrap
from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")

FDC_APP_DETAILS_BASE_URL = "https://fdc.nal.usda.gov/fdc-app.html#/food-details/"


def get_fdc_app_details_url(fdc_id: int):
    return f"{FDC_APP_DETAILS_BASE_URL}{fdc_id}"


class AutoStrEnum(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


class MaxiMunchTokenFinder:
    def __init__(self, tokens):
        self.regex = re.compile(
            "(" + "|".join(re.escape(token) for token in sorted(tokens, key=len, reverse=True)) + ")"
        )

    def find_all(self, s: str):
        return self.regex.findall(s)


def select_n_random(
    items: Sequence[T],
    n: int,
    criterion: Optional[Callable[[T], bool]] = None,
    pad: Optional[Callable[[], T]] = None,
) -> List[T]:
    indices_todo = list(range(len(items)))
    selected: List[T] = []
    while len(selected) < n:
        if not indices_todo:
            if pad:
                selected.extend(pad() for _ in range(n - len(selected)))
                break
            error_msg = (
                "not enough items fulfilling criterion in given sequence"
                if criterion is not None
                else "not enough items in given sequence"
            )
            raise ValueError(error_msg)
        i = random.choice(indices_todo)
        indices_todo.remove(i)
        item = items[i]
        if criterion is not None and not criterion(item):
            continue
        selected.append(item)
    return selected


def print_as_table(rows, column_width=None):
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
    n_columns_set = set(len(row) for row in rows)
    assert len(n_columns_set) == 1, "all rows need to have the same amount of columns"
    n_columns = list(n_columns_set)[0]
    if column_width is None:
        column_width = terminal_width // n_columns - 1
    print("+".join("-" * column_width for _ in range(n_columns)))
    for row in rows:
        output_rows = []
        for i, column in enumerate(row):
            wrapped_rows = wrap(column, width=column_width)
            for _ in range(max(0, len(wrapped_rows) - len(output_rows))):
                output_rows.append(["" for _ in range(n_columns)])
            for j, wrapped_row in enumerate(wrapped_rows):
                output_rows[j][i] = wrapped_row
        for output_row in output_rows:
            print(
                "|".join(
                    "{{output_cell:<{w}}}".format(w=column_width).format(output_cell=output_cell)
                    for output_cell in output_row
                )
            )
        print("+".join("-" * column_width for _ in range(n_columns)))
