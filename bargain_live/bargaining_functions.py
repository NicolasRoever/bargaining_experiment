from typing import List, Tuple, Any, Dict
import pandas as pd
import json
import time
import re
import numpy as np
import random
import math
from datetime import datetime, timezone


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


def cumulative_transaction_cost_function(time: float, cost_factor: float) -> float:
    """This function spells out the cumulative transaction cost function dependent on time"""

    cumulative_transaction_cost = time * cost_factor

    return cumulative_transaction_cost


def calculate_transaction_costs(cost_factor: float, total_bargaining_time: int) -> Tuple[List[float], List[float]]:
    """
    Calculate the cumulative costs over time with a decay factor depending on the treatment andotre
    compute the differences between each consecutive cost.

    Args:
        cost_factor (float): The cost factor for the transaction costs in costs in Euros per second.
        total_bargaining_time (int): Total time in seconds for which the costs are to be calculated.

    Returns:
        Tuple[List[float], List[float]]: 
        - A list of cumulative costs at each second.
        - A list of differences between each second's cost and the next.
    """

    time_values = np.arange(0, total_bargaining_time + 1)

    cumulative_costs = cumulative_transaction_cost_function(time = time_values, cost_factor = cost_factor)

    # Calculate the differences between each second's cost and the next
    cost_differences = np.append(np.diff(cumulative_costs), 0)

    return cumulative_costs.tolist(), cost_differences.tolist() 


def update_broadcast_dict_with_basic_values(
    player: Any, group: Any, broadcast: Dict[int, Dict[str, Any]]
) -> Dict[int, Dict[str, Any]]:
    """
    Updates the broadcast dictionary and player database with transaction costs, payoffs, delays, 
    and other values based on the current state of the player and group.

    Args:
        player (Any): The player object containing the necessary fields and lists.
        group (Any): The group object containing the bargaining start time.
        broadcast (Dict[int, Dict[str, Any]]): The dictionary to be updated.

    Returns:
        Dict[int, Dict[str, Any]]: The updated broadcast dictionary.
    """
    # Calculate elapsed bargaining time
    bargaining_time_elapsed = round(
        time.time() - group.bargain_start_time
    )
    
    # Set variables based on elapsed time
    if bargaining_time_elapsed < 0:
        current_transaction_costs = None
        current_survival_probability = 1
        cumulated_TA_costs = None
        total_cost_y_values = []
    else:
        total_cost_y_values = json.loads(player.total_costs_list)[:bargaining_time_elapsed]
        termination_probabilities_list = json.loads(player.termination_probabilities_list)
        print("bargaining_time_elapsed: ", bargaining_time_elapsed)
        current_transaction_costs = json.loads(player.current_costs_list)[bargaining_time_elapsed]
        current_termination_probability = termination_probabilities_list[bargaining_time_elapsed]
        current_survival_probability = 1 - current_termination_probability
        cumulated_TA_costs = total_cost_y_values[bargaining_time_elapsed - 1] if total_cost_y_values else None

    # Update player attributes if values exist and are valid
    if total_cost_y_values and bargaining_time_elapsed > 0 and cumulated_TA_costs is not None:
        player.current_TA_costs = current_transaction_costs
        player.cumulated_TA_costs = cumulated_TA_costs
        player.current_payoff_terminate = -cumulated_TA_costs
    
    # Update the broadcast dictionary with the new values
    broadcast.update({
        'current_TA_costs': player.field_maybe_none('current_TA_costs'),
        'cumulated_TA_costs': player.field_maybe_none('cumulated_TA_costs'),
        'current_payoff_terminate': player.field_maybe_none('current_payoff_terminate'),
        'payment_delay': player.field_maybe_none('payment_delay'),
        'bargaining_time_elapsed': bargaining_time_elapsed,
        'total_cost_y_values': total_cost_y_values,
        'x_axis_values_TA_graph': json.loads(player.x_axis_values_TA_graph),
        'current_transaction_costs': current_transaction_costs,
        'current_survival_probability': current_survival_probability,
    })
    
    return broadcast

def update_broadcast_dict_with_other_player_values(player: Any, broadcast: Dict[int, Dict[str, Any]], practice_round: bool) -> Dict[int, Dict[str, Any]]:
    """
    Updates the broadcast dictionary with the other player's transaction costs, payoffs, delays, and other values based on

    Args:
        player (Any): The player object containing the necessary fields and lists.
        other (Any): The other player object containing the necessary fields and lists.
        broadcast (Dict[int, Dict[str, Any]]): The dictionary to be updated.

    Returns:
        Dict[int, Dict[str, Any]]: The updated broadcast dictionary.
    
    """

    if practice_round:
        other_player_transaction_cost = player.field_maybe_none('cumulated_TA_costs') #I simulate here that the other player has the same transaction costs as the player himself.
    else:
        [other] = player.get_others_in_group()
        other_player_transaction_cost = other.field_maybe_none('cumulated_TA_costs')

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
    amount_proposed_list = json.loads(player.amount_proposed_list)
    offer = data.get('amount')
    if offer is not None:
        amount_proposed_list.append(float(offer))
    player.amount_proposed_list = json.dumps(amount_proposed_list)
    player.current_amount_proposed = data.get('amount')

    # Update the offer_time_list field
    offer_time_list = json.loads(player.offer_time_list)
    offer_time = data.get('offer_time')
    print("Here is the offer time: ", offer_time)
    if offer_time is not None:
        offer_time_list.append(float(offer_time))
    player.offer_time_list = json.dumps(offer_time_list)
    player.proposal_made = True


