import pytest

from bargain_live.functions.bargaining import calculate_total_delay, calculate_transaction_costs




# Mock player class for testing
class MockPlayer:
    def __init__(self, delay_multiplier):
        self.delay_multiplier = delay_multiplier

# Mock constants class for testing
class MockConstants:
    TOTAL_BARGAINING_TIME = 120  

def test_calculate_total_delay_low_treatment():
    player = MockPlayer(delay_multiplier=0.5)
    C = MockConstants()
    expected_delay_list = [i * 0.5 for i in range(C.TOTAL_BARGAINING_TIME)]
    result = calculate_total_delay(player, C)
    
    assert result == expected_delay_list

def test_calculate_total_delay_high_treatment():
    player = MockPlayer(delay_multiplier=3.5)
    C = MockConstants()
    expected_delay_list = [i * 3.5 for i in range(C.TOTAL_BARGAINING_TIME)]
    result = calculate_total_delay(player, C)
    
    assert result == expected_delay_list

def test_calculate_transaction_costs_high_treatment():
    # High treatment, where decay factor is 0.99
    total_costs, current_costs = calculate_transaction_costs(TA_treatment_high=True, total_bargaining_time=120)
    expected_total_costs = [0.25 * (0.99 ** t) for t in range(120)]
    expected_current_costs = [expected_total_costs[i] - expected_total_costs[i + 1] for i in range(119)] + [0]
    
    assert total_costs == pytest.approx(expected_total_costs), "High treatment total cost calculation failed."
    assert current_costs == pytest.approx(expected_current_costs), "High treatment current cost differences failed."

def test_calculate_transaction_costs_low_treatment():
    # Low treatment, where decay factor is 0.93
    total_costs, current_costs = calculate_transaction_costs(TA_treatment_high=False, total_bargaining_time=120)
    expected_total_costs = [0.25 * (0.93 ** t) for t in range(120)]
    expected_current_costs = [expected_total_costs[i] - expected_total_costs[i + 1] for i in range(119)] + [0]
    
    assert total_costs == pytest.approx(expected_total_costs), "Low treatment total cost calculation failed."
    assert current_costs == pytest.approx(expected_current_costs), "Low treatment current cost differences failed."


