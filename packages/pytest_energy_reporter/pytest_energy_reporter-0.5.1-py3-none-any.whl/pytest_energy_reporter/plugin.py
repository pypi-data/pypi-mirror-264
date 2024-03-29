import pytest

from .util import print_table_str
from .measurement import EnergyMeasurement, energy_tester, measure_energy

energy_metrics: list[EnergyMeasurement] = []

def pytest_addoption(parser):
    '''Add command line options for the plugin'''
    parser.addoption("--energy-iterations", action="store", default=3, type=int,
                     help="Number of runs for tests marked as 'energy'")
    parser.addoption("--energy-report-path", action="store", type=str,
                     default='reports/energy', help="Path relative to the working directory in which the energy report will be saved.")
    parser.addoption("--save-energy-report", action="store_true",
                     default=False, help="Save the energy report")


def pytest_configure(config):
    '''Configure the energy tester based on the command line options'''
    # save the energy report if the option is set
    energy_tester.set_save_report(config.getoption(
        "--save-energy-report", default=False))

    # set energy report path
    energy_tester.report_builder.report_path = config.getoption(
        "--energy-report-path")

    # add a marker for energy tests
    config.addinivalue_line(
        "markers", "energy(n): specify the number of iterations for energy analysis."
    )


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
    measurement = measure_energy(
        item.runtest, n=energy_runs, func_name=item.nodeid)
    energy_metrics.append(measurement)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''Report the energy metrics at the end of the test run'''

    # Skip report if nothing was measured
    if len(energy_metrics) == 0:
        return

    # get the energy metrics sorted by EDP
    ordered_measurements = sorted(
        energy_metrics, key=lambda x: x.edp, reverse=True)

    # report the energy metrics as a table
    terminalreporter.write_sep('-', 'Energy Summary')
    table_headers = ['Test', 'Time (s)', 'Energy (J)', 'Power (W)', 'EDP (Js)']
    table_values = [
        [
            m.name,
            f"{m.get_time_s():.2f}",
            f"{m.energy_j:.2f}",
            f"{m.power_w:.2f}",
            f"{m.edp:.1f}",
        ]
        for m in ordered_measurements
    ]
    
    # calculate the max available width in the terminal
    # this limits the width of the Test column
    # The other ones are limited by the size of their title (as these are bigger than the values)
    name_max_width = terminalreporter._screen_width - sum(list(map(lambda x: len(x) + 3, table_headers[1:]))) - 3

    table_strings = print_table_str(table_headers,
                                    table_values,
                                    max_col_widths=[name_max_width])
    for line in table_strings:
        terminalreporter.write_line(line)