def update_group_database_upon_acceptance(group: Any, data: Dict[str, Any]) -> None:
    """
    Updates the group's database fields upon acceptance of a deal.

    Args:
        group: The group object containing the deal details.
        data: A dictionary containing the 'amount', 'acceptance_time', and 'accepted_by' information.

    Returns:
        None
    """

    group.deal_price = float(re.sub(r'[^\d.]', '', str(data.get('amount')))) # This converts e.g. "$1.10" into 1.10, and ensures that it also works for the practice rounds where amount is a float.
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
    group.termination_mode = 'Player'

def update_group_database_upon_random_termination(group: Any) -> None:
    """
    Updates the group's database fields upon random termination of the bargaining process.

    Args:
        group: The group object containing the termination details.

    Returns:
        None
    """
    bargaining_time_elapsed = round(time.time() - group.bargain_start_time)
    group.is_finished = True
    group.termination_time = bargaining_time_elapsed
    group.termination_mode = 'Random_Termination'
    group.deal_price = None
    group.terminated = True


def setup_player_valuation(player: Any) -> None:
    """
    Sets up the player's valuation and saves it in the SQL database.
    This valuation setup is based on the theory model. 

    Args:
        player (Any): The player object containing the specific players database.

    Returns:
        None
    """

    if player.role == "Seller":
        player.valuation = 50

    elif player.role == "Buyer":
        valuation_list = list(range(1, 61, 1))
        player.valuation = random.choice(valuation_list)


def setup_player_transaction_costs(player: Any, cost_factor: float, total_bargaining_time) -> None:
    """This function sets up the player's transaction costs based on the treatment. and saves the data in the player database.

    Args:
        player: The player object containing the specific player's database.
        cost_factor: The cost factor for the transaction costs in costs in Euros per second.
        total_bargaining_time: The total time for bargaining in seconds.

    Returns:
        None
    """

    #Calculate Transacion Costs
    transaction_cost_list, current_costs_list = calculate_transaction_costs(
    cost_factor=cost_factor, 
    total_bargaining_time=total_bargaining_time)


    #Save all values relevant for displaying transaction costs in the database
    
    player.total_costs_list = json.dumps(transaction_cost_list)
    player.current_costs_list = json.dumps(current_costs_list)
    player.x_axis_values_TA_graph = json.dumps(list(range(0, total_bargaining_time + 1)))
    player.y_axis_maximum_TA_graph = 20


def setup_player_delay_list(player: Any, delay_treatment_high: bool, total_bargaining_time: int) -> None:
    """
    This function sets up the player's delay list and saves the data in the player database.

    Args:
        player: The player object containing the specific player's database.
        delay_multiplier: The delay multiplier for the player.
        total_bargaining_time: The total time for bargaining in seconds.

    Returns:
        None
    """

    delay_multiplier = 3.5 if delay_treatment_high else 1
    player.delay_multiplier = delay_multiplier

    # Calculate the total delay list
    total_delay_list = calculate_total_delay_list(total_bargaining_time, delay_multiplier)

    # Save all values relevant for displaying delays in the database
    player.total_delay_list = json.dumps(total_delay_list)
    player.x_axis_values_delay_graph = json.dumps(list(range(0, total_bargaining_time + 1)))
    player.y_axis_maximum_delay_graph = math.ceil(total_bargaining_time * delay_multiplier)


def setup_player_shrinking_pie_discount_factors(player: Any, delay_treatment_high: bool, total_bargaining_time: int) -> None:
    """
    This function sets up the player's discount factors for the shrinking pie in the bargaining game.

    Args:
        player: The player object containing the specific player's database.
        delay_treatment_high: The delay treatment for the player.
        total_bargaining_time: The total time for bargaining in seconds.
    """

    discount_factors = calculate_discount_factors_for_shrinking_pie(delay_treatment_high, total_bargaining_time)

    player.discount_factors_list = json.dumps(discount_factors)





def record_player_payoff_from_round(player: Any) -> None:
    """
    Records the player's payoff from the round in the SQL database.

    Args:
        player (Any): The player object containing the specific player's database.
        group (Any): The group object containing the deal price.

    Returns:
        None
    """
    
    #Case 1: A deal was made
    if player.group.field_maybe_none('deal_price'):

        transaction_costs = player.cumulated_TA_costs

        if player.participant.vars['role_in_game'] == "Seller":
            player.payoff = (player.group.deal_price - player.valuation)  - transaction_costs 


        elif player.participant.vars['role_in_game'] == "Buyer":
            player.payoff = (player.valuation - player.group.deal_price)  - transaction_costs 


    #Case 2: A deal was terminated
    elif player.group.field_maybe_none('terminated'):

        transaction_costs = player.cumulated_TA_costs

        player.payoff = -transaction_costs 


    #Case 3: Time was up

    else: 
        player.payoff = -json.loads(player.total_costs_list)[-1] 
    


