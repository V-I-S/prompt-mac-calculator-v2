import logging

from tdma_calc.algorithms.bernoulli import communication_success_bernoulli
from tdma_calc.algorithms.tslots import communication_success_probability
from prompt_mac_calculator.algorithms.fault_tolerant_bernoulli import probability_recursive_bernoulli
from prompt_mac_calculator.algorithms.fault_tolerant_tslots import communication_success_probability_with_tolerance


def tslots_success_probability(transmitters: int, slots: int, selects: int) -> float:
    """
    Calculates the all-agents communication success probability for tSlots strategy.
    tSlots strategy assumes that each agent selects t-size transmission set of available slots.

    :param transmitters: number of the transmitting agents
    :param slots: number of the available slots
    :param selects: predefined size of each agent's transmission slot
    :return: all-agents communication success probability
    """
    try:
        return communication_success_probability(transmitters, slots, selects)
    except ValueError as ex:
        logging.warning(f'Calculation threw exception: {ex}')
        return 0.0


def fault_tolerant_tslots_success_probability(transmitters: int, slots: int, selects: int,
                                              fault_tolerance: int) -> float:
    """
    Calculates the all-agents communication success probability for tSlots strategy.
    tSlots strategy assumes that each agent selects t-size transmission set of available slots.

    :param transmitters: number of the transmitting agents
    :param slots: number of the available slots
    :param selects: predefined size of each agent's transmission slot
    :param fault_tolerance: limit of accepted nodes failing to transmit without collision
    :return: all-agents communication success probability
    """
    pragmatic_fault_tolerance = fault_tolerance if fault_tolerance <= transmitters else transmitters
    try:
        return communication_success_probability_with_tolerance(transmitters, slots, selects, pragmatic_fault_tolerance)
    except ValueError as ex:
        logging.warning(f'Calculation threw exception: {ex}')
        return 0.0


def tslots_optimal_selects_choice(transmitters: int, slots: int, fault_tolerance: int = 0) -> (int, float):
    """
    Finds the optimal size of agents' transmission set and the corresponding success probability.
    tSlots strategy assumes that each agent selects t-size transmission set of available slots.

    :param transmitters: number of the transmitting agents
    :param slots: number of the available slots
    :param fault_tolerance: optional number of accepted nodes failing to transmit without collision, default 0
    :return: tuple of (optimal size of the transmission set, communication success probability)
    """
    best_selects = initial_selects = max(slots // transmitters, 1)
    probability = 0.0
    for selects in range(initial_selects, 0, -1):
        new_prob = communication_success_probability_with_tolerance(transmitters, slots, selects, fault_tolerance)
        if new_prob >= probability:
            probability = new_prob
            best_selects = selects
        else:
            break
    return best_selects, probability


def bernoulli_success_probability(transmitters: int, slots: int, broadcast_probability: float) -> float:
    """
    Calculates the all-agents communication success probability for BT strategy.
    Bernoulli trials (BT) strategy assumes that each agent tosses whether to transmit in each slot separately.

    :param transmitters: number of the transmitting agents
    :param slots: number of the available slots
    :param broadcast_probability: probability of the transmission in each slot
    :return: all-agents communication success probability
    """
    return communication_success_bernoulli(transmitters, slots, broadcast_probability)


def fault_tolerant_bernoulli_success_probability(transmitters: int, slots: int, broadcast_probability: float,
                                                 fault_tolerance: int) -> float:
    return probability_recursive_bernoulli(transmitters, slots, broadcast_probability, fault_tolerance)


def bernoulli_optimal_probability_choice(transmitters: int, slots: int, fault_tolerance: int = 0) -> (float, float):
    """
    Finds agents' best broadcast probability setup and the corresponding communication success probability.
    Bernoulli trials (BT) strategy assumes that each agent tosses whether to transmit in each slot separately.

    :param transmitters: number of transmitting agents
    :param slots: number of available slots
    :param fault_tolerance: optional number of accepted nodes failing to transmit without collision, default 0
    :return: tuple of (optimal slot transmission probability, communication success probability)
    """
    best_probability = 1 / transmitters
    if fault_tolerance == 0:
        return best_probability, bernoulli_success_probability(transmitters, slots, best_probability)
    else:
        return best_probability, fault_tolerant_bernoulli_success_probability(transmitters, slots, best_probability,
                                                                              fault_tolerance)
