# fault_tolerant_tslots.py
# Patryk Stopyra, Wrocław University of Science and Technology
#
# Model tSlots: Each of k transmitters randomly selects exactly t slots of all available as a transmission set.

import logging
from decimal import Decimal
from typing import Generator

from prompt_mac_calculator.utilities.common import *

progress = 0

logger = logging.getLogger('prompt-mac')


def communication_success_probability_with_tolerance(transmitters: int, slots: int, selects: int,
                                                     fault_tolerance: int) -> float:
    """Success is defined as a sequence of transmissions in which
    maximum 'fault_tolerance' transmitters had no slot where it was the only one sending."""
    logger.debug(f'Calculating... slots:{slots}, transmitters:{transmitters}, selects:{selects}')
    _clear_counter()
    _serve_corner_cases(transmitters, slots, selects, fault_tolerance)
    proper_combinations = Decimal(_proper_combinations(transmitters, slots, selects, fault_tolerance))
    all_combinations = Decimal(_all_possible_combinations(transmitters, slots, selects))
    probability = float(proper_combinations / all_combinations)
    logger.debug(
        f'Done calculations. slots:{slots}, transmitters:{transmitters}, selects:{selects}, probability:{probability}')
    return probability


def _serve_corner_cases(transmitters: int, slots: int, selects: int, fault_tolerance: int) -> None:
    if transmitters < 0:
        raise ValueError('Number of transmitters has to be positive')
    if fault_tolerance < 0:
        raise ValueError('Accepted fault tolerance has to be non-negative')
    if fault_tolerance > transmitters:
        raise ValueError('Accepted fault tolerance cannot exceed number of participating transmitters')
    if slots < transmitters:
        raise ValueError('Communication success is not achievable, less slots than transmitters')
    if slots - transmitters + fault_tolerance < selects - 1:
        raise ValueError('Communication success is not achievable, pigeonhole principle')


def _all_possible_combinations(transmitters: int, slots: int, selects: int) -> int:
    return binomial(slots, selects) ** transmitters


def _proper_combinations(transmitters: int, slots: int, selects: int, fault_tolerance: int) -> int:
    if slots < transmitters - fault_tolerance:
        return 0
    if transmitters == 0:
        return 1
    if transmitters == 1 and 1 <= slots <= selects:
        return 1

    value = 0
    for f in inclusive_range(0, fault_tolerance):
        this_value = _combinations_with_failures(transmitters, slots, selects, f)
        logger.debug(f'Tolerance: {f}, success chance: '
                      f'{this_value / _all_possible_combinations(transmitters, slots, selects)}')
        value += this_value
    return value


def _combinations_with_failures(transmitters: int, slots: int, selects: int, failures: int) -> int:
    value = 0
    for failed_seq in _transmission_sequences(0, failures, selects, slots):
        for succ_seq in _transmission_sequences(1, transmitters - failures, selects, slots - sum(failed_seq)):
            assert sum(failed_seq + succ_seq) <= slots
            value += _combinations_for_sequences(transmitters, slots, selects, failures, failed_seq, succ_seq)
            _log_counter(selects, failed_seq + succ_seq)

    return value


def _combinations_for_sequences(transmitters: int, slots: int, selects: int, failures: int,
                                failed_seq: Tuple[int], success_seq: Tuple[int]) -> int:
    def collided_slots_combinations_func(el: int) -> int:
        return binomial(slots - seq_sum, selects - el)

    seq_sum = sum(failed_seq + success_seq)
    return binomial(slots, seq_sum) \
        * multinomial(seq_sum, failed_seq + success_seq) \
        * _sequence_cardinality(failed_seq, failures) \
        * _sequence_cardinality(success_seq, transmitters - failures) \
        * (-1) ** (seq_sum + transmitters - failures) \
        * reduce(operator.mul, map(collided_slots_combinations_func, failed_seq + success_seq)) \
        * binomial(transmitters, failures)


def _sequence_cardinality(sequence: Tuple[int], sequence_len: int) -> int:
    numerator = factorial(sequence_len)
    denominator = _sequence_cardinality_denominator(sequence, sequence_len)
    assert numerator % denominator == 0
    return numerator // denominator


def _sequence_cardinality_denominator(sequence: Tuple[int], sequence_len: int) -> int:
    denominator = 1
    rep = 1
    for transmitter in range(1, sequence_len):
        if sequence[transmitter] == sequence[transmitter - 1]:
            rep += 1
        else:
            denominator *= factorial(rep)
            rep = 1
    return denominator * factorial(rep)


def _transmission_sequences(start: int, transmitters: int, selects: int, slots_left: int) -> Generator[Tuple[int], None, None]:
    """
    Returns all possible configurations of non-collided slots' amount per transmitter.
        'start' - minimum count of agent-individual transmission slots (non-decreasing, repetitive configurations compensated with the '_sequence_cardinality_denominator'
        'transmitters' - number of transmitters (agents)
        'selects' - maximum number of slots claimed by single agent
        'slots_left' - the remaining available channel capacity
    """
    if transmitters == 0:
        yield ()
    else:
        for n_slots in inclusive_range(start, min(selects, slots_left)):
            for config in _transmission_sequences(n_slots, transmitters - 1, selects, slots_left - n_slots):
                yield (n_slots,) + config


def _clear_counter() -> None:
    global progress
    progress = 0


def _log_counter(selects: int, sequence: Tuple[int]) -> None:
    global progress
    progress += 1
    if not progress % 500000:
        logger.debug(f'Iterated {progress} combinations. Present selects: {selects} sequence: {sequence}')
