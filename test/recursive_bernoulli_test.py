import logging
import unittest

from prompt_mac_calculator.algorithms.fault_tolerant_bernoulli import probability_recursive_bernoulli
from prompt_mac_calculator.algorithms.bernoulli import communication_success_bernoulli

logging.basicConfig(level=logging.INFO)


class AllSuccessRecursiveTests(unittest.TestCase):
    def test_sample_equals_2_2_half(self):
        transmitters: int = 2
        slots: int = 2
        prob: float = 0.5
        model_bt: float = communication_success_bernoulli(transmitters, slots, prob)
        recursive_bt: float = probability_recursive_bernoulli(transmitters, 0, slots, prob)
        print(f'result: {model_bt}, recursive: {recursive_bt}')
        self.assertAlmostEqual(model_bt, recursive_bt, places=9)

    def test_sample_equals_2_2_quarter(self):
        transmitters: int = 2
        slots: int = 2
        prob: float = 0.25
        model_bt: float = communication_success_bernoulli(transmitters, slots, prob)
        recursive_bt: float = probability_recursive_bernoulli(transmitters, 0, slots, prob)
        print(f'Results: {model_bt}, recursive: {recursive_bt}')
        self.assertAlmostEqual(model_bt, recursive_bt, places=9)

    def test_sample_equals_2_3_half(self):
        transmitters: int = 2
        slots: int = 3
        prob: float = 0.5
        model_bt: float = communication_success_bernoulli(transmitters, slots, prob)
        recursive_bt: float = probability_recursive_bernoulli(transmitters, 0, slots, prob)
        print(f'Results: {model_bt}, recursive: {recursive_bt}')
        self.assertAlmostEqual(model_bt, recursive_bt, places=9)

    def test_sample_equals_5_13_quarter(self):
        transmitters: int = 5
        slots: int = 13
        prob: float = 0.25
        model_bt: float = communication_success_bernoulli(transmitters, slots, prob)
        recursive_bt: float = probability_recursive_bernoulli(transmitters, 0, slots, prob)
        print(f'Results: {model_bt}, recursive: {recursive_bt}')
        self.assertAlmostEqual(model_bt, recursive_bt, places=9)

    def test_sample_equals_5_8_ptthree(self):
        transmitters: int = 5
        slots: int = 8
        prob: float = 0.3
        model_bt: float = communication_success_bernoulli(transmitters, slots, prob)
        recursive_bt: float = probability_recursive_bernoulli(transmitters, 0, slots, prob)
        print(f'Results: {model_bt}, recursive: {recursive_bt}')
        self.assertAlmostEqual(model_bt, recursive_bt, places=9)

    def test_sample_equals_8_50_oneeigth(self):
        transmitters: int = 8
        slots: int = 50
        prob: float = 0.125
        model_bt: float = communication_success_bernoulli(transmitters, slots, prob)
        recursive_bt: float = probability_recursive_bernoulli(transmitters, 0, slots, prob)
        print(f'Results: {model_bt}, recursive: {recursive_bt}')
        self.assertAlmostEqual(model_bt, recursive_bt, places=9)


class AcceptedFailuresRecursiveTests(unittest.TestCase):
    def test_sample_equals_8_50_oneeigth(self):
        transmitters: int = 10
        tolerance = 1
        slots: int = 100
        prob: float = 0.1
        recursive_bt: float = probability_recursive_bernoulli(transmitters-tolerance, tolerance, slots, prob)
        print(f'Results recursive: {recursive_bt}')
        # self.assertAlmostEqual(model_bt, recursive_bt, places=9)


if __name__ == '__main__':
    unittest.main()
