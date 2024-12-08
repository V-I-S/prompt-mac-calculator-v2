# tslots.py
# Patryk Stopyra, Wroclaw University of Science and Technology
#
# Model tSlots: Each of k transmitters randomly selects exactly t slots of all available as a transmission set.

import logging
from decimal import Decimal
from typing import Generator

from prompt_mac_calculator.utilities.common import *

progress = 0

logger = logging.getLogger('prompt-mac')


def communication_success_probability(transmitters: int, slots: int, selects: int) -> float:
    """Success is defined as a sequence of transmissions in which
    each transmitter had at least one slot where it was the only sending."""
    logging.debug(f'Calculating... slots:{slots}, transmitters:{transmitters}, selects:{selects}')
    _clear_counter()
    _serve_corner_cases(transmitters, slots, selects)
    proper_combinations = Decimal(_count_proper_sequence_combinations(transmitters, slots, selects))
    all_combinations = Decimal(_count_all_possible_combinations(transmitters, slots, selects))
    probability = float(proper_combinations / all_combinations)
    logging.debug(
        f'Done calculations. slots:{slots}, transmitters:{transmitters}, selects:{selects}, probability:{probability}')
    return probability


def _serve_corner_cases(transmitters: int, slots: int, selects: int) -> None:
    if transmitters <= 0:
        raise ValueError('Number of transmitters has to be non-negative')
    if slots < transmitters:
        raise ValueError('Communication success is not achievable, less slots than transmitters')
    if slots - transmitters < selects - 1:
        raise ValueError('Communication success is not achievable, pigeonhole principle')


def _count_all_possible_combinations(transmitters: int, slots: int, selects: int) -> int:
    return binomial(slots, selects) ** transmitters


def _count_proper_sequence_combinations(transmitters: int, slots: int, selects: int) -> int:
    """Returns number of combinations of sequences in 'slots'-size set of available slots."""
    value = 0
    for seq in _proper_transmission_sequences(1, transmitters, selects):
        value += _count_combinations_for_transmission_sequence(seq, transmitters, slots, selects)
    return value


def _count_combinations_for_transmission_sequence(sequence: Tuple[int], transmitters: int, slots: int,
                                                  selects: int) -> int:
    """
    Proper Sequence is a sequence of sets depicting selected transmission slots for each transmitter, in which sequence every
    transmitter set has at least one slot of unique transmission.
    """
    _log_counter(selects, sequence)

    def collided_slots_combinations_func(el: int) -> int:
        return binomial(slots - sum_seq, selects - el)

    sum_seq = sum(sequence)

    if slots < transmitters:
        return 0
    if transmitters == 1 and 1 <= slots <= selects:
        return 1
    if sum_seq > slots:
        return 0

    return binomial(slots, sum_seq) \
        * _sequence_cardinality(sequence) \
        * multinomial(sum_seq, sequence) \
        * reduce(operator.mul, map(collided_slots_combinations_func, sequence)) \
        * (-1) ** (transmitters + sum_seq)


def _sequence_cardinality(sequence: Tuple[int]) -> int:
    numerator = factorial(len(sequence))
    denominator = _sequence_cardinality_denominator(sequence)
    assert numerator % denominator == 0
    return numerator // denominator


def _sequence_cardinality_denominator(sequence: Tuple[int]) -> int:
    denominator = 1
    rep = 1
    for transmitter in range(1, len(sequence)):
        if sequence[transmitter] == sequence[transmitter - 1]:
            rep += 1
        else:
            denominator *= factorial(rep)
            rep = 1
    return denominator * factorial(rep)


def _proper_transmission_sequences(min: int, transmitters: int, selects: int) -> Generator[Tuple[int], None, None]:
    """Returns all possible configurations of non-collided slots' amount per transmitter"""
    if transmitters == 1:
        for n_slots in inclusive_range(min, selects):
            yield (n_slots,)
    else:
        for n_slots in inclusive_range(min, selects):
            for config in _proper_transmission_sequences(n_slots, transmitters - 1, selects):
                yield (n_slots,) + config


def _clear_counter() -> None:
    global progress
    progress = 0


def _log_counter(selects: int, sequence: Tuple[int]) -> None:
    global progress
    progress += 1
    if not progress % 100000:
        logging.debug(f'Iterated {progress} combinations. Present selects: {selects} sequence: {sequence}')
