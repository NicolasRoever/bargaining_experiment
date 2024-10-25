import pytest
import pandas as pd
import numpy as np
from typing import List, Tuple
from unittest.mock import Mock

from bargain_live.bargaining_functions import calculate_total_delay_list, calculate_transaction_costs, create_matches_for_rounds, create_random_values_dataframe, create_participant_data, create_group_matrix_for_individual_round, create_group_matrices_for_all_rounds, cumulative_transaction_cost_function, calculate_discount_factors_for_shrinking_pie, record_player_payoff_from_round, draw_termination_times, create_list_with_termination_probabilities_from_geometric_distribution


#-------------------------
# Test cases for calculate_total_delay_list

@pytest.mark.parametrize("bargaining_time, delay_multiplier, expected", [
    # Test case 1: Simple case with a small bargaining time and delay multiplier
    (5, 0.1, [0.1, 0.2, 0.3, 0.4, 0.5]),
    
    # Test case 2: Different values
    (3, 0.5, [0.5, 1.0, 1.5]),

    # Test case 3: No delay multiplier
    (4, 0.0, [0.0, 0.0, 0.0, 0.0]),

    # Test case 4: Single time step
    (1, 2.0, [2.0]),

    # Test case 5: Larger delay multiplier
    (3, 1.5, [1.5, 3.0, 4.5])
])
def test_calculate_total_delay_list(bargaining_time: int, delay_multiplier: float, expected: List[float]):
    # Act: Call the function with the test data
    actual = calculate_total_delay_list(bargaining_time, delay_multiplier)

    # Assert: Check if the actual result matches the expected result
    assert actual == pytest.approx(expected, rel=1e-9), f"Expected {expected}, but got {actual}"


#-------------------------
# Test cases for cumulative_transaction_cost_function

def test_cumulative_transaction_cost():
    time = 120
    cost_factor = 0.375
    decay_factor = 0.035

    expected_cost = 10.565

    actual_result = cumulative_transaction_cost_function(time, cost_factor, decay_factor)

    # Assert the result is close to the expected value
    assert np.isclose(expected_cost, actual_result, atol=1e-2)



#-------------------------
# Test cases for calculate_transaction_costs

@pytest.mark.parametrize("TA_treatment_high, total_bargaining_time, expected_cumulative, expected_differences", [
    # Test case 1: High treatment, short time
    (True, 5, 
     [0, 0.2475, 0.2475, 0.492525, 0.492525], 
     [0.12375, 0.1225125, 0.1225125, 0, 0]),

])

def test_calculate_transaction_costs(TA_treatment_high: bool, total_bargaining_time: int, 
                                     expected_cumulative: List[float], 
                                     expected_differences: List[float]):
    
    # Act: Call the function with the test data
    actual_cumulative, actual_differences = calculate_transaction_costs(TA_treatment_high, total_bargaining_time)

    # Assert: Check if the actual result matches the expected result
    assert actual_cumulative == pytest.approx(expected_cumulative, rel=1e-1), "Cumulative costs do not match"
    assert actual_differences == pytest.approx(expected_differences, rel=1e-1), "Cost differences do not match"


#-------------------------
# Test cases for create_matches_for_rounds

# Sample dataframe for testing
@pytest.fixture
def sample_dataframe():
    data = {
        'Participant_ID': range(1, 17),
        'Group_ID': [2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2],
        'Role': ['Seller', 'Seller', 'Buyer', 'Seller', 'Buyer', 'Buyer', 'Seller', 'Buyer', 
                 'Seller', 'Seller', 'Buyer', 'Buyer', 'Buyer', 'Seller', 'Buyer', 'Seller']
    }
    return pd.DataFrame(data)


def test_create_match_rounds_correct_columns(sample_dataframe):
    # Test that the correct number of match round columns is created
    result_df = create_matches_for_rounds(sample_dataframe.copy(), num_rounds=20)
    expected_columns = [f'Match_Round_{i}' for i in range(1, 21)]
    assert all(col in result_df.columns for col in expected_columns), "Not all match round columns are present."

