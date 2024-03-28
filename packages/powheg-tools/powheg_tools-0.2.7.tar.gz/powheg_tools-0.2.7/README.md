# Some useful powheg scripts

[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/powheg-tools.svg)

## Install

To install the scripts, simply run the following command:

```bash
$ pip install powheg-tools
```

## pytopdrawer

Plot powheg top files:

```bash
$ pytopdrawer pwg-btl.top
```

## cleanpowheg

This script is used to clean the powheg output files. It is useful to clean the output files before running the next iteration of the powheg process. The script is used as follows:

```bash
$ cleanpowheg [-p here/or/there]
```

## genpwgseeds

Generates a list of random seeds for the powheg process. The script is used as follows:

```bash
$ genpwgseeds [-n 10] [...]
```

Generates equidistante seed numbers, such that individual bad seeds can easily be increased without producing conflicting seeds or too long seeds

## geninitrwgt

Generates the initrwgt block for specific pdf and scale variations. The script is used as follows:

```bash
$ geninitrwgt cteq66
```


## pypowhegparse

Scan for errors in powheg output files. The script is used as follows:

```bash
pypowhegparse [-f powheg/folder/here] [...]
```

[pypi image]: https://badge.fury.io/py/powheg-tools.svg
[pypi link]: https://pypi.org/project/powheg-tools/
[pypi versions]: https://img.shields.io/pypi/pyversions/powheg-tools.svg