def record_bargaining_time_on_group_level(player: Any, C: Any) -> None:
    """
    Records the bargaining time on the group level in the SQL database.

    Args:
        player (Any): The player object containing the specific player's database.
        C (Any): The Constants object 

    Returns:
        None
    """


    #Case 1: There was an acceptance

    if player.group.field_maybe_none('acceptance_time'):

        player.group.bargaining_duration = player.group.acceptance_time

    #Case 2: There was a termination
    
    elif player.group.field_maybe_none('termination_time'):

        player.group.bargaining_duration = player.group.termination_time 

    #Case 3: Time was up
    else:
        player.group.bargaining_duration = C.TOTAL_BARGAINING_TIME

def set_final_player_payoff(player: Any, C: Any) -> None:
    """
    Chooses a random round to determine the final payoffs. 

    Args:
        player (Any): The player object containing the specific player's database.
        C (Any): The Constants object containing the number of rounds.

    Returns:
        None
    """

    player.participant.random_round = random.choice(list(range(1, C.NUM_ROUNDS)))
    player.participant.payoff = player.in_round(player.participant.random_round).payoff + player.group.subsession.session.config['participation_fee']
    player.participant.vars["clerpay_amount"] = float(player.participant.payoff) if float(player.participant.payoff) >= 7.5 else 7.5



def create_random_values_dataframe(number_of_groups: int, buyer_valuations: pd.Series) -> pd.DataFrame:
    """
    Creates a dataframe with all random values needed in the experiment.

    Args:
        number_of_groups (int): The number of groups; each group consists of eight participants.
        buyer_valuations (pd.Series): The vector of buyer valuations to draw from.

    Returns:
        pd.Dataframe: A dataframe with all random values.
        Columns:
        - Participant_ID: The unique ID of the participant.
        - Group_ID: The unique ID of the group.
        - Role: The role of the participant.
        - Valuation: The valuation of the participant.
        - Transaction_Costs: The transaction costs of the participant.
        - Delay_Treatment: The delay multiplier of the participant.
        - Match_Round_X: The participant_ID with whom the player is matched in the respective round X. 
    """

    # Initialize Participant Number
    participant_ids = list(range(1, 8 * number_of_groups + 1)) 
    df = pd.DataFrame({'Participant_ID': participant_ids})

    #Initialize Group ID's
    group_ids = np.repeat(range(1, number_of_groups + 1), 8)
    np.random.shuffle(group_ids)
    df['Group_ID'] = group_ids

    #Initialize Roles
    df["Role"] =  df.groupby('Group_ID')['Participant_ID'].transform(
    lambda x: np.random.permutation(['Seller'] * 4 + ['Buyer'] * 4))

    #Initialize Transaction Cost Treatment
    df["TA_Treatment"] = df.groupby('Group_ID')['Participant_ID'].transform(lambda x: np.random.permutation(['High'] * 4 + ['Low'] * 4))

    #Initialize Delay Treatment
    df["Delay_Treatment"] = df.groupby('Group_ID')['Participant_ID'].transform(
    lambda x: np.random.permutation(['High'] * 4 + ['Low'] * 4))

    #Initialize Valuation
    df['Valuation'] = np.where(
    df['Role'] == 'Buyer', 
    np.random.choice(buyer_valuations, size=len(df)), 
    0)

    #Add Matches for individual round
    df_with_matches = create_matches_for_rounds(df.copy())

    return df_with_matches

def round_or_fallback(value, fallback="No deal", precision=1):
    """This function rounds the value if it is not None, otherwise it returns the fallback value."""
    return round(value, precision) if value is not None else fallback



# Function to create match rounds
def create_matches_for_rounds(df: pd.DataFrame, num_rounds: int = 20) -> pd.DataFrame:
    """
    Creates columns for match rounds where each buyer is randomly matched with a seller from the same group.
    
    Parameters:
    - df: DataFrame containing participant IDs, group numbers, and roles.
    - num_rounds: Number of match rounds to create.
    
    Returns:
    - DataFrame with added columns for each match round.
    """

    # Create columns for each match round
    for round_num in range(1, num_rounds + 1):
        match_column_name = f'Match_Round_{round_num}'

        # Initialize the column with NaN
        df[match_column_name] = np.nan

        # Loop over each group
        for group, group_data in df.groupby('Group_ID'):
            # Get buyers and sellers within the group
            buyers = group_data[group_data['Role'] == 'Buyer']['Participant_ID'].tolist()
            sellers = group_data[group_data['Role'] == 'Seller']['Participant_ID'].tolist()

            # Randomly shuffle sellers to create random matches
            np.random.shuffle(sellers)

            # Assign matches to buyers and sellers
            for i in range(len(buyers)):
                # Match buyer with a seller
                df.loc[df['Participant_ID'] == buyers[i], match_column_name] = sellers[i]
                # Match seller with a buyer
                df.loc[df['Participant_ID'] == sellers[i], match_column_name] = buyers[i]
    
    return df


