# Development notes

Notes only relevant for myself in 3 years or anyone else who looks at the code.

## Apologies

It turned out needlessly messy, in particular because

a) I tried to use it as a "testbed" for some techniques (e.g. there is a lot of
   dependency inversion in certain parts) and
b) I tried to go for zero dependencies for the package itself (i.e. excluding
   development/testing tools like pytest). No real reason why.

## "Indexed Jsonable Store"

As a consequence of (b) above, I wrote a  document database-like thing (with
greatly reduced functionality however) under `utils/indexed_jsonable_store`.
The goal here was to have a compressed and randomly accessible database of JSON
FoodData entries so that e.g. tests run faster than they would if the entire
original FoodData JSON had to be read in each time, without blowing up my hard
drive with a huge uncompressed SQLite database or anything like that. Had I
been fine with dependencies, I could've used one of the existing document
databases offering compression instead.

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
