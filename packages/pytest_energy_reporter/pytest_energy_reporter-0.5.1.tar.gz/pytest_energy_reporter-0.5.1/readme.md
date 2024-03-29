# An Energy Reporter Plugin for pytest

The `pytest_energy_reporter` is a `pytest` plugin can be used to report on energy and power consumption usage of code, by easily integrating in existing test suites.

It relies on the [Energy Consumption Reporter](https://github.com/aron-hoogeveen/energy-consumption-reporter) to get approximations for energy measurements.

## Installation

To install pytest energy reporter, simply run:

```bash
pip install pytest_energy_reporter
```

## Usage

The package is automatically enabled in pytest. If it is not, make sure to read the documentation on [how to enable plugins in pytest](https://docs.pytest.org/en/stable/how-to/plugins.html). To start measuring energy consumption, mark tests as energy test using:

```python
import pytest

@pytest.mark.energy
def test_fn():

# Or define the exact number of iterations to measure
@pytest.mark.energy(n=3)
def test_fn():

# Or use the measurement directly
from pytest_energy_reporter.measurement import measure_energy

def test_fn():
  measure = measure_energy(fn)
  assert measure.energy_j < 200

# Or use the measurement and the result of the method
from pytest_energy_reporter.measurement import measure

def test_fn():
  measure, result, error = measure(fn, n=2)
  assert result == # ...
  assert error == None
  assert result.energy_j < 200
```

The plugin exposes a few flags in pytest

| Flag | Argument | Default | Meaning |
| --- | --- | --- | --- |
| `--energy-iterations` | `int` | `3` |  Specify the number of iterations for the energy measurement. |
| `--save-energy-report` | `<none>` | `False` | Whether to save the energy report.
| `--energy-report-path` | `str` | `'reports/energy'` | The path to save the energy report in.

## Contributing

### Prerequistes

Make sure you have [poetry](https://python-poetry.org/) installed.

### Installation

To install the pytest energy reporter repository, run:

1. Clone the repository
```bash
git clone git@github.com:delanoflipse/pytest-energy-reporter.git
```

2. Install dependencies 
```bash
poetry install
```
### Usage

To develop the plugin, use:

```bash
poetry shell
```

And run the example test suite:

```bash
pytest --log-cli-level=DEBUG
```

### Publishing

1. Build the project:

```bash
poetry build
```
2. Publish to pip (make sure you [have credentials setup](https://python-poetry.org/docs/repositories/#configuring-credentials)):
```bash
poetry publish
```