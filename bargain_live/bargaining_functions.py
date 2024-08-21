from typing import List, Tuple, Any, Dict
import pandas as pd
import json
import time
import re
import numpy as np

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
    cumulative_cost_list = [2.3 * np.log(t+1) for t in range(total_bargaining_time)]

    # Calculate differences between consecutive costs
    current_cost_list = [cumulative_cost_list[i+1] - cumulative_cost_list[i] for i in range(len(cumulative_cost_list) - 1)]
    current_cost_list.append(0.0)  # Append 0 for the last entry as specified

    return cumulative_cost_list, current_cost_list


def update_broadcast_dict_with_basic_values(player: Any, group: Any, broadcast: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Updates the broadcast dictionary with transaction costs, payoffs, delays, and other values based on 
    the current state of the player and group.

    Args:
        player (Any): The player object containing the necessary fields and lists.
        group (Any): The group object containing the bargaining start time.
        broadcast (Dict[int, Dict[str, Any]]): The dictionary to be updated.
        my_current_proposed_amount (Any): The current proposed amount by the player.
        other_current_proposed_amount (Any): The current proposed amount by the other player.

    Returns:
        Dict[int, Dict[str, Any]]: The updated broadcast dictionary.
    """
    
    # Calculate the elapsed bargaining time
    bargaining_time_elapsed = int(time.time() - group.bargain_start_time)

    # Parse the lists and calculate relevant values based on the elapsed time
    total_cost_y_values = json.loads(player.total_costs_list)[0:bargaining_time_elapsed + 1]
    total_delay_y_values = json.loads(player.total_delay_list)[0:bargaining_time_elapsed + 1]
    current_transaction_costs = json.loads(player.current_costs_list)[bargaining_time_elapsed]

    # Update player attributes
    player.current_TA_costs = current_transaction_costs
    player.cumulated_TA_costs = total_cost_y_values[-1]
    player.current_payoff_terminate = -player.cumulated_TA_costs
    player.payment_delay = total_delay_y_values[-1]

    # Update the broadcast dictionary with the new values individually
    broadcast['current_TA_costs'] = player.current_TA_costs
    broadcast['cumulated_TA_costs'] = player.cumulated_TA_costs
    broadcast['current_payoff_terminate'] = player.current_payoff_terminate
    broadcast['payment_delay'] = player.payment_delay
    broadcast['bargaining_time_elapsed'] = bargaining_time_elapsed
    broadcast['total_cost_y_values'] = total_cost_y_values
    broadcast['total_delay_y_values'] = total_delay_y_values
    broadcast['x_axis_values_TA_graph'] = json.loads(player.x_axis_values_TA_graph)
    broadcast['x_axis_values_delay_graph'] = json.loads(player.x_axis_values_delay_graph)
    broadcast['current_transaction_costs'] = current_transaction_costs

    return broadcast

def update_broadcast_dict_with_other_player_values(player: Any, other: Any, broadcast: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Updates the broadcast dictionary with the other player's transaction costs, payoffs, delays, and other values based on

    Args:
        player (Any): The player object containing the necessary fields and lists.
        other (Any): The other player object containing the necessary fields and lists.
        broadcast (Dict[int, Dict[str, Any]]): The dictionary to be updated.

    Returns:
        Dict[int, Dict[str, Any]]: The updated broadcast dictionary.
    
    """

    other_player_transaction_cost = other.cumulated_TA_costs

    # Update the broadcast dictionary with the new values individually
    broadcast['other_player_transaction_cost'] = other_player_transaction_cost


    return broadcast
                                                                                    
                                                                                                                          



def update_player_database_with_proposal(player: Any, data: Dict[str, Any]) -> None:
    """
    Updates the player's amount_proposed_list and offer_time_list fields with new proposal data.

    Args:
        player (Any): The player object containing the database fields.
        data (Dict[str, Any]): A dictionary containing the 'amount' and 'offer_time' to be added.

    Returns:
        None
    """
    # Update the amount_proposed_list field
    amount_proposed_list = json.loads(player.field_maybe_none('amount_proposed_list') or "[]")
    amount_proposed_list.append(data.get('amount'))
    player.amount_proposed_list = json.dumps(amount_proposed_list)

    # Update the offer_time_list field
    offer_time_list = json.loads(player.field_maybe_none('offer_time_list') or "[]")
    offer_time_list.append(data.get('offer_time'))
    player.offer_time_list = json.dumps(offer_time_list)

def update_group_database_upon_acceptance(group, data):
    """
    Updates the group's database fields upon acceptance of a deal.

    Args:
        group: The group object containing the deal details.
        data: A dictionary containing the 'amount', 'acceptance_time', and 'accepted_by' information.

    Returns:
        None
    """
    group.deal_price = float(re.sub(r'[^\d.]', '', data.get('amount'))) # This converts e.g. "$1.10" into 1.10
    group.acceptance_time = data.get('acceptance_time')
    group.accepted_by = data.get('accepted_by')


def update_group_database_upon_termination(group, data):
    """
    Updates the group's database fields upon termination of the bargaining process.

    Args:
        group: The group object containing the termination details.
        data: A dictionary containing the 'termination_time' and 'terminated_by' information.

    Returns:
        None
    """
    group.termination_time = data.get('termination_time')
    group.terminated_by = data.get('terminated_by')
    group.deal_price = None
    group.terminated = True

