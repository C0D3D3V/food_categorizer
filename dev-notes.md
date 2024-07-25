# Development notes

Notes only relevant for myself in 3 years or anyone else who looks at the code.

## Apologies

It turned out needlessly messy

## README.md pre-commit hook

The project's README.md is generated from the GitHub Pages markdown using an
(also extremely messy for now) pre-commit hook. Run `pre-commit install` to
install it.

## Included tools

The package comes with command-line tools to export data, improve the reference
data and do some simple querying:

```shell
$ food-categorizer --help
usage: food-categorizer [-h] {generate,input-ref,annotate-ref,list-by-veg-and-fdc-categories} ...

positional arguments:
  {generate,input-ref,annotate-ref,list-by-veg-and-fdc-categories}
    generate            generate vegattributes JSON
    input-ref           interactively input reference data

optional arguments:
  -h, --help            show this help message and exit
```

They are either self-explanatory or explained in their respective help
texts.