def test_create_match_rounds_valid_matching(sample_dataframe):
    # Test that all matches are valid between buyers and sellers within the same group
    result_df = create_matches_for_rounds(sample_dataframe.copy(), num_rounds=20)
    for round_num in range(1, 21):
        match_column = f'Match_Round_{round_num}'
        for group, group_data in result_df.groupby('Group_ID'):
            buyers = group_data[group_data['Role'] == 'Buyer']['Participant_ID'].tolist()
            sellers = group_data[group_data['Role'] == 'Seller']['Participant_ID'].tolist()
            matched_buyers = group_data[group_data['Role'] == 'Buyer'][match_column].tolist()
            matched_sellers = group_data[group_data['Role'] == 'Seller'][match_column].tolist()
            assert set(matched_buyers).issubset(set(sellers)), f"Invalid buyer matches in round {round_num} for group {group}."
            assert set(matched_sellers).issubset(set(buyers)), f"Invalid seller matches in round {round_num} for group {group}."

def test_create_match_rounds_unique_matching(sample_dataframe):
    # Test that each buyer and seller is matched uniquely within each round
    result_df = create_matches_for_rounds(sample_dataframe.copy(), num_rounds=20)
    for round_num in range(1, 21):
        match_column = f'Match_Round_{round_num}'
        for group, group_data in result_df.groupby('Group_ID'):
            matches = group_data[match_column].tolist()
            assert len(matches) == len(set(matches)), f"Duplicate matches found in round {round_num} for group {group}."

def test_create_match_rounds_consistent_participants(sample_dataframe):
    # Test that the number of participants remains the same after creating match rounds
    initial_participants = sample_dataframe['Participant_ID'].tolist()
    result_df = create_matches_for_rounds(sample_dataframe.copy(), num_rounds=20)
    final_participants = result_df['Participant_ID'].tolist()
    assert initial_participants == final_participants, "The number of participants changed after creating match rounds."

    
#-------------------------
# Test cases for create_random_values_dataframe

# Sample test data for testing
@pytest.fixture
def buyer_valuations():
    # Create a sample series of buyer valuations
    return pd.Series(np.random.uniform(0, 100, 1000))  # Example with 1000 buyer valuations

@pytest.fixture
def number_of_groups():
    # Set the number of groups for testing
    return 2  # Example with 5 groups

def test_correct_number_of_participants(number_of_groups, buyer_valuations):
    # Test that the dataframe has the correct number of participants
    df = create_random_values_dataframe(number_of_groups, buyer_valuations)
    expected_number_of_participants = number_of_groups * 8
    assert len(df) == expected_number_of_participants, "The number of participants is incorrect."

def test_half_buyers_half_sellers_per_group(number_of_groups, buyer_valuations):
    # Test that each group has exactly 4 buyers and 4 sellers
    df = create_random_values_dataframe(number_of_groups, buyer_valuations)
    for group_id, group_data in df.groupby('Group_ID'):
        buyers = group_data[group_data['Role'] == 'Buyer']
        sellers = group_data[group_data['Role'] == 'Seller']
        assert len(buyers) == 4, f"Group {group_id} does not have 4 buyers."
        assert len(sellers) == 4, f"Group {group_id} does not have 4 sellers."

def test_correct_valuations_assignment(number_of_groups, buyer_valuations):
    # Test that buyers have valuations from the buyer_valuations and sellers have valuation 0
    df = create_random_values_dataframe(number_of_groups, buyer_valuations)
    for index, row in df.iterrows():
        if row['Role'] == 'Buyer':
            assert row['Valuation'] in buyer_valuations.values, "Buyer has an incorrect valuation."
        elif row['Role'] == 'Seller':
            assert row['Valuation'] == 0, "Seller does not have a valuation of 0."

def test_match_round_columns_exist(number_of_groups, buyer_valuations):
    # Test that the match round columns exist and are correctly named
    df = create_random_values_dataframe(number_of_groups, buyer_valuations)
    match_round_columns = [f'Match_Round_{i}' for i in range(1, 21)]
    for col in match_round_columns:
        assert col in df.columns, f"{col} column is missing in the dataframe."

