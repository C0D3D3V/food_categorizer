import json
from pathlib import Path
from unittest.mock import patch

from fooddata_vegattributes.app.generate import main

from .conftest import FakeFoodDataJson


def test_generate_vegattributes_json(
  fake_fooddata_json: FakeFoodDataJson,
  tmp_path: Path,
):
  # shortcuts
  json_path = fake_fooddata_json.path
  fooddata_dict = fake_fooddata_json.food_data_dicts[0]

  # patches
  with patch(
    "fooddata_vegattributes.app.default_paths.default_dir_paths"
    ".survey_fooddata_json",
    json_path,
  ), patch(
    "fooddata_vegattributes.app.default_paths.default_dir_paths"
    ".compressed_indexed_fooddata_json",
    tmp_path/"compressed_indexed_fooddata.json.tar.xz",
  ), patch(
    "fooddata_vegattributes.app.default_paths.default_dir_paths"
    ".generated_vegattributes_json",
    tmp_path/"generated_vegattributes.json",
  ) as generated_vegattributes_json_path:
    # run generate app
    main()

  # read results (generated VegAttributes JSON file)
  with generated_vegattributes_json_path.open() as f:
    generated_vegattributes_dicts = json.load(f)

  # checks
  assert len(generated_vegattributes_dicts) == 1
  assert generated_vegattributes_dicts == [
    {
      "fdcId": fooddata_dict["fdcId"],
      "vegCategory": "UNCATEGORIZED",
    }
  ]