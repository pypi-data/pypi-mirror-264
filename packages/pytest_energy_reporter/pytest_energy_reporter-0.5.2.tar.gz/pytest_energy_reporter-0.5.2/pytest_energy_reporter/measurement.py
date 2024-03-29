
from typing import Optional
from energy_consumption_reporter.energy_tester import EnergyTester
import numpy as np

energy_tester = EnergyTester()
energy_tester.report_builder.report_path = "reports/energy/"


class EnergyMeasurement:
    '''Energy Measurement data class'''

    def __init__(self, name: str, time_ms: float, energy_j: float, power_w: float, cpu_util: float):
        self.name = name
        # Average time in mili sceonds
        self.time_ms = time_ms
        # Energy in Joules
        self.energy_j = energy_j
        # Energy in Watts
        self.power_w = power_w
        # EDP
        self.edp = (time_ms / 1000) * energy_j
        # CPU Utilization
        self.cpu_util_percent = cpu_util

    def get_time_s(self):
        return self.time_ms / 1000

    def __str__(self):
        return f"Name: {self.name}\tTime: {self.time_ms:.2f} ms\tEnergy: {self.energy_j:.2f} J\tPower: {self.power_w:.2f} W"


def measure(fn, n: int = 3, func_name: Optional[str] = None, include_case=False) -> tuple[EnergyMeasurement, Optional[any], Optional[Exception]]:
    '''Measure the energy consumption of a function n times using the energy tester'''

    # Default to the function name
    if func_name is None:
        func_name = fn.__qualname__

    # Run the energy tester
    metrics = energy_tester.test(
        fn, n, func_name=func_name, include_case=include_case)

    # Convert to measurement
    # Taking the average time, energy, and power
    time = np.mean(metrics['time'])
    energy = np.mean(metrics['energy'])
    power = np.mean(metrics['power'])
    measurement = EnergyMeasurement(func_name, time, energy, power, metrics['cpu_util'])
    result = metrics['result']
    exception = metrics['exception']

    return (measurement, result, exception)


def measure_energy(fn, n: int = 3, func_name: Optional[str] = None, include_case=False) -> EnergyMeasurement:
    '''Measure the energy consumption of a function n times using the energy tester'''
    measurement, _, _ = measure(fn, n, func_name, include_case)
    return measurement
