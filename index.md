---
title: food-categorizer
---
Inspired from [v3gtb](https://github.com/v3gtb/fooddata-vegattributes/)

## About

The aim of this project is to provide free and open add-on data for the
[USDA's FDC FoodData datasets](https://fdc.nal.usda.gov/download-datasets.html)
containing attributes that categorize foods as vegan, vegetarian, or neither.

This will hopefully enable applications and services that deal with nutrition
data to take these dietary preferences into account, e.g. when displaying or
suggesting foods to users. The target audience of this project are mainly small
open source projects, although nothing keeps you from using it in a commercial
project (see the License section below).

## Accuracy

The data are generated using a naive heuristic based only on the descriptions
of each food and those of its ingredients, which are compared to hardcoded
lists of phrases and the most likely categories they suggest. Neither this
approach nor the lists of phrases are perfect, so there are still many
incorrectly categorized foods that will hopefully become fewer over time.

## Strictness

For those foods whose categorization as vegan/vegetarian/omni depends on one's
level of "strictness", an attempt is made to classify them as an appropriate
composite category. E.g., wines should ideally all be categorized as
`VEGAN_VEGETARIAN_OR_OMNI` because [certain filtration methods normally used in
the winemaking process involve animal
products](https://www.peta.org/about-peta/faq/is-wine-vegan/), some of which
require killing the animal to extract, although it's plausible that a subset of
vegans/vegetarians would consider them vegan/vegetarian regardless.

Note that these same composite categories are also used more generally in cases
in which it's impossible to tell from the available information whether
something is vegan/vegetarian or not. Although this meaning is technically
distinct from the strictness-dependent categorization above, in practice they
tend to overlap almost perfectly. Returning e.g. to the example above, there do
exist strictly vegan wines made without resorting to animal products in any
step of the process, but a description saying just "wine" could refer to either
these or the non-vegan variants.

## Supported datasets

Attributes are provided for foods in the FNDDS ("Survey") and SR Legacy
datasets. Data for both datasets are provided together in one file as foods are
uniquely identified by e.g. their FDC ID and the file size is small anyway. As
of now there are no plans to extend this project to the other FDC datasets, but
who knows.

## Web preview

For debugging and demoing purposes, the current lists of foods in each category
can be viewed here:

{% include_relative categories-toc.md %}

## Source code and development

The script used to generate the data released by this project from FDC data via
the heuristic explained above can be found in the project's
[source code](https://github.com/c0d3d3v/food-categorizer).

Some incomplete notes on development can be found [here](dev-notes.html).

## License

Like the USDA FDC datasets themselves, the data published by this project is
hereby released into the public domain or, in jurisdictions where this is not
possible, the closest legal equivalent.

The script to generate the data is provided under the MIT license.