def create_participant_data(number_of_groups: int, buyer_valuations: List[List], seller_valuations: List[List], information_asymmetry: str, number_of_rounds: int = 20) -> pd.DataFrame:
    """
    Creates a dataframe with group assignments, roles treatments and valuations for each participant.

    Args:
        number_of_groups (int): The number of groups; each group consists of eight participants.
        buyer_valuations (List[List]): This is a list of four lists, each containing the 30  valuations of the buyers in a group.
        seller_valuations (List[List]): This is a list of four lists, each containing the 30  valuations of the sellers in a group.
    Returns:
        pd.Dataframe: A dataframe with group assignments.
        Columns:
        - Participant_ID: The unique ID of the participant.
        - Group_ID: The unique ID of the group.
    """

    # Initialize Participant Number
    participant_ids = list(range(1, 8 * number_of_groups + 1)) 
    df = pd.DataFrame({'Participant_ID': participant_ids})

    # Initialize Group ID's
    group_ids = np.repeat(range(1, number_of_groups + 1), 8)
    np.random.shuffle(group_ids)
    df['Group_ID'] = group_ids

    #Initialize Roles
    df["Role"] =  df.groupby('Group_ID')['Participant_ID'].transform(
    lambda x: np.random.permutation(['Seller'] * 4 + ['Buyer'] * 4))

    if information_asymmetry == "one-sided":
        # Initialize Valuations
        df['Valuation'] = [np.zeros(number_of_rounds).tolist()] * len(df)
        for group_id, group_data in df.groupby('Group_ID'):
            buyers_indices = group_data[group_data['Role'] == 'Buyer'].index
            for i, buyer_index in enumerate(buyers_indices):
                df.at[buyer_index, 'Valuation'] = buyer_valuations[i].tolist()

    elif information_asymmetry == "two-sided":
        # Initialize Valuations
        df['Valuation'] = [np.zeros(number_of_rounds).tolist()] * len(df)
        for group_id, group_data in df.groupby('Group_ID'):
            buyers_indices = group_data[group_data['Role'] == 'Buyer'].index
            for i, buyer_index in enumerate(buyers_indices):
                df.at[buyer_index, 'Valuation'] = buyer_valuations[i].tolist()
                
            sellers_indices = group_data[group_data['Role'] == 'Seller'].index
            for i, seller_index in enumerate(sellers_indices):
                df.at[seller_index, 'Valuation'] = seller_valuations[i].tolist()
  
    return df




def create_group_matrix_for_individual_round(group_dataframe: pd.DataFrame, random_seed = 40) -> List[List[int]]:
    """
    Creates a matrix of group assignments for each participant in a single round.
    Each match is unique, all matched participants are in the same group, 
    and a "Buyer" is matched with a "Seller".

    Args:
        group_dataframe (pd.DataFrame): A dataframe with group assignments for each participant,
                                        the ID of each participant, and their roles.

    Returns:
        List[List]: A matrix of group assignments for each participant in a single round.
    """
    # Set the random seed for reproducibility
    np.random.seed(random_seed)

    # Initialize the matrix to store the matches
    group_matrix = []

    # Iterate through each group in the dataframe
    for group_id, group_data in group_dataframe.groupby('Group_ID'):
        # Separate buyers and sellers within the group
        buyers = group_data[group_data['Role'] == 'Buyer']['Participant_ID'].tolist()
        sellers = group_data[group_data['Role'] == 'Seller']['Participant_ID'].tolist()

        # Shuffle the lists to create random matches
        np.random.shuffle(buyers)
        np.random.shuffle(sellers)

        # Pair each buyer with a seller
        for buyer, seller in zip(buyers, sellers):
            group_matrix.append([seller, buyer])  # Pair the seller with the buyer

    return group_matrix




def create_group_matrices_for_all_rounds(group_dataframe: pd.DataFrame, number_of_rounds: int = 20) -> List[List[List]]:
    """
    Creates a matrix of group assignments for each participant in all 20 rounds. It is of the following shape:  
    [[[1, 2],
     [5, 4],
     [3, 6],
      ...],
     [[1, 2],
     [5, 4],
     [3, 6],
      ...],
      ...].
      The requirements are that (1) each match of two participants is unique, (2) all matched participants are in the same group (3) a participant with the role "Buyer" is matched with a participant with the role "Seller".

    Args:
        group_dataframe (pd.DataFrame): A dataframe with group assignments for each participant, the id of each participant and the roles of the participants. 

    Returns:
        List[List[List]]: A matrix of group assignments for each participant in all rounds.
    """

    # Initialize a list to store the matrices for all rounds
    all_rounds_matrix = []

    # Create group assignments for 20 rounds
    for round_number in range(number_of_rounds):
        # Count the random seed upwards starting from 40
        random_seed = 40 + round_number

        # Generate the group matrix for the current round
        round_matrix = create_group_matrix_for_individual_round(group_dataframe, random_seed)

        # Append the matrix for the current round to the list
        all_rounds_matrix.append(round_matrix)

    return all_rounds_matrix



def is_valid_dataframe(obj, name_of_object: str) -> bool:
    """
    Checks if the given object is a valid pandas DataFrame.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is a valid DataFrame, False otherwise.
    """
    # Check if the object is an instance of pd.DataFrame
    if isinstance(obj, pd.DataFrame):
        # Additional checks to ensure the DataFrame is not empty and has columns
        if not obj.empty and obj.columns is not None:
            return True
        else:
            print(f"Error: The DataFrame {name_of_object} is empty or has no columns.")
            return False
    else:
        print(f"Error: The object {name_of_object} is not a DataFrame.")
        return False