def test_correct_transaction_costs_and_delay_treatments(number_of_groups, buyer_valuations):
    # Test that the transaction costs and delay treatments are correctly assigned
    df = create_random_values_dataframe(number_of_groups, buyer_valuations)
    for group_id, group_data in df.groupby('Group_ID'):
        high_treatment = group_data['TA_Treatment'].tolist().count('High')
        low_treatment = group_data['TA_Treatment'].tolist().count('Low')
        high_delay = group_data['Delay_Treatment'].tolist().count('High')
        low_delay = group_data['Delay_Treatment'].tolist().count('Low')
        assert high_treatment == 4 and low_treatment == 4, f"Incorrect TA_Treatment distribution in group {group_id}."
        assert high_delay == 4 and low_delay == 4, f"Incorrect Delay_Treatment distribution in group {group_id}."


#-------------------------
# Test cases for create_participant_data

@pytest.fixture
def buyer_valuations():
    buyer_valuations = [
        np.arange(1, 21),
        np.arange(21, 41),
        np.arange(41, 61),
        np.arange(61, 81)
    ]
    return buyer_valuations


def test_correct_number_of_participants(number_of_groups, buyer_valuations):
    # Test that the dataframe has the correct number of participants
    df = create_participant_data(number_of_groups, buyer_valuations)
    expected_number_of_participants = number_of_groups * 8
    assert len(df) == expected_number_of_participants, "The number of participants is incorrect."

def test_half_buyers_half_sellers_per_group(number_of_groups, buyer_valuations):
    # Test that each group has exactly 4 buyers and 4 sellers
    df = create_participant_data(number_of_groups, buyer_valuations)
    for group_id, group_data in df.groupby('Group_ID'):
        buyers = group_data[group_data['Role'] == 'Buyer']
        sellers = group_data[group_data['Role'] == 'Seller']
        assert len(buyers) == 4, f"Group {group_id} does not have 4 buyers."
        assert len(sellers) == 4, f"Group {group_id} does not have 4 sellers."

def test_unique_group_assignments(number_of_groups, buyer_valuations):
    # Test that each participant is uniquely assigned to a group
    df = create_participant_data(number_of_groups, buyer_valuations)
    assert df['Group_ID'].nunique() == number_of_groups, "The number of unique groups is incorrect."

def test_buyer_valuations(number_of_groups, buyer_valuations):

    np.random.seed(0)

    expected_result = pd.DataFrame({
         'Participant_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'Group_ID': [1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2],
        'Role': ['Buyer', 'Seller', 'Seller', 'Buyer', 
    'Buyer', 'Seller', 'Buyer', 'Buyer', 
    'Seller', 'Buyer', 'Buyer', 'Seller', 
    'Seller', 'Buyer', 'Seller', 'Seller'],
        'Valuation':[
             np.arange(1, 21).tolist(),           # [1, 2, 3, ..., 20]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.arange(1, 21).tolist(),           # [1, 2, 3, ..., 20]
    np.arange(21, 41).tolist(),          # [21, 22, ..., 40]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.arange(21, 41).tolist(),          # [21, 22, ..., 40]
    np.arange(41, 61).tolist(),          # [41, 42, ..., 60]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.arange(41, 61).tolist(),          # [41, 42, ..., 60]
    np.arange(61, 81).tolist(),          # [61, 62, ..., 80]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.arange(61, 81).tolist(),          # [61, 62, ..., 80]
    np.zeros(20).tolist(),               # [0.0, 0.0, ..., 0.0]
    np.zeros(20).tolist()    

        ]})
    
    actual_result = create_participant_data(number_of_groups, buyer_valuations)


    pd.testing.assert_frame_equal(actual_result, expected_result, check_dtype=False)

#-------------------------
# Test cases for create_group_matrix_for_individual_round


@pytest.fixture
def sample_input():
    return pd.DataFrame({
        'Participant_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'Group_ID': [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
        'Role': ['Seller', 'Seller', 'Buyer', 'Buyer', 'Seller', 'Seller', 'Buyer', 'Buyer',
                 'Seller', 'Seller', 'Buyer', 'Buyer', 'Seller', 'Seller', 'Buyer', 'Buyer'],
    })

