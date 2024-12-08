# Patryk Stopyra
# Department of Fundamentals of Computer Science
# Wroclaw University of Technology
# 2022
#
# Slots/TDMA dynamic-programming calculator (v0.1)
import time
from prompt_mac_calculator.api import *

logging.basicConfig(level=logging.DEBUG)


def example_api_call():
    transmitters: int = 10
    slots: int = 160
    transmissions: int = 58
    transmission_probability: float = 0.002
    fault_tolerance: int = 0
    start_t = time.time()
    test_fault_tolernce_tslots(transmitters, slots, transmissions, fault_tolerance)
    # print(f'optimal config: {bernoulli_optimal_probability_choice(transmitters, slots, fault_tolerance)}')
    # test_bernoulli(transmitters, slots, transmission_probability)
    # find_best_selects(transmitters, slots)
    print(f'time: {time.time() - start_t}')


def test_fault_tolernce_tslots(transmitters: int, slots: int, t: int, tolerance: int):
    print(f'Result n={slots}, k={transmitters}, t={t}: {communication_success_probability_with_tolerance(transmitters, slots, t, tolerance)}')


def test_bernoulli(transmitters: int, slots: int, t: int):
    print(f'Result n={slots}, k={transmitters}, t={t}: {bernoulli_success_probability(transmitters, slots, t)}')


def find_best_selects(k_transmitters: int, n_slots: int) -> None:
    tslots = tslots_optimal_selects_choice(k_transmitters, n_slots)
    bernoulli = bernoulli_optimal_probability_choice(k_transmitters, n_slots)
    print(f'Optimal config tSlots (size, probability):\t\t{tslots}')
    print(f'Optimal config Bernoulli (size, probability):\t{bernoulli}')
    print(f'Ratio: {tslots[1] / bernoulli[1]}')


if __name__ == '__main__':
    '''See prompt_mac_calculator/api.py for the interface methods'''
    example_api_call()