def is_valid_list(obj, name_of_object: str) -> bool:
    """
    Checks if the given object is a valid pandas DataFrame.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is a valid DataFrame, False otherwise.
    """
    # Check if the object is an instance of pd.DataFrame
    if isinstance(obj, List):
 
            return True
    else:
        print(f"Error: The object {name_of_object} is not a List.")
        return False
    

def calculate_discount_factors_for_shrinking_pie(delay_treatment_high: bool, total_bargaining_time: int = 120) -> List[float]:
    """This function gives out the percentages of the gains of trade the players get for all values of time. 
    
    Args:
        delay_treatment_high (bool): Whether the delay treatment is high.
        total_bargaining_time (int): Total time in seconds for which the discount factors are to be calculated.

    Returns:
        List[float]: A list of discount factors for each second of the bargaining period.
    """

    discount_rate = 0.03 if delay_treatment_high else 0.01
    
    time_values = np.arange(0, total_bargaining_time + 1)

    discount_factors = 1 / (1 + discount_rate)**time_values

    return discount_factors.tolist()


def calculate_round_results(player: Any, practice_round: bool) -> Dict[str, Any]:
    """
    Returns the dictionary that the HTML page RoundResults.html needs to display the results of a round. 

    Args:
        player (Any): The player object containing the specific player's database.

    Returns:
        Dict[str, Any]: A dictionary containing the results of the round.
    """

    role_in_game = player.participant.vars['role_in_game']
    negative_deal_price = -player.group.field_maybe_none('deal_price') if player.group.field_maybe_none('deal_price') is not None else None

    if practice_round == True:
        other_role = "Buyer" if player.participant.vars['role_in_game'] == "Seller" else "Seller"
        round_number = player.round_number
    else:
        other_role = player.get_others_in_group()[0].participant.vars['role_in_game']
        round_number = player.round_number - 3

    if player.group.field_maybe_none('deal_price') is not None:
        if player.participant.vars['role_in_game'] == "Buyer":
            gains_from_trade = player.valuation - player.group.field_maybe_none('deal_price')
        else:
            gains_from_trade = player.group.field_maybe_none('deal_price') - player.valuation
    else:
        gains_from_trade = None

    return dict(
        deal_price=round_or_fallback(player.group.field_maybe_none('deal_price')),
        negative_deal_price=round_or_fallback(negative_deal_price),
        valuation=round_or_fallback(player.valuation),
        negative_valuation=round_or_fallback(-player.valuation),
        gains_from_trade=round_or_fallback(gains_from_trade),
        transaction_costs=round_or_fallback(player.cumulated_TA_costs),
        negative_transaction_costs=round_or_fallback(-player.cumulated_TA_costs),
        other_role=other_role,
        payoff=round_or_fallback(player.payoff),
        participation_fee=round_or_fallback(player.group.subsession.session.config['participation_fee']),
        payoff_plus_participation_fee=round_or_fallback(player.payoff + player.group.subsession.session.config['participation_fee']),
        TA_treatment = player.group.subsession.session.vars['TA_treatment'],
        round_number = round_number,
        practice_round = practice_round, 
        role_in_game = role_in_game
    )


def create_dictionary_with_html_variables_for_bargain_instructions(player: Any) -> Dict[str, Any]:
    """
    Creates a dictionary with the variables needed for the HTML page BargainInstructions.html.
    """

    termination_probability = 0.01 if player.group.subsession.session.config['termination_treatment'] == "low_prob" else 0.04
    termination_probability_in_percent = termination_probability * 100
    
    expected_termination_time = round(1 / termination_probability)

    transaction_costs = player.group.subsession.session.config['transaction_costs']

    transaction_costs_in_cents = round(transaction_costs * 100)

    player_role = player.participant.vars['role_in_game']

    minimum_payoff = player.group.subsession.session.config['minimum_payoff']

    return {'termination_probability_in_percent': termination_probability_in_percent, 
            'transaction_costs_in_cents': transaction_costs_in_cents, 
            'expected_termination_time': expected_termination_time,
            'player_role': player_role, 
            'minimum_payoff': minimum_payoff
            }



