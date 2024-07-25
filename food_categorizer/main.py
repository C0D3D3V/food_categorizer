from argparse import ArgumentParser

from food_categorizer.app.generate import main as generate_main
from food_categorizer.app.input_reference_samples import main as input_ref_main


def main():
    parser = ArgumentParser(prog="fooddata-vegattributes")
    subparsers = parser.add_subparsers()

    generate_parser = subparsers.add_parser("generate", help="Generate vegattributes JSON")
    generate_parser.set_defaults(func=generate_main)

    input_ref_parser = subparsers.add_parser("input-ref", help="Interactively input reference data")
    input_ref_parser.set_defaults(func=input_ref_main)

    args = parser.parse_args()
    if hasattr(args, "func"):
        # If we would need Arguments ("parser.add_argument") for the function, we can collect them like this:
        # **{k: v for k, v in vars(args).items() if k != "func"}
        args.func()
    else:
        print('You need to specify one option')

    parser.exit()
