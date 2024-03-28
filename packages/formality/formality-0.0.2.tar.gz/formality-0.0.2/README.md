# Formality `formality`, Symbolic Expression Utilities

[![PyPI version](https://badge.fury.io/py/mathexp.svg)](https://badge.fury.io/py/mathexp)
[![Build](https://github.com/JWKennington/mathexp/actions/workflows/build.yml/badge.svg)](https://github.com/JWKennington/mathexp/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/jwkennington/mathexp/branch/main/graph/badge.svg?token=3Z3Z3Z3Z3Z)](https://codecov.io/gh/jwkennington/mathexp)
[![CodeFactor](https://www.codefactor.io/repository/github/jwkennington/mathexp/badge)](https://www.codefactor.io/repository/github/jwkennington/mathexp)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-391/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Documentation Status](https://readthedocs.org/projects/mathexp/badge/?version=latest)](https://mathexp.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[//]: # ([![Maintainability]&#40;https://api.codeclimate.com/v1/badges/64bec68e4630ae8fbef0/maintainability&#41;]&#40;https://codeclimate.com/github/JWKennington/mathexp/maintainability&#41;)


The `formality` repo contains a general set symbolic expression utilities, mostly for extending the capabilities of `sympy`. The repo also contains a set of executable scripts for performing various mathematical experiments. Caveat lector.

## Installation

```bash
pip install formality
```

## Sample Usage

### Working with integer partitions

```python
from formality.comb import partition

partition.from_str('3+2+1')
>>> IntegerPartition([3, 2, 1])
```

More documentation to come.
