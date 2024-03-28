# pytest energy reporter

The pytest energy reporter can be used to report on energy usage of code, by measuring tests.

## Installation

To install pytest energy reporter, simply run:

```bash
pip install pytest_energy_reporter
```

## Usage

The package is automatically enabled in pytest. To start measuring energy consumption, mark tests as energy test using:

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
  result = measure_energy(fn)
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

2. Clone subrepositories

```bash
git submodule init && git submodule update
```

3. Install dependencies 
```bash
poetry install
```

4. (Temporary) (Only on windows) install wmi:
```bash
poetry run pip install pywin32
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