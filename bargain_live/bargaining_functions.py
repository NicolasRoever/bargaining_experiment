from typing import List, Tuple, Dict, Any
import pandas as pd
import time
import json

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

def update_player_costs_and_payoff(player: Any, group: Any, broadcast: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates the broadcast dictionary with the current transaction costs, cumulative transaction costs, 
    current payoff for termination, and payment delay for a given player based on the elapsed bargaining time.

    Args:
        player (Any): The player object containing transaction cost lists and payoff information.
        group (Any): The group object containing the start time for bargaining.
        broadcast (Dict[str, Any]): The dictionary to be updated with new player information.

    Returns:
        Dict[str, Any]: The updated broadcast dictionary with the player's current transaction costs, 
                        cumulative costs, payoff for termination, and payment delay.
    """
    # Calculate the elapsed bargaining time
    bargaining_time_elapsed = int(time.time() - group.bargain_start_time)

    # Update the broadcast dictionary with relevant values
    broadcast.update({
        'current_TA_costs': json.loads(player.current_costs_list)[bargaining_time_elapsed],
        'cumulated_TA_costs': json.loads(player.total_costs_list)[bargaining_time_elapsed],
        'current_payoff_terminate': -json.loads(player.total_costs_list)[bargaining_time_elapsed],
        'payment_delay': json.loads(player.total_delay_list)[bargaining_time_elapsed]
    })

    return broadcast

def update_player_list(player: Any, list_name: str, data: Dict[str, Any], key: str = 'amount') -> None:
    """
    Loads a list from the player's data by the specified list name, appends a new value from the given data, 
    and saves the updated list back to the player.

    Args:
        player (Any): The player object containing the list to be updated.
        list_name (str): The name of the list to be updated in the player's data.
        data (Dict[str, Any]): The data dictionary containing the new value to be appended.
        key (str, optional): The key to extract the value from the data dictionary. Defaults to 'amount'.

    Returns:
        None
    """
    # Load the specified list from the player's data, or start with an empty list if not present
    current_list = json.loads(player.field_maybe_none(list_name) or "[]")
    
    # Append the new value from the data
    current_list.append(data.get(key))
    
    # Save the updated list back to the player using the specified list name
    setattr(player, list_name, json.dumps(current_list))