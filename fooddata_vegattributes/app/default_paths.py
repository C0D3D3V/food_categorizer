from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileNames:
    survey_fooddata_json: str
    sr_legacy_fooddata_json: str
    compressed_indexed_fooddata_json: str
    reference_samples_csv: str
    generated_vegattributes_json: str


default_filenames = FileNames(
    survey_fooddata_json="FoodData_Central_survey_food_json_2022-10-28.json",
    sr_legacy_fooddata_json="FoodData_Central_sr_legacy_food_json_2021-10-28.json",
    compressed_indexed_fooddata_json="indexed_FoodData_Central_survey_and_sr_legacy_food_json_2022-10-28.jsons.zip",
    reference_samples_csv="reference_samples.csv",
    generated_vegattributes_json="VegAttributes_for_FoodData_Central_survey_and_sr_legacy_food_json_2022-10-28.json",
)


@dataclass
class DirPaths:
    def __init__(self, dir_path: Path, file_names: FileNames):
        self.dir_path = dir_path
        self.survey_fooddata_json = self.dir_path / file_names.survey_fooddata_json
        self.sr_legacy_fooddata_json = self.dir_path / file_names.sr_legacy_fooddata_json
        self.compressed_indexed_fooddata_json = self.dir_path / file_names.compressed_indexed_fooddata_json
        self.reference_samples_csv = self.dir_path / file_names.reference_samples_csv
        self.generated_vegattributes_json = self.dir_path / file_names.generated_vegattributes_json


default_dir_paths = DirPaths(Path("."), default_filenames)