def create_payoff_dictionary(player: Any) -> Dict[str, Any]:
    """This function creates the dictionary that the HTML page FinalResults.html needs to display the results of the game. 

    Args:
        player (Any): The player object containing the specific player's database.

    Returns:
        Dict[str, Any]: A dictionary containing the results of the game.
    """
    # Get the randomly chosen round
    
    chosen_round = player.participant.random_round
    round_data = player.in_round(chosen_round)


    # Extract necessary values from the chosen round
    deal_price = round_data.group.field_maybe_none('deal_price')
    negative_deal_price = -deal_price if deal_price is not None else None
    transaction_costs = round_data.field_maybe_none('cumulated_TA_costs')
    negative_transaction_costs = -transaction_costs if transaction_costs is not None else None
    valuation = round_data.valuation
    negative_valuation = -valuation
    payoff = round_data.payoff
    participation_fee = round_data.group.subsession.session.config['participation_fee']
    payoff_plus_participation_fee = payoff + participation_fee
    is_finished = round_data.group.is_finished

    deal_accepted_by = round_data.group.field_maybe_none('accepted_by')

    if deal_price is not None:
        if player.participant.vars['role_in_game'] == "Buyer":
            gains_from_trade = valuation - deal_price
        else:
            gains_from_trade = deal_price - valuation
    else:
        loss_from_discounting = None
        negative_loss_from_discounting = None
        gains_from_trade = None
        discounted_gains_from_trade = None

    return dict(
        deal_price=round_or_fallback(deal_price),
        negative_deal_price=round_or_fallback(negative_deal_price),
        valuation=round_or_fallback(valuation),
        negative_valuation=round_or_fallback(negative_valuation),
        gains_from_trade=round_or_fallback(gains_from_trade),
        transaction_costs=round_or_fallback(transaction_costs),
        negative_transaction_costs=round_or_fallback(negative_transaction_costs),
        payoff=round_or_fallback(payoff),
        participation_fee=round_or_fallback(participation_fee),
        payoff_plus_participation_fee=round_or_fallback(payoff_plus_participation_fee),
        is_finished=is_finished,
        terminated= round_data.group.terminated,
        deal_accepted_by=deal_accepted_by,
        chosen_round=chosen_round,
        TA_treatment = round_data.group.subsession.session.vars['TA_treatment']
    )

def draw_termination_times(number_of_rounds: int, probability_of_termination: float) -> List[int]:
    """
    Draws the termination times for the given number of rounds and probability of termination from a geometric distribution.

    Args:
        number_of_rounds (int): The number of rounds.
        probability_of_termination (float): The probability of termination for each round.

    Returns:
        List[int]: A list of termination times in seconds.

    """

    termination_times = []
    for i in range(number_of_rounds):
        np.random.seed(42 + i)
        termination_time = np.random.geometric(probability_of_termination)
        termination_times.append(termination_time)

    return termination_times


def create_dictionary_with_html_variables_for_bargain_page(player: Any, 
                                                      practice_round: bool = False) -> Dict[str, Any]:
    """
    Creates a dictionary with the variables needed for the HTML page Bargain.html.

    Args:
        player (Any): The player object containing the specific player's database.
        practice_round (bool): Whether this is a practice round. Defaults to False.

    Returns:
        Dict[str, Any]: A dictionary containing the variables needed for the HTML page Bargain.html.
    """
    
    dictionary = {}
    
    dictionary['my_role'] = player.participant.vars['role_in_game']
    dictionary['role_in_game'] = player.participant.vars['role_in_game']
    dictionary['valuation'] = player.valuation
    dictionary['information_asymmetry'] = player.group.subsession.session.config['information_asymmetry']
    dictionary['TA_treatment'] = player.group.subsession.session.vars['TA_treatment']

    if practice_round == False:
        dictionary['other_valuation'] = player.get_others_in_group()[0].valuation
        dictionary['other_role'] = player.get_others_in_group()[0].participant.vars['role_in_game']
        dictionary['practice_round'] = False
        dictionary['round_number'] = player.round_number - 3
    else:
        dictionary['practice_round'] = True
        dictionary['round_number'] = player.round_number 
        if player.participant.vars['role_in_game'] == "Buyer":
            dictionary['other_role'] = "Seller"
            dictionary['other_valuation'] = 0
        else:
            dictionary['other_role'] = "Buyer"


    if player.group.subsession.session.config['termination_treatment'] == 'high_prob':
        dictionary['termination_probability'] = 4
    else:
        dictionary['termination_probability'] = 1

    return dictionary


def create_dictionary_with_js_variables_for_bargain_page(player: Any, C: Any, practice_round: bool = False, language_code: str = 'en') -> Dict[str, Any]:
    """
    Creates a dictionary with the variables needed for the JavaScript page Bargain.html.

    Args:
        player (Any): The player object containing the specific player's database.

    Returns:
        Dict[str, Any]: A dictionary containing the variables needed for the JavaScript page Bargain.html.
    """
    dictionary = {}
    
    dictionary['my_id'] = player.id_in_group
    dictionary['start_time'] = player.group.bargain_start_time
    dictionary['my_role'] = player.participant.vars['role_in_game']
    dictionary['my_valuation'] = player.valuation
    dictionary['information_asymmetry'] = player.group.subsession.session.config['information_asymmetry']
    dictionary['maximum_bargain_time'] = C.TOTAL_BARGAINING_TIME
    dictionary['x_values_TA_graph'] = json.loads(player.x_axis_values_TA_graph)
    dictionary['y_axis_maximum_TA_graph'] = player.y_axis_maximum_TA_graph
    dictionary['TA_treatment'] = player.group.subsession.session.vars['TA_treatment']

    if practice_round == False:
        dictionary['other_id'] = player.get_others_in_group()[0].id_in_group
        dictionary['other_valuation'] = player.get_others_in_group()[0].valuation
        dictionary['other_role'] = player.get_others_in_group()[0].participant.vars['role_in_game']

    if practice_round == True:
        if player.participant.vars['role_in_game'] == "Buyer":
            dictionary['other_valuation'] = 0
        else:
            dictionary['other_valuation'] = np.nan

    dictionary["language_code"] = language_code

    return dictionary


