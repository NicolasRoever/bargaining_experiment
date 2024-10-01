from typing import List, Tuple, Any, Dict
import pandas as pd
import json
import time
import re
import numpy as np
import random
import math

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


def cumulative_transaction_cost_function(time: float, cost_factor: float, decay_factor: float) -> float:
    """This function spells out the cumulative transaction cost function dependent on time"""

    cumulative_transaction_cost = cost_factor * ((1-np.exp(-decay_factor*time)) / decay_factor) 

    return cumulative_transaction_cost


def calculate_transaction_costs(TA_treatment_high: bool, delay_treatment_high: bool, total_bargaining_time: int) -> Tuple[List[float], List[float]]:
    """
    Calculate the cumulative costs over time with a decay factor depending on the treatment andotre
    compute the differences between each consecutive cost.

    Args:
        TA_treatment_high (bool): Whether the treatment for Transactional Adjustment is high.
        total_bargaining_time (int): Total time in seconds for which the costs are to be calculated.

    Returns:
        Tuple[List[float], List[float]]: 
        - A list of cumulative costs at each second.
        - A list of differences between each second's cost and the next.
    """
    
    cost_factor = 0.375 if TA_treatment_high else 0.125
    
    decay_factor = 0.035 if delay_treatment_high else 0.01

    time_values = np.arange(0, total_bargaining_time + 1)

    cumulative_costs = cumulative_transaction_cost_function(time_values, cost_factor, decay_factor)

    # Calculate the differences between each second's cost and the next
    cost_differences = np.append(np.diff(cumulative_costs), 0)

    return cumulative_costs.tolist(), cost_differences.tolist() 


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
    total_cost_y_values = json.loads(player.total_costs_list)[0:bargaining_time_elapsed]
    total_delay_y_values = json.loads(player.total_delay_list)[0:bargaining_time_elapsed]
    current_transaction_costs = json.loads(player.current_costs_list)[bargaining_time_elapsed - 1]
    current_discount_factor = json.loads(player.discount_factors_list)[bargaining_time_elapsed]


    # Update player attributes
    #The if clause ensures that we do not get an error for period 0.
    if total_cost_y_values:

        player.current_TA_costs = current_transaction_costs
        player.cumulated_TA_costs = total_cost_y_values[-1]
        player.current_payoff_terminate = -player.cumulated_TA_costs
        player.payment_delay = total_delay_y_values[-1]
        player.current_discount_factor = current_discount_factor

    

    # Update the broadcast dictionary with the new values individually
    broadcast['current_TA_costs'] = player.field_maybe_none('current_TA_costs')
    broadcast['cumulated_TA_costs'] = player.field_maybe_none('cumulated_TA_costs')
    broadcast['current_payoff_terminate'] = player.field_maybe_none('current_payoff_terminate')
    broadcast['payment_delay'] = player.field_maybe_none('payment_delay')   
    broadcast['bargaining_time_elapsed'] = bargaining_time_elapsed
    broadcast['total_cost_y_values'] = total_cost_y_values
    broadcast['total_delay_y_values'] = total_delay_y_values
    broadcast['x_axis_values_TA_graph'] = json.loads(player.x_axis_values_TA_graph)
    broadcast['x_axis_values_delay_graph'] = json.loads(player.x_axis_values_delay_graph)
    broadcast['current_transaction_costs'] = current_transaction_costs
    broadcast['current_discount_factor'] = current_discount_factor

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
    player.proposal_made = True


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
        valuation_list = list(range(1, 101, 1))
        player.valuation = random.choice(valuation_list)


def setup_player_transaction_costs(player: Any, ta_treatment: bool, delay_treatment: bool, total_bargaining_time) -> None:
    """This function sets up the player's transaction costs based on the treatment. and saves the data in the player database.

    Args:
        player: The player object containing the specific player's database.
        ta_treatment: The treatment for Transaction Costs
        total_bargaining_time: The total time for bargaining in seconds.

    Returns:
        None
    """

    #Calculate Transacion Costs
    transaction_cost_list, current_costs_list = calculate_transaction_costs(
    TA_treatment_high=ta_treatment, 
    delay_treatment_high=delay_treatment,
    total_bargaining_time=total_bargaining_time)


    #Save all values relevant for displaying transaction costs in the database
    player.total_costs_list = json.dumps(transaction_cost_list)
    player.current_costs_list = json.dumps(current_costs_list)
    player.x_axis_values_TA_graph = json.dumps(list(range(0, total_bargaining_time + 1)))
    player.y_axis_maximum_TA_graph = transaction_cost_list[-1]


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
        discount_factor = player.current_discount_factor #Recall that this is a percentage of the money to keee.

        if player.role == "Seller":
            player.payoff = (player.group.deal_price - player.valuation) * discount_factor - transaction_costs


        elif player.role == "Buyer":
            player.payoff = (player.valuation - player.group.deal_price) * discount_factor - transaction_costs


    #Case 2: A deal was terminated
    elif player.group.field_maybe_none('termination_time'):

        transaction_costs = player.cumulated_TA_costs
        player.payoff = -transaction_costs
        print(player.payoff)

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

        player.group.bargain_duration = player.group.acceptance_time

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
    player.participant.payoff = player.in_round(player.participant.random_round).payoff



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



# Function to create match rounds
def create_matches_for_rounds(df, num_rounds=20):
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


def create_participant_data(number_of_groups: int, buyer_valuations: List[List]) -> pd.DataFrame:
    """
    Creates a dataframe with group assignments, roles treatments and valuations for each participant.

    Args:
        number_of_groups (int): The number of groups; each group consists of eight participants.
        buyer_valuations (List[List]): This is a list of four lists, each containing the 20  valuations of the buyers in a group.

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

    # Initialize Valuations
    df['Valuation'] = [np.zeros(20).tolist()] * len(df)
    for group_id, group_data in df.groupby('Group_ID'):
        buyers_indices = group_data[group_data['Role'] == 'Buyer'].index
        for i, buyer_index in enumerate(buyers_indices):
            df.at[buyer_index, 'Valuation'] = buyer_valuations[i].tolist()
        
  
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




def create_group_matrices_for_all_rounds(group_dataframe: pd.DataFrame) -> List[List[List]]:
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
    for round_number in range(20):
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