def test_create_group_matrix_for_individual_round_for_sample_seed(sample_input):

    expected_output = [
        [6, 8], [2, 3], [5, 4], [1, 7], [9, 16], [10, 12], [13, 15], [14, 11]
    ]

    actual_output = create_group_matrix_for_individual_round(sample_input, random_seed=40)

    assert actual_output == expected_output, "The group matrix is incorrect."

@pytest.mark.parametrize("seed", [10, 20, 30, 40, 50])
def test_unique_matches(sample_input, seed):
    # Test that each match of two participants is unique
    matrix = create_group_matrix_for_individual_round(sample_input, random_seed=seed)
    unique_pairs = set(tuple(sorted(pair)) for pair in matrix)
    assert len(unique_pairs) == len(matrix), f"Each match should be unique for seed {seed}."

@pytest.mark.parametrize("seed", [10, 20, 30, 40, 50])
def test_same_group(sample_input, seed):
    # Test that all matched participants are in the same group
    matrix = create_group_matrix_for_individual_round(sample_input, random_seed=seed)
    group_dict = sample_input.set_index('Participant_ID')['Group_ID'].to_dict()
    for seller, buyer in matrix:
        assert group_dict[seller] == group_dict[buyer], f"All matched participants should be in the same group for seed {seed}."

@pytest.mark.parametrize("seed", [10, 20, 30, 40, 50])
def test_buyer_seller_match(sample_input, seed):
    # Test that a buyer is matched with a seller
    matrix = create_group_matrix_for_individual_round(sample_input, random_seed=seed)
    role_dict = sample_input.set_index('Participant_ID')['Role'].to_dict()
    for seller, buyer in matrix:
        assert role_dict[seller] == 'Seller', f"Seller in match is not correct for seed {seed}."
        assert role_dict[buyer] == 'Buyer', f"Buyer in match is not correct for seed {seed}."

@pytest.mark.parametrize("seed", [10, 20, 30, 40, 50])
def test_number_of_matches(sample_input, seed):
    # Test that the number of matches is correct (4 matches per group, total of 8 matches for 2 groups)
    matrix = create_group_matrix_for_individual_round(sample_input, random_seed=seed)
    assert len(matrix) == 8, f"Number of matches should be 8 for seed {seed}."





#-------------------------
# Test cases for create_group_matrices_for_all_rounds


def test_round_2_different_from_round_1(sample_input):
    # Generate the group matrix for all rounds
    all_rounds_matrix = create_group_matrices_for_all_rounds(sample_input)

    # Get the matrices for round 1 and round 2
    round_1_matrix = all_rounds_matrix[0]
    round_2_matrix = all_rounds_matrix[1]

    # Check that the matrix for round 2 is different from round 1
    assert round_1_matrix != round_2_matrix, "The group matrix for round 2 should be different from round 1."


#-------------------------
# Test cases for calculate_discount_factors_for_shrinking_pie

@pytest.mark.parametrize("t, expected", [
    (0, 1),
    (30, 0.7397),
    (60, 0.547),
    (120, 0.2993)
])
def test_calculate_discount_factors_low_at_t(t, expected):
    # Set up test parameters
    total_bargaining_time = 120

    # Test when delay_treatment_high = True
    discount_factors_high = calculate_discount_factors_for_shrinking_pie(False, total_bargaining_time)
    
    # Test the value at the given time t
    assert np.isclose(discount_factors_high[t], expected, atol=1e-2), f"Expected {expected} at t={t}, but got {discount_factors_high[t]}"


#-------------------------
# Test cases for record_player_payoff_from_round

@pytest.fixture
def mock_player():
    player = Mock()
    player.role = "Seller"
    player.valuation = 0
    player.cumulated_TA_costs = 5
    player.current_discount_factor = 0.5
    player.group = Mock()
    player.group.deal_price = 20
    player.group.field_maybe_none = lambda x: 20 if x == 'deal_price' else None
    return player

def test_record_player_payoff_from_round_seller(mock_player):
    record_player_payoff_from_round(mock_player)
    expected_payoff = (20 - 0) * 0.5 - 5  # (deal_price - valuation) * discount_factor - transaction_costs
    assert np.isclose(mock_player.payoff, expected_payoff), f"Expected payoff {expected_payoff}, but got {mock_player.payoff}"

