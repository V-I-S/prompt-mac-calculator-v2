# tslots.py
# Patryk Stopyra, Wroclaw University of Science and Technology
#
# Model BT: Each of k transmitters tosses whether to transmit in the slot with probability p, each slot separately.
import logging

from prompt_mac_calculator.utilities.common import *

logger = logging.getLogger('prompt-mac')


def communication_success_bernoulli(transmitters: int, slots: int, broadcast_probability: float) -> float:
    """
    Success is defined as a sequence of transmissions in which each transmitter had at least one slot where it was the only sending.
    """
    _validate(transmitters, slots, broadcast_probability)
    return sum([_iteration_step_a(jammed, transmitters, slots, broadcast_probability) for jammed in inclusive_range(0, transmitters)])


def _validate(transmitters: int, slots: int, broadcast_probability: float) -> None:
    if transmitters < 0 or slots < 0:
        raise ValueError('Both number of #transmitters and #slots are expected to be non-negative')
    if broadcast_probability > 1.0 or broadcast_probability < 0.0:
        raise ValueError('Single transmitter broadcasting probability is expected to be in [0, 1] interval')


def _iteration_step_a(a: int, transmitters: int, slots: int, broadcast_probability: float):
    """:a: is a number of transmitters jammed over whole transmission period (all slots)."""
    no_jam_prob = _no_jam_probability(transmitters, broadcast_probability)
    return (-1) ** a \
        * binomial(transmitters, a) \
        * (1 - a * no_jam_prob) ** slots


def _no_jam_probability(transmitters: int, broadcast_probability: float) -> float:
    return broadcast_probability * (1.0 - broadcast_probability) ** (transmitters - 1.0)
