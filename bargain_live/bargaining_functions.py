from typing import List, Tuple
import pandas as pd

def calculate_total_delay_list(bargaining_time: int, delay_multiplier: float) -> List[float]:
    """
    Calculate the total delay for a player based on the bargaining time and their delay multiplier.

    Args:
        bargaining_time (int): Total time in seconds for which the delay is to be calculated.
        delay_multiplier (float): The delay multiplier for the player, which determines the delay per second.

    Returns:
        total_delay_list: A list of cumulative delays at each time step.
    """
    total_delay_list = []
    cumulative_delay = 0.0
    
    for t in range(1, bargaining_time + 1):
        cumulative_delay += delay_multiplier
        total_delay_list.append(cumulative_delay)
    
    return total_delay_list


def calculate_transaction_costs(TA_treatment_high: bool, total_bargaining_time: int) -> Tuple[List[float], List[float]]:
    """
    Calculate the cumulative costs over time with a decay factor depending on the treatment and
    compute the differences between each consecutive cost.

    Args:
        TA_treatment_high (bool): Whether the treatment for Transactional Adjustment is high.
        total_bargaining_time (int): Total time in seconds for which the costs are to be calculated.

    Returns:
        Tuple[List[float], List[float]]: 
        - A list of cumulative costs at each second.
        - A list of differences between each second's cost and the next.
    """
    decay_factor = 0.99 if TA_treatment_high else 0.93
    base_cost = 0.25

    # Calculate costs at each second
    total_cost_list = [base_cost * (decay_factor ** t) for t in range(total_bargaining_time)]

    # Calculate cumulative costs
    cumulative_cost_list = pd.Series(total_cost_list).cumsum().tolist()

    # Calculate differences between consecutive costs
    current_cost_list = [total_cost_list[i] - total_cost_list[i + 1] for i in range(len(total_cost_list) - 1)]
    current_cost_list.append(0.0)  # Append 0 for the last entry as specified

    return cumulative_cost_list, current_cost_list