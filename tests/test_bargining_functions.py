import pytest
from typing import List, Tuple

from bargain_live.bargaining_functions import calculate_total_delay_list, calculate_transaction_costs



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
