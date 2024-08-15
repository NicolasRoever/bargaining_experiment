from typing import List, Tuple

def calculate_total_delay(player, C):
    """
    Calculate the total delay for a player based on the bargaining time and their delay multiplier.

    Args:
        player: The player object containing player-specific attributes like additional_delay and delay_multiplier.
        C: Constants class that includes TOTAL_BARGAINING_TIME and other constants used in the calculation.

    Returns:
        total_delay_list: A list of cumulative delays at each time step.
    """
    total_delay = 0
    total_delay_list = []
    
    delay_multiplier = player.delay_multiplier
    
    # Initiate list of total transaction costs
    for i in range(C.TOTAL_BARGAINING_TIME):
        total_delay = i * delay_multiplier 
        total_delay_list.append(total_delay)
    
    return total_delay_list


def calculate_transaction_costs(TA_treatment_high: bool, total_bargaining_time: int) -> Tuple[List[float], List[float]]:
    """
    Calculate the total cost over time with a decay factor depending on the treatment and
    compute the difference between each consecutive cost.

    Args:
        TA_treatment_high (bool): Whether the treatment for Transactional Adjustment is high.
        total_bargaining_time (int): Total time in seconds for which the costs are to be calculated.

    Returns:
        Tuple[List[float], List[float]]: 
        - A list of total costs at each second.
        - A list of differences between each second's cost and the next.
    """
    total_cost_list = []
    current_cost_list = []
    decay_factor = 0.99 if TA_treatment_high else 0.93
    base_cost = 0.25

    # Calculate the cost for each second
    for t in range(total_bargaining_time):
        cost_at_t = base_cost * (decay_factor ** t)
        total_cost_list.append(cost_at_t)
    
    # Calculate the difference between current and next second costs
    for i in range(len(total_cost_list) - 1):
        current_cost = total_cost_list[i] - total_cost_list[i + 1]
        current_cost_list.append(current_cost)

    # Append 0 for the last entry, as specified
    current_cost_list.append(0.0)

    return total_cost_list, current_cost_list