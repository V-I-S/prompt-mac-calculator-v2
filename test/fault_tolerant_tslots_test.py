import logging
import unittest

from prompt_mac_calculator.api import tslots_success_probability, fault_tolerant_tslots_success_probability

from prompt_mac_calculator.algorithms.fault_tolerant_bernoulli import probability_recursive_bernoulli
from prompt_mac_calculator.algorithms.bernoulli import communication_success_bernoulli

logging.basicConfig(level=logging.DEBUG)


class AllSuccessTSlotsTests(unittest.TestCase):
    def test_sample_equals_2_2_1(self):
        transmitters: int = 2
        slots: int = 2
        selects: int = 1
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, 0)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        self.assertAlmostEqual(model_ts, tolerant_ts, places=9)

    def test_sample_equals_2_2_2(self):
        transmitters: int = 2
        slots: int = 2
        selects: int = 1
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, 0)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        self.assertAlmostEqual(model_ts, tolerant_ts, places=9)

    def test_sample_equals_2_3_1(self):
        transmitters: int = 2
        slots: int = 3
        selects: int = 1
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, 0)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        self.assertAlmostEqual(model_ts, tolerant_ts, places=9)

    def test_sample_equals_5_13_3(self):
        transmitters: int = 5
        slots: int = 13
        selects: int = 3
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, 0)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        self.assertAlmostEqual(model_ts, tolerant_ts, places=9)

    def test_sample_equals_5_8_1(self):
        transmitters: int = 5
        slots: int = 8
        selects: int = 3
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, 0)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        self.assertAlmostEqual(model_ts, tolerant_ts, places=9)

    def test_sample_equals_8_50_6(self):
        transmitters: int = 8
        slots: int = 50
        selects: int = 6
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, 0)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        self.assertAlmostEqual(model_ts, tolerant_ts, places=9)


class AcceptedFailuresRecursiveTests(unittest.TestCase):
    def test_sample_equals_8_50_5(self):
        transmitters: int = 10
        slots: int = 100
        selects: int = 20
        tolerance = 0
        model_ts: float = tslots_success_probability(transmitters, slots, selects)
        tolerant_ts: float = fault_tolerant_tslots_success_probability(transmitters, slots, selects, tolerance)
        print(f'result: {model_ts}, recursive: {tolerant_ts}')
        # self.assertAlmostEqual(model_ts, tolerant_ts, places=9)


if __name__ == '__main__':
    unittest.main()
