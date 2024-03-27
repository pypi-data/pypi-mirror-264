import pytest

from .util import print_table_str
from .measurement import EnergyMeasurement, energy_tester, measure_energy

energy_metrics: list[EnergyMeasurement] = []


def pytest_addoption(parser):
    '''Add command line options for the plugin'''
    parser.addoption("--energy-iterations", action="store", default=3, type=int,
                     help="Number of runs for tests marked as 'energy'")
    parser.addoption("--save-energy-report", action="store_true",
                     default=False, help="Save the energy report")


def pytest_configure(config):
    '''Configure the energy tester based on the command line options'''
    if config.getoption("--save-energy-report"):
        energy_tester.set_save_report(True)
    else:
        energy_tester.set_save_report(False)


@pytest.hookimpl
def pytest_runtest_call(item):
    '''Hook into the test call to measure the energy'''	
    # only run the tests marked for energy
    if not "energy" in item.keywords:
        return

    # define the number of runs for the energy test
    energy_marker = item.get_closest_marker("energy")
    if energy_marker and energy_marker.kwargs and "n" in energy_marker.kwargs:
        energy_runs = energy_marker.kwargs.get("n")
    else:
        energy_runs = item.session.config.getoption("--energy-iterations")

    # run tests and collect metrics
    measurement = measure_energy(item.runtest, n=energy_runs, func_name=item.nodeid)
    energy_metrics.append(measurement)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''Report the energy metrics at the end of the test run'''
    
    # get the energy metrics sorted by power
    ordered_measurements = sorted(energy_metrics, key=lambda x: x.edp, reverse=True)
    
    # report the energy metrics as a table
    terminalreporter.write_sep('-', 'Energy Summary')
    table_strings = print_table_str(['Test', 'Time (s)', 'Energy (J)', 'Power (W)', 'EDP (Js)'],
                                      [[m.name, f"{m.time_s:.2f}", f"{m.energy_j:.2f}", f"{m.power_w:.2f}", f"{m.edp:.1f}"] for m in ordered_measurements])
    for line in table_strings:
        terminalreporter.write_line(line)
