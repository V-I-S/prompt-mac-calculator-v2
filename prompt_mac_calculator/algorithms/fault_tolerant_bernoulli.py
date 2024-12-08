# fault_tolerant_bernoulli.py
# Patryk Stopyra, Wrocław University of Science and Technology
#
# Model BT: Each of k transmitters tosses whether to transmit in the slot with probability p, each slot separately.


import logging

from prompt_mac_calculator.utilities.cache import cacheable

from prompt_mac_calculator.utilities.common import binomial, inclusive_range, factorial

logger = logging.getLogger('prompt-mac')


class RecursiveBernoulli:
    init_transmitters: int
    successful_transmitters: int
    failed_transmitters: int
    init_slots: int
    prob: float
    single_slot_success_prob: float

    def __init__(self, successful_transmitters: int, failed_transmitters: int, slots: int, broadcast_probability: float):
        self.init_transmitters = successful_transmitters + failed_transmitters
        self.successful_transmitters = successful_transmitters
        self.failed_transmitters = failed_transmitters
        self.init_slots = slots
        self.prob = broadcast_probability
        self.single_slot_success_prob = self._single_slot_success_prob()

    def solve(self) -> float:
        return self._recursion_step(self.successful_transmitters, self.failed_transmitters, self.init_slots)

    @cacheable
    def _recursion_step(self, transmitters: int, failed: int, slots: int) -> float:
        if transmitters == 0:
            return self._exact_slots_failure_prob(slots)
        logging.debug(f'Calculating k={transmitters}, n={slots}')
        intermediates = [self._recursion_step(transmitters - 1, failed, slots - i) *
                         self._exact_slots_success_prob(slots, i)
                         for i in inclusive_range(1, slots)]
        if failed != 0:
            intermediates.append(self._recursion_step(transmitters, failed - 1, slots) *
                                 self._exact_slots_success_prob(slots, 0))
        logging.debug(f'Elements of k={transmitters}, n={slots}: {intermediates}')
        return sum(intermediates)

    def _exact_slots_failure_prob(self, available_slots: int) -> float:
        return (1 - self.init_transmitters * self.single_slot_success_prob) ** available_slots

    def _exact_slots_success_prob(self, available_slots: int, successful_slots: int) -> float:
        return binomial(available_slots, successful_slots) * (self.single_slot_success_prob ** successful_slots)

    def _single_slot_success_prob(self) -> float:
        return self.prob * (1 - self.prob) ** (self.init_transmitters - 1)

    def _single_slot_failure_prob(self) -> float:
        return (1 - self.single_slot_success_prob) ** self.init_slots


def probability_recursive_bernoulli(transmitters: int, slots: int, broadcast_probability: float,
                                    fault_tolerance: int) -> float:
    return sum(
        [RecursiveBernoulli(transmitters - i, i, slots, broadcast_probability).solve()
         for i in inclusive_range(0, fault_tolerance)]
    )
