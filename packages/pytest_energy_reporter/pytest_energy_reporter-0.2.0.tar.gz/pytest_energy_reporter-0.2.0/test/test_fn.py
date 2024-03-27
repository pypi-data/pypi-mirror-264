import pytest
from pytest_energy_reporter.measurement import measure_energy

pytest_plugins = ("pytest_energy_reporter.plugin",)

def fib(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n-1) + fib(n-2)

@pytest.mark.energy(n=5)
def test_fib_n5():
  fib(35)
  
@pytest.mark.energy(n=4)
def test_fib_n4():
  fib(35)
  
@pytest.mark.energy(n=3)
def test_fib_n3():
  fib(35)
  
@pytest.mark.energy(n=2)
def test_fib_n2():
  fib(35)
  
@pytest.mark.energy(n=1)
def test_fib_n1():
  fib(35)

@pytest.mark.energy()
def test_fib_2x():
  fib(35)
  fib(35)

@pytest.mark.energy()
def test_fib_lower():
  fib(34)

def test_fib_assert_w():
  energy = measure_energy(lambda: fib(34), n=3)
  assert energy.power_w < 200

def test_fib_assert_j():
  energy = measure_energy(lambda: fib(34), n=2)
  assert energy.energy_j < 1000
