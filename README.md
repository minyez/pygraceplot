# pygraceplot

matplotlib.pyplot emulation for creating Grace plots

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

See scripts in `examples`

`Sin` function

![Sin(x)](examples/sin.png)

A bar plot

![Bar](examples/bar.png)

## Miscs

`.png` files in `examples` is created with the following steps:

1. open the corresponding `.agr` file and export to eps (`CMD+F` on macOS qtgrace)
2. clean up the eps by [`eps2eps`](https://nixdoc.net/man-pages/linux/man1/eps2eps.1.html)
3. convert the cleaned `.eps` file to `.png` by [imagemagick](https://www.imagemagick.org/). For example,

    ```bash
    convert -density 300 sin.eps sin.png
    ```