@pytest.fixture
def mock_buyer():
    player = Mock()
    player.role = "Buyer"
    player.valuation = 50
    player.cumulated_TA_costs = 5
    player.current_discount_factor = 0.5
    player.group = Mock()
    player.group.deal_price = 20
    player.group.field_maybe_none = lambda x: 20 if x == 'deal_price' else None
    return player

def test_record_player_payoff_from_round_buyer(mock_buyer):
    record_player_payoff_from_round(mock_buyer)
    expected_payoff = (50 - 20) * 0.5 - 5  # (valuation - deal_price) * discount_factor - transaction_costs
    assert np.isclose(mock_buyer.payoff, expected_payoff), f"Expected payoff {expected_payoff}, but got {mock_buyer.payoff}"

@pytest.fixture
def mock_player_terminated():
    player = Mock()
    player.cumulated_TA_costs = 5
    player.group = Mock()
    player.group.field_maybe_none = lambda x: 'some_time' if x == 'termination_time' else None
    return player

def test_record_player_payoff_from_round_terminated(mock_player_terminated):
    record_player_payoff_from_round(mock_player_terminated)
    expected_payoff = -5  # -transaction_costs
    assert mock_player_terminated.payoff == expected_payoff

@pytest.fixture
def mock_player_time_up():
    player = Mock()
    player.group = Mock()
    player.group.field_maybe_none = lambda x: None
    player.total_costs_list = '[1, 2, 3, 4, 5]'
    return player

def test_record_player_payoff_from_round_time_up(mock_player_time_up):
    record_player_payoff_from_round(mock_player_time_up)
    expected_payoff = -5  # -json.loads(player.total_costs_list)[-1]
    assert mock_player_time_up.payoff == expected_payoff


#-------------------------
# Test cases for draw_termination_times


@pytest.fixture
def default_params():
    return 5, 0.1

def test_draw_termination_times_correct_length(default_params):
    number_of_rounds, probability = default_params
    result = draw_termination_times(number_of_rounds, probability)
    assert len(result) == number_of_rounds

def test_draw_termination_times_all_integers(default_params):
    number_of_rounds, probability = default_params
    result = draw_termination_times(number_of_rounds, probability)
    assert all(isinstance(time, int) for time in result)

def test_draw_termination_times_all_positive(default_params):
    number_of_rounds, probability = default_params
    result = draw_termination_times(number_of_rounds, probability)
    assert all(time > 0 for time in result)

def test_draw_termination_times_reproducibility(default_params):
    number_of_rounds, probability = default_params
    result1 = draw_termination_times(number_of_rounds, probability)
    result2 = draw_termination_times(number_of_rounds, probability)
    assert result1 == result2

def test_draw_termination_times_probability_effect():
    number_of_rounds = 1000
    result_low_prob = draw_termination_times(number_of_rounds, 0.01)
    result_high_prob = draw_termination_times(number_of_rounds, 0.5)
    assert np.mean(result_low_prob) > np.mean(result_high_prob)

def test_draw_termination_times_zero_rounds():
    with pytest.raises(ValueError):
        draw_termination_times(0, 0.1)

def test_draw_termination_times_zero_probability():
    with pytest.raises(ValueError):
        draw_termination_times(5, 0)

def test_draw_termination_times_probability_greater_than_one():
    with pytest.raises(ValueError):
        draw_termination_times(5, 1.1)

def test_draw_termination_times_large_rounds():
    large_rounds = 1000
    large_result = draw_termination_times(large_rounds, 0.1)
    assert len(large_result) == large_rounds





#-------------------------
# Test cases for create_list_with_termination_probabilities_from_geometric_distribution


def test_create_list_with_termination_probabilities():

    number_of_seconds = 100
    probability_of_termination = 0.01
    probabilities = create_list_with_termination_probabilities_from_geometric_distribution(number_of_seconds, probability_of_termination)
    assert np.isclose(probabilities[2], 0.02970, atol=1e-3), "The probability at the 3rd position should be 0.02970."

