from setuptools import setup

setup(
    name="pytest_energy_reporter",
    version='0.2.0',
    description='A energy estimation reporter for pytest',
    url='https://github.com/delanoflipse/pytest-energy-reporter',
    packages=["pytest_energy_reporter"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["pytest_energy_reporter = pytest_energy_reporter.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