def update_broadcast_dict_based_on_actions(broadcast: Dict, data: Dict[str, Any], player: Any, group: Any, practice_round: bool = False):
    """
    Updates the broadcast dictionary based on the actions of the players.

    Args:
        broadcast (Dict): The broadcast dictionary.
        data (Dict[str, Any]): The data dictionary.
        player (Any): The player object.
        group (Any): The group object.

    Returns:
        Dict: The updated broadcast dictionary.
    """


    # Update database and broadcast if a proposal was made
    if data.get('type') == 'propose':

        if player.id_in_group == data.get('proposal_by_id'):

            update_player_database_with_proposal(
                player=player,
                data=data
            )

        if data.get("proposal_by_role") == "Seller":


            group.current_seller_offer = data.get('amount')
            broadcast["seller_proposal"] = data.get('amount')
            broadcast["notification_seller_proposal"] = True 

            if group.field_maybe_none('current_buyer_offer') is not None and player.current_amount_proposed < group.field_maybe_none('current_buyer_offer'):

                treat_seller_offer_lower_than_buyer_as_acceptance(
                    broadcast=broadcast, 
                    player=player, 
                    group=group, 
                    data=data
                )

            return broadcast
        
        elif data.get("proposal_by_role") == "Buyer":

            
            group.current_buyer_offer = data.get('amount')    
            broadcast["buyer_proposal"] = data.get('amount')
            broadcast["notification_buyer_proposal"] = True 


            if group.field_maybe_none('current_seller_offer') is not None and group.field_maybe_none('current_seller_offer') < player.current_amount_proposed:

                treat_buyer_offer_larger_than_seller_as_acceptance(
                    broadcast=broadcast, 
                    player=player, 
                    group=group, 
                    data=data
                )

                return broadcast

    # Update database and finish bargaining if a deal was accepted
    elif data.get('type') == 'accept':

        update_group_database_upon_acceptance(
            group=group, 
            data=data
        )

        group.is_finished = True
        broadcast["finished"] = True

    # Update database and finish bargaining if a deal was terminated
    elif data.get('terminated_by'):

        update_group_database_upon_termination(
            group=group,
            data=data
        )

        group.is_finished = True  # This ensures no error is thrown
        broadcast["finished"] = True

    # Update database and finish bargaining if random termination time is reached
    bargaining_time_elapsed = round(time.time() - group.bargain_start_time)

    if bargaining_time_elapsed >= group.random_termination_time_current_round:

        update_group_database_upon_random_termination(
            group=group
        )

        group.is_finished = True
        broadcast["finished"] = True

    #Update broadcast if offers were already sent so that the client updates the payoffs (which change every second because of the transaction costs)
    if group.field_maybe_none('current_seller_offer'):

        broadcast.setdefault("seller_proposal", group.current_seller_offer)

    if group.field_maybe_none('current_buyer_offer'):

        broadcast.setdefault("buyer_proposal", group.current_buyer_offer)

    return broadcast



def write_bot_giving_offer_and_improving(broadcast: Dict, data: Dict[str, Any], player: Any, group: Any, initial_offer_from_bot: float, bargaining_time_elapsed: int, improvement_factor: float = 1.2):
    """
    Writes the simple bot logic. The bot gives the offer after 5 seconds and improves the offer by 105 every 10 seconds. THis means, if the player is a buyer, the offer will decrease, if the player is a seller, the offer will increase.

    Args:
        broadcast (Dict): The broadcast dictionary.
        data (Dict[str, Any]): The data dictionary.
        player (Any): The player object.
        group (Any): The group object.
        offer_from_bot (float): The offer from the bot.
        bargaining_time_elapsed (int): The bargaining time elapsed.

    Returns:
        Dict: The updated broadcast dictionary.
    """

    # Bot gives initial offer after 10 seconds
    if np.isclose(bargaining_time_elapsed, 10, atol=1):
        set_bot_offer(broadcast=broadcast, 
                      player=player, 
                      group=group, 
                      offer_from_bot=initial_offer_from_bot)
        
    #Calculate the nearest 10 seconde
    nearest_round_second = round(bargaining_time_elapsed / 10) * 10

    # Bot improves offer every 10 seconds after the initial offer
    if abs(bargaining_time_elapsed - nearest_round_second) <= 1 and nearest_round_second > 10:

        improvement_index = nearest_round_second // 10 - 1 

        print(f"improvement_index: {improvement_index}")

        if player.participant.vars['role_in_game'] == "Buyer":
            new_offer = round(initial_offer_from_bot / (improvement_factor ** improvement_index))
            set_bot_offer(broadcast=broadcast, 
                          player=player, 
                          group=group, 
                          offer_from_bot=new_offer)
        else:  # player is Seller
            new_offer = round(initial_offer_from_bot * (improvement_factor ** improvement_index))
            set_bot_offer(broadcast=broadcast, 
                          player=player, 
                          group=group, 
                          offer_from_bot=new_offer)

    return broadcast


