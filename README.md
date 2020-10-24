# pygraceplot

A matplotlib.pyplot emulation for creating Grace plots.

Note that for now `pygraceplot` only generates the `.agr` file and does
not offer a wrapper to `grace` command for the image export.
It may be a feature to be implemented in the days to come.

## Requirement

- Python >= 3.7, but 3.5 should be sufficient
- NumPy

Run `pip install -r requirements.txt` to install dependencies.
If you use `conda`, try

```bash
conda install -c conda-forge -n myenv --file requirements.txt
```

Note that in this case you may need to set your virtual environment `myenv` first.

## Installation

Assume that `pygraceplot` is cloned to `path/to/pygraceplot`.

```bash
export PYTHONPATH="path/to/pygraceplot:$PYTHONPATH"
```

## Usage

See scripts in `examples`.
`pygraceplot` is capable of generating grace file for simple plots,
such as one-variable mathematical functions ([sin](examples/sin.py)),
bar graphs ([bar](examples/bar.py)), but also some complicated

## Examples

1. `Sin` function

   ![Sin(x)](examples/sin.png)

2. A bar plot

   ![Bar](examples/bar.png)

## Documentation

### Export control object: `Plot`

#### Initialization

- Positional arguments
  - `nrows`: number of rows
  - `ncols`: number of columns
- Optional keyword arguments
  - `hgap`, `vgap`: the interval between graphs in a row and in a column, respectively.
    A float number can be parsed. One can also parse a list of float, whose length
    should be the same as the number of intervals.
  - `width_ratios`, `heigh_ratios`: determine the ratios of graphs in their widths and heights.
    A `str` should be parsed, with the ratio of each graph in a column/row separated by colon `:`.
  - `bc`: background color, an `int` or `str` as the color identifier.
  - `background`: switch for the fill of background. Set to `'none'` for transparent background.
  - `lw`, `ls`, `color`, `pattern`, `charsize`, `symbolsize`: these are arguments parsed to the
    `Default` object to determine the default behavior (linewidth, linestyle, color, fill pattern) 
    of objects when created in the xmgrace GUI.
  - `description`: a `str` for describing the project.

The factory method `Plot.subplots` has the same keyword arguments and basically does the same
thing as `Plot`, but it has a more convenient way to specify number of rows and columns:

- with no positional argument: plot with a single graph
- Single positional argument, convertable to `int`:
  - `int` = n < 10 draws a plot with one column and `n` rows
  - `int` = mn, 10 < mn < 100 draws a plot with `m` rows and `n` columns

#### Methods


### Workhorse of data plotting: `Graph`

- `plot`
- `set_legend`
- `set_xlim`, `set_ylim`

### Customization with `~/.pygraceplotrc`

(Unix only)

## Miscs

### Handling of `.eps` file exported by grace

The encapsulated postscript exported by the grace engine
is not optimzed. It would be better to first process it by the
[`eps2eps`](https://nixdoc.net/man-pages/linux/man1/eps2eps.1.html) program.
Then one can convert the `.eps` to `.png` by using
[imagemagick](https://www.imagemagick.org/). For example,

```bash
convert -density 300 sin.eps sin.png
```

The figures in the [examples](examples/) is produced in this way.

