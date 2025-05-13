class Lexicon:


    #-----------------------------------
    # Consent
    #-----------------------------------

    consent_title = "Consent"

    #-----------------------------------
    # Bargain
    #-----------------------------------

    match_value = "In this match, your value of the object is "
    buyer_value_random = "The Buyer's value of the object will be randomly drawn between 0 and 30€."
    bargaining_starts_in = "Bargaining starts in 5"
    negotiation_costs = "Negotiation Costs"
    current_negotiation_costs = "Current negotiation costs per 1 second: "
    total_negotiation_costs = "Total negotiation costs: "
    time = "Time: "
    current_price_offer = "Your current submitted price offer: "
    no_offer_yet = "No offer yet."
    your_payoff = "Your payoff: "
    seconds = "Seconds"
    submit = "Submit"
    instructions = "Instructions"
    welcome_message = "Welcome to the experiment. Please read these instructions carefully. The payment you will receive from this experiment depends partly on your decisions, partly on the decisions of others, and partly on chance. The amount you earn will be paid electronically via "
    experiment_structure = "The experiment consists of 30 matches. At the beginning of the experiment, participants will be randomly assigned the role of either buyer or seller. This role will remain fixed throughout all 30 matches. At the beginning of each match, you will be randomly paired with another participant in the opposite role. After each match, participants will be randomly re-paired, and new pairs will be formed."
    negotiation_intro = "In each match, buyers and sellers will negotiate to trade an object:"
    seller_value_one_sided = "The seller's value for the object is 0 euros."
    seller_value_two_sided = "The seller's value for the object is a random number between 0 and 30 euros."
    buyer_value = "The buyer's value for the object is private and will be randomly set between 0 and 30 euros. Only the buyer knows their value, and this value will remain unknown to the seller."
    information_one_sided = "This means that the seller does not know the buyer's value."
    information_two_sided = "This means that neither the buyer nor the seller knows the other's value."
    price_negotiation_heading = "1. Price Negotiation"
    price_negotiation_intro = "The buyer and seller negotiate the price:"
    price_submission = "Both participants can submit prices by selecting a value on a slider and clicking \"Submit.\" The submitted price will appear on the other person's screen."
    price_update = "You can submit new prices at any time during the negotiation. When a new price is submitted, the previous one becomes invalid and disappears from the other person's screen."
    costs_heading = "2. Costs Associated with Delay"
    costs_intro = "During the price negotiation, any delay incurs two types of costs: transaction costs and termination uncertainty."
    negotiation_cost_heading = "2.1 Negotiation Cost"
    negotiation_costs1 = "Negotiation costs of "
    negotiation_costs2 = " Cents are incurred for each second of the negotiation. The longer the negotiation, the higher the cost imposed on both participants. The graph on the left visualizes the cumulative negotiation costs. The sum of the negotiation costs will be deducted from your participation fees (which will be explained later) in this experiment."
    termination_heading = "2.2 Termination Uncertainty"
    termination_probability1 = "Each second during the negotiation, there is a "
    termination_probability2 = " % chance that the computer will end the negotiation. On average, this means, if no agreement is reached before, negotiations are expected to last about "
    termination_probability3 = " seconds before they are terminated."

    termination_explanation = "This process is similar to drawing a ball from a jar with 99 red balls and 1 blue ball at the end of each second. If a red ball is drawn, the negotiation continues; if a blue ball is drawn, the negotiation ends. Each draw is independent, so the outcome of one second does not affect the next."

    ending_negotiation_heading = "3. Ending the Negotiation"
    ending_negotiation_intro = "The negotiation ends if:"
    acceptance_rule = "A participant accepts the other's price. You can also accept by making a \"stupid\" offer. This means if the buyer makes an offer that is lower than the seller's offer, this is treated as an acceptance. Similarly, if the seller makes an offer that is higher than the buyer's offer, this is also treated as an acceptance."
    terminate_rule = "Either participant clicks \"Terminate,\" which ends the match with zero trade gains for both."
    termination_explanation_costs = "Any incurred negotiation costs will still apply."
    random_termination_rule = "The negotiation is randomly terminated, which also ends the match with zero trade gains for both."
    random_termination_explanation_costs = "Any incurred negotiation costs will still apply."

    options_summary_heading = "4. Options Summary"
    options_summary_intro = "Throughout the negotiation, you have three options:"
    option_submit_price = "Submit a new price."
    option_terminate = "Terminate the negotiation."
    option_accept = "Accept the other participant's price (only available after the first price is submitted)."
    example_buyer_screen = "Example of Buyer’s screen"
    example_seller_screen = "Example of Seller’s screen"
    
    payment_heading = "Payment"
    payment_info = " At the end of the experiment, one match will be randomly selected for payment. Your final payoff is obtained as:"
    final_payoff_formula_ta_costs = "Final Payoff = Show-Up Fee (10€) + Gains from Trade – Total negotiation costs"
    final_payoff_formula_no_ta_costs = "Final Payoff = Show-Up Fee (10€) + Gains from Trade"

    buyer_payoff_example_intro_transaction_costs  = "Here is an example for how buyer's final payoff is calculated: If the price you negotiated is 31€ and the valuation is 38€, and you reach the agreement after 20 seconds, which results in transaction costs (in this example 0.05€ per second), the payoff is:"
    buyer_payoff_example_intro_no_transaction_costs = "Here is an example for how buyer's final payoff is calculated: If the price you negotiated is 31€ and the valuation is 38€, and you reach the agreement after 20 seconds, the payoff is:"
    buyer_payoff_value = "Value of the Object: "
    buyer_payoff_price = "Price: "
    buyer_payoff_trade_gains = "Gains from Trade: "
    buyer_payoff_transaction_costs = "Transaction Costs: "
    buyer_payoff_match = "Payoff from Match: "
    buyer_payoff_participation_fee = "Participation Fee: "
    buyer_payoff_total = "Total Payoff: "

    seller_payoff_example_intro_transaction_costs = "Here is an example for how seller’s final payoff is calculated: If the price you negotiated is 20€ and the valuation is 0€, and you reach the agreement after 20 seconds, which results in transaction costs (in this example 0.05€ per second), the payoff is:"
    seller_payoff_example_intro_no_transaction_costs = "Here is an example for how seller’s final payoff is calculated: If the price you negotiated is 20€ and the valuation is 0€, and you reach the agreement after 20 seconds, the payoff is:"
    seller_payoff_price = "Price: "
    seller_payoff_value = "Value of the Object: "
    seller_payoff_trade_gains = "Gains from Trade: "
    seller_payoff_transaction_costs = "Transaction Costs: "
    seller_payoff_match = "Payoff from Match: "
    seller_payoff_participation_fee = "Participation Fee: "
    seller_payoff_total = "Total Payoff: "

    comprehension_question_1 = "Comprehension Question: Please choose the incorrect statement"
    comprehension_question_2 = "Comprehension Question: Please choose the incorrect statement"
    comprehension_question_3 = "Comprehension Question: Assume that the negotiation is randomly terminated before the agreement. Which of the following statements is incorrect?"

    section_overview = "Overview"
    section_main_task = "Main Task"

    practice_round_1_title = "Practice Round 1 / 3"
    practice_round_1_text = "In this practice round, you will see the environment, you can submit offers or terminate the negotiation. You will not be playing against other players, so nothing will happen. Instead, the computer will automatically terminate the negotiation after 30 seconds."

    practice_round_2_title = "Practice Round 2 / 3"
    practice_round_2_text = "In this practice round, you will negotiate with the computer. The computer will make a random offer after 10 seconds and improve it every 10 seconds. You can choose to accept the offer, reject it, make a counter-offer, or terminate the negotiation. However, the computer will not accept any offers you make. The negotiation will automatically end after 60 seconds."

    practice_round_3_title = "Practice Round 3 / 3"
    practice_round_3_text = "In this practice round, the computer will make a random offer after 10 seconds and improve it every 10 seconds. You can choose to accept the offer, reject it, make a counter-offer, or terminate the negotiation. The computer will accept your second offer. If no agreement is reached according to the given rules, the negotiation will automatically end after 120 seconds."


    minimum_payoff_text_1 = "The minimum payoff in this experiment is "
    minimum_payoff_text_2 = "€. If your payoff in the round we select for payment is under "
    minimum_payoff_text_3 = "€, you will receive "
    minimum_payoff_text_4 = "€."


    comprehension_question_1_choice_1 = "The experiment consists of 30 matches."
    comprehension_question_1_choice_2 = "Participants will be randomly assigned the role of buyer or seller."
    comprehension_question_1_choice_3 = "The role of buyer and seller will be alternated across matches."
    comprehension_question_1_choice_4 = "At the beginning of each match, a buyer and a seller will be randomly paired."

    comprehension_question_2_choice_1 = "All participants can submit prices at any time."
    comprehension_question_2_choice_2 = "The seller’s value for the object is 0 euros."
    comprehension_question_2_choice_3 = "The buyer’s value for the object will be randomly set between 1 and 30 euros."
    comprehension_question_2_choice_4 = "At the beginning of each match, the buyer’s value for the object will be known to a seller in the same pair."

    comprehension_question_3_choice_1 = "The gains from trade are zero."
    comprehension_question_3_choice_2 = "The accumulated negotiation costs will not be deducted from the participation fees."
    comprehension_question_3_choice_3 = "The accumulated negotiation costs will be deducted from the participation fees."

    strategy_question_buyer = "Suppose you are a buyer with a valuation of 20. Describe your strategy for the bargaining game. Write at least 2 sentences."
    strategy_question_seller = "Suppose you are a seller with a valuation of 0 and a buyer makes an offer of 10. Describe your strategy for the bargaining game. Write at least 2 sentences."



    intro_practice_rounds_title = "Start of Practice Rounds"

    intro_practice_rounds_1 = "In this experiment, you are assigned the role of"
    intro_practice_rounds_2 = "and this role will remain the same throughout the entire experiment. Before the experiment begins, you will complete three practice rounds. The main purpose of these practice rounds is to help you become familiar with the environment. No practice round will count toward the final payment. Please read the instructions for each practice round carefully."
    
    intro_real_game_title = "End of Practice Rounds"
    intro_real_game = "Now, the real experiment begins. You will be matched with humans for a total of 30 matches. We will select one of these matches randomly to calculate your final payment."


    #-----------------------------------
    # Results
    #-----------------------------------

    practice_round_results_title_1 = " Results of this Practice Match (Practice Match"
    practice_round_results_title_2 = "of"
    practice_round_results_title_3 = ")"

    real_game_results_title_1 = " Results of this Match (Match"
    real_game_results_title_2 = "of"
    real_game_results_title_3 = ")"

    value_of_object = "Value of the Object: "
    price_label = "Price: "
    no_deal_text = "No Deal"
    gains_from_trade_label = "Gains from Trade: "
    transaction_costs_label = "Transaction Costs: "
    payoff_from_match_label = "Payoff from Match: "
    participation_fee_label = "Participation Fee: "
    total_payoff_label = "Total Payoff: "

    acceptance_1 = "You accepted the price offer by the "
    acceptance_2 = " of "
    acceptance_3 = "€."

    acceptance_4 = "The "
    acceptance_5 = " accepted your offer of "
    acceptance_6 = "€."

    payoff_calculation_practice_1 = "We would calculate your total payoff in the real experiment as "
    payoff_calculation_practice_2 = "€. It is calculated as follows: "

    payoff_calculation_real_1 = "If this match is drawn to be payoff-relevant, your total payoff is going to be "
    payoff_calculation_real_2 = "€. It is calculated as follows: "

    termination_text_computer_1 = "The bargaining was terminated by the computer after "
    termination_text_computer_2 = " seconds."

    termination_text_player_self = "You terminated the negotation and no deal has been made."
    termination_text_player_other = "The bargaining was terminated by the other player and no deal has been made."

    no_deal_text = "No deal was made in the given time frame."


    bargain_page_warning_message_buyer = "Your offer is higher than the value of the object for you. Are you sure you want to submit your offer?"
    bargain_page_warning_message_seller = "Your offer is lower than the value of the object for the other player. Are you sure you want to submit your offer?"
          

    #-----------------------------------
    # Final Results
    #-----------------------------------

    final_results_title = "Your Payoff"

        
    final_results_1 = "Match "
    final_results_2 = " was chosen to be payoff-relevant. "

    below_minimum_payoff_1 = "The payoff from this match would be: "
    below_minimum_payoff_2 = "€. However, this is below the minimum payoff of 7.5€. Thus, your final payoff is 7.5€."

        
    final_results_3 = "This means the money you get for this participating in the experiment is: "
    final_results_4 = "€. We calculate this as follows:"

    final_results_5 = "The deal was terminated. Thus, your final payoff is given by participation fee minus transaction costs, so "
    final_results_6 = " - "
    final_results_7 = " = "

    final_results_8 = "No deal was made in the given time frame. Thus, your final payoff is given by participation fee minus transaction costs, so "
    final_results_9 = " - "
    final_results_10 = " = "


    #-----------------------------------
    #Bargain Page
    #-----------------------------------

    bargaining_countdown_text = "Bargaining starts in 5"

    bargain_page_title_practice_1 = "Practice Match "
    bargain_page_title_practice_2 = " of "
    bargain_page_title_real_1 = "Match "
    bargain_page_title_real_2 = " of "

    bargain_page_own_value = "In this match, your value of the object is"
    value_of_object_for_seller_0 = "The value of the object for the seller is 0."
    value_of_object_for_seller_random = "The value of the object for the seller is a random number between 0 and 30€."
    value_of_object_for_buyer = "The value of the object for the buyer is randomly drawn between 0 and 30€."

    bargain_page_negotiation_costs_heading = "Negotiation Costs"
    bargain_page_negotiation_costs_current = "Current negotiation costs per 1 second"
    bargain_page_negotiation_costs_total = "Total negotiation costs"


    bargain_time = "Time: "
    seconds = " seconds"

    bargain_page_current_price_offer = "Your current submitted price offer:"

    submit = "Submit"
    accept_other_player_offer = "Accept"

    bargain_page_other_player_accepts_your_current_offer = "If the other player accepts your current offer:"

    bargain_page_your_payoff = "Your payoff:"
    bargain_page_payoff_other_player = "Payoff Other Player:"

    bargain_page_other_player_current_price_offer = "Other Player's current submitted price offer:"

    bargain_page_if_you_accept_the_offer = "If you accept the offer: "


    bargain_page_accept_other_player_offer = "Accept Other Player's Offer"

    bargain_page_if_you_accept_the_offer = "If you accept the offer: "

    bargain_page_risk_of_termination = "Risk of Termination"

    bargain_page_probability_of_termination = "The probability that the computer will terminate the negotiation in the next second is "

    bargain_page_payoffs_heading = "Payoffs"
    bargain_page_payoffs_heading_1 = "If an offer is accepted:"
    bargain_page_payoffs_seller_payoff_ta_costs = "Seller's payoff: Accepted offer - Negotiation costs"
    bargain_page_payoffs_buyer_payoff_ta_costs = "Buyer's payoff: Buyer's valuation - Accepted offer - Negotiation costs"
    bargain_page_payoffs_seller_payoff_0_ta_costs = "Seller's payoff: Accepted offer - Seller's Valuation"
    bargain_page_payoffs_buyer_payoff_0_ta_costs = "Buyer's payoff: Buyer's valuation - Accepted offer"

    bargain_page_payoffs_heading_2 = "If buyer or seller terminates the negotiation:"
    bargain_page_payoffs_both_payoff_ta_costs = "Both payoff: - Negotiation costs"
    bargain_page_payoffs_both_payoff_0_ta_costs = "Both payoff: 0€"

    bargain_page_terminate_negotiation_button = "Terminate"
    bargain_page_terminate_negotiation = "Terminate the Negotiation"
    bargain_page_terminate_negotiation_if_you = "If you terminate the negotiation:"
    bargain_page_terminate_negotiation_both_payoff = "Both players receive a payoff of: "
    bargain_page_terminate_negotiation_other_payoff = "Other Player's Payoff: "

    bargain_page_terminate_negotiation_heading = "Termination"
    bargain_page_terminate_negotiation_heading_1 = "If you terminate the negotiation:"
    bargain_page_terminate_negotiation_heading_2 = "If the other player terminates the negotiation:"
    