def write_bot_giving_offer_and_accepting_the_second_offer(broadcast: Dict, data: Dict[str, Any], player: Any, group: Any, initial_offer_from_bot: float, bargaining_time_elapsed: int, amount_proposed_list: List[float]):
    """
    Writes the bot logic. The bot gives the offer after 10 seconds and accepts the second offer.

    Args:
        broadcast (Dict): The broadcast dictionary.
        data (Dict[str, Any]): The data dictionary.
        player (Any): The player object.
        group (Any): The group object.
        offer_from_bot (float): The offer from the bot.

    Returns:
        Dict: The updated broadcast dictionary.
    """

    # Bot gives initial offer after 10 seconds
    if np.isclose(bargaining_time_elapsed, 10, atol=1):
        set_bot_offer(broadcast=broadcast, 
                      player=player, 
                      group=group, 
                      offer_from_bot=initial_offer_from_bot)
        
    #bot accepts the second offer
    if len(amount_proposed_list) == 2:
    
        print("bot accepts the second offer")
        if player.participant.vars['role_in_game'] == "Buyer":
            accept_deal_as_bot(broadcast=broadcast, 
                            player=player, 
                            group=group,
                            data=data)
        else:  # player is Seller
            accept_deal_as_bot(broadcast=broadcast, 
                            player=player, 
                            group=group,
                            data=data)

    return broadcast


def accept_deal_as_bot(broadcast: Dict, player: Any, group: Any, data: Dict[str, Any]) -> None:
    """
    Accepts the deal as the bot.

    Args:
        broadcast (Dict): The broadcast dictionary.
        player (Any): The player object.
        group (Any): The group object.
    """

    data['type'] = 'accept'
    data['proposal_by_role'] = player.participant.vars['role_in_game']
    data['proposal_by_id'] = player.id_in_group
    data['amount'] = player.current_amount_proposed 
    data['acceptance_time'] = round(time.time() - group.bargain_start_time)
    data['accepted_by'] = player.id_in_group + 1

    update_group_database_upon_acceptance(
        group=group, 
        data=data
    )

    broadcast["finished"] = True
    group.is_finished = True




    


    



def set_bot_offer(broadcast: Dict, player: Any, group: Any, offer_from_bot: float) -> Dict:
    """
    Handles the bot's initial offer after 10 seconds.

    Args:
        broadcast (Dict): The broadcast dictionary.
        player (Any): The player object.
        group (Any): The group object.
        offer_from_bot (float): The offer from the bot.

    Returns:
        Dict: The updated broadcast dictionary.
    """
    if player.participant.vars['role_in_game'] == "Buyer":
        broadcast["seller_proposal"] = offer_from_bot
        broadcast["notification_seller_proposal"] = True
        group.current_seller_offer = offer_from_bot
    else:  # player is Seller
        broadcast["buyer_proposal"] = offer_from_bot
        broadcast["notification_buyer_proposal"] = True
        group.current_buyer_offer = offer_from_bot
    
    return broadcast


def create_list_with_termination_probabilities_from_geometric_distribution(number_of_seconds: int, probability_of_termination: float) -> List[float]:
    """
    Args:
        number_of_seconds (int): The number of seconds.
        probability_of_termination (Boolean): The probability of termination (high_prob or low_prob)

    Returns:
        List[float]: A list with the termination probabilities.

    """
    if probability_of_termination == "high_prob":
        probability = 0.04
    else:
        probability = 0.01

    # Create an array of time points
    time_points = np.arange(1, number_of_seconds + 1)
    
    # Calculate the cumulative probabilities
    cumulative_probabilities = 1 - (1 - probability) ** time_points
    
    return cumulative_probabilities.tolist()




def treat_buyer_offer_larger_than_seller_as_acceptance(broadcast: Dict, player: Any, group: Any, data: Dict[str, Any]) -> None:
    """
    Treats the buyer's offer as acceptance if it is larger than the seller's offer.

    Args:
        broadcast (Dict): The broadcast dictionary.
        player (Any): The player object.
        group (Any): The group object.
        data (Dict[str, Any]): The data dictionary.
    """

    data['type'] = 'accept'
    data['proposal_by_role'] = player.participant.vars['role_in_game']
    data['proposal_by_id'] = player.id_in_group
    data['amount'] = group.current_seller_offer
    data['acceptance_time'] = round(time.time() - group.bargain_start_time)
    data['accepted_by'] = player.id_in_group

    group.deal_price = float(re.sub(r'[^\d.]', '', str(group.current_seller_offer))) # This converts e.g. "$1.10" into 1.10, and ensures that it also works for the practice rounds where amount is a float.
    group.acceptance_time = data.get('acceptance_time')
    group.accepted_by = data.get('accepted_by')

    broadcast["finished"] = True
    group.is_finished = True

 


def treat_seller_offer_lower_than_buyer_as_acceptance(broadcast: Dict, player: Any, group: Any, data: Dict[str, Any]) -> None:
    """
    Treats the seller's offer as acceptance if it is lower than the buyer's offer.
    """

    data['type'] = 'accept'
    data['proposal_by_role'] = player.participant.vars['role_in_game']
    data['proposal_by_id'] = player.id_in_group
    data['amount'] = group.current_buyer_offer
    data['acceptance_time'] = round(time.time() - group.bargain_start_time)
    data['accepted_by'] = player.id_in_group

    group.deal_price = float(re.sub(r'[^\d.]', '', str(group.current_buyer_offer))) # This converts e.g. "$1.10" into 1.10, and ensures that it also works for the practice rounds where amount is a float.
    group.acceptance_time = data.get('acceptance_time')
    group.accepted_by = data.get('accepted_by')

    broadcast["finished"] = True
    group.is_finished = True


