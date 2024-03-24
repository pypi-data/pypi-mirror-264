![](https://hiveplotlib.readthedocs.io/stable/_static/hiveplotlib.svg)

A plotting package for generating and visualizing static Hive Plots in `matplotlib`.

![](https://gitlab.com/geomdata/hiveplotlib/-/raw/22-add-formal-holoviews-support/.gitlab/python_badge.svg)

[![](https://gitlab.com/geomdata/hiveplotlib/-/raw/master/.gitlab/matplotlib_badge.svg)](https://matplotlib.org/)
[![](https://gitlab.com/geomdata/hiveplotlib/-/raw/master/.gitlab/bokeh_badge.svg)](https://docs.bokeh.org/en/latest/)
[![](https://gitlab.com/geomdata/hiveplotlib/-/raw/master/.gitlab/holoviews_badge.svg)](https://holoviews.org/index.html)
[![](https://gitlab.com/geomdata/hiveplotlib/-/raw/master/.gitlab/plotly_badge.svg)](https://plotly.com/python/)
[![](https://gitlab.com/geomdata/hiveplotlib/-/raw/master/.gitlab/datashader_badge.svg)](https://datashader.org/)

# Installation

`hiveplotlib` can be installed via [pypi](https://pypi.org/project/hiveplotlib/):

```
$ pip install hiveplotlib
```

To uninstall, run:

```
$ pip uninstall hiveplotlib
```

By default, `hiveplotlib` supports visualization only with the [matplotlib](https://matplotlib.org/) backend, but
`hiveplotlib` also supports [bokeh](https://docs.bokeh.org/en/latest/), [holoviews](https://holoviews.org/index.html),
and [plotly](https://plotly.com/python/) visualizations, which can be installed via `pip install hiveplotlib[bokeh]`,
`pip install hiveplotlib[holoviews]`, and `pip install hiveplotlib[plotly]`, respectively.

`hiveplotlib` also supports large network visualization via the [datashader](https://datashader.org/) backend,
which can be installed as `pip install hiveplotlib[datashader]`.

# Contributing

For more on contributing to the project, see [CONTRIBUTING.md](https://gitlab.com/geomdata/hiveplotlib/-/blob/master/CONTRIBUTING.md)

# How to Use and Examples

For more on how to use the software and examples, see the
[docs](https://hiveplotlib.readthedocs.io/stable/index.html).

All the example notebooks are available for download as `jupyter` notebooks in the repository under the
[examples](https://gitlab.com/geomdata/hiveplotlib/-/tree/master/examples) directory.

If trying to run the example notebooks, note that these are maintained to run in the conda
environment in the repository, specified by `hiveplot_env.yml`.

To install this `conda` environment and associated `jupyter` kernel, clone the repository and run:

```
$ cd <path/to/repository>
$ bash install.sh
```

# More on Hive Plots

For more on Hive Plots, see our
[Introduction to Hive Plots](https://hiveplotlib.readthedocs.io/stable/introduction_to_hive_plots.html).

For additional resources, see:

- [http://www.hiveplot.com/](http://www.hiveplot.com/)

- Krzywinski M, Birol I, Jones S, Marra M (2011). Hive Plots — Rational Approach to
Visualizing Networks. Briefings in Bioinformatics (early access 9 December 2011,
doi: 10.1093/bib/bbr069).

## Acknowledgements

We'd like to thank Rodrigo Garcia-Herrera for his work on
[`pyveplot`](https://gitlab.com/rgarcia-herrera/pyveplot), which we referenced
as a starting point for our structural design. We also translated some of his utility
methods for use in this repository. 