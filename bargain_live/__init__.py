from otree.api import *
import json
import random
import time
import math
import pandas as pd
import re
import numpy as np
import pathlib
from datetime import datetime, timezone, timedelta

from bargain_live.bargaining_functions import calculate_total_delay_list, calculate_transaction_costs, update_broadcast_dict_with_basic_values, update_player_database_with_proposal, update_group_database_upon_acceptance, update_group_database_upon_termination, update_broadcast_dict_with_other_player_values, setup_player_valuation, setup_player_transaction_costs, setup_player_delay_list, record_player_payoff_from_round, record_bargaining_time_on_group_level, set_final_player_payoff, is_valid_dataframe, is_valid_list, setup_player_shrinking_pie_discount_factors, calculate_round_results, create_payoff_dictionary, update_group_database_upon_random_termination, create_dictionary_with_html_variables_for_bargain_page, create_dictionary_with_js_variables_for_bargain_page, update_broadcast_dict_based_on_actions, write_bot_giving_offer_and_improving, write_bot_giving_offer_and_accepting_the_second_offer, create_list_with_termination_probabilities_from_geometric_distribution, create_dictionary_with_html_variables_for_bargain_instructions

from settings import LANGUAGE_CODE


doc = """
"""

CURRENT_PATH = pathlib.Path(__file__).parent


#-----------------------------------------------------------------------------------------------

#Language
if LANGUAGE_CODE == 'de':
    from bargain_live.lexicons.lexicon_de import Lexicon
else:
    from bargain_live.lexicons.lexicon_en import Lexicon

which_language = {'en': False, 'de': False, 'zh': False}  # noqa
which_language[LANGUAGE_CODE[:2]] = True

# Global Classes
class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = 2
    NUM_PRACTICE_ROUNDS = 3
    NUM_REAL_ROUNDS = 30
    NUM_ROUNDS = NUM_PRACTICE_ROUNDS + NUM_REAL_ROUNDS
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'
    TOTAL_BARGAINING_TIME = 500
 

class Subsession(BaseSubsession):
    is_practice_round = models.BooleanField()
    real_round_number = models.IntegerField()


class Group(BaseGroup):
    deal_price = models.FloatField()
    is_finished = models.BooleanField(initial=False)

    acceptance_time = models.IntegerField()
    accepted_by = models.IntegerField()

    first_proposal_by = models.IntegerField()
    latest_proposal_by = models.IntegerField()

    terminated = models.BooleanField(initial=False)
    termination_time = models.IntegerField()
    terminated_by = models.IntegerField()

    bargain_start_time = models.FloatField()
    bargaining_duration = models.FloatField()
   
    current_seller_offer = models.FloatField()
    current_buyer_offer = models.FloatField()

    termination_times_list = models.LongStringField()
    random_termination_time_current_round = models.IntegerField()
    termination_mode = models.StringField()


class Player(BasePlayer):

    consent_form = models.BooleanField(label='Ich habe die Teilnehmebedingungen gelesen und bin mit der Teilnahme einverstanden.', 
        widget=widgets.CheckboxInput,
        blank=False)

    proposal_made = models.BooleanField(initial=False)
    amount_proposed = models.FloatField()#
    amount_accepted = models.IntegerField()#
    current_amount_proposed = models.FloatField()

    amount_proposed_list = models.LongStringField(default="[]")
    offer_time_list = models.LongStringField(default="[]")

    valuation = models.FloatField()#
    current_deal_accept = models.IntegerField()#
    current_payoff_accept = models.FloatField()#


    current_deal_other_accepts = models.IntegerField()#
    current_payoff_other_accepts = models.FloatField()#

    initial_TA_costs = models.IntegerField()#
    decrease_TA_costs_per_second = models.IntegerField()#
    current_TA_costs = models.FloatField()#
    cumulated_TA_costs = models.FloatField(initial=0)#

    delay_multiplier = models.FloatField()
    payment_delay = models.FloatField()
    current_discount_factor = models.FloatField()

    current_payoff_terminate = models.FloatField()#

    current_costs_list = models.LongStringField()
    total_costs_list = models.LongStringField()
    total_delay_list = models.LongStringField()
    discount_factors_list = models.LongStringField()
    x_axis_values_TA_graph = models.LongStringField()
    x_axis_values_delay_graph = models.LongStringField()
    y_axis_maximum_TA_graph = models.FloatField()
    y_axis_maximum_delay_graph = models.FloatField()

    termination_probabilities_list = models.LongStringField()

    #Comprehension questions
    comprehension_1 = models.IntegerField(
        label="Which of the following statements is incorrect?",
        choices=[
            [1, Lexicon.comprehension_question_1_choice_1],
            [2, Lexicon.comprehension_question_1_choice_2],
            [3, Lexicon.comprehension_question_1_choice_3],
            [4, Lexicon.comprehension_question_1_choice_4]
        ], 
        blank=True
    )

    comprehension_2 = models.IntegerField(
        label="Which of the following statements is incorrect?",
        choices=[
            [1, Lexicon.comprehension_question_2_choice_1],
            [2, Lexicon.comprehension_question_2_choice_2],
            [3, Lexicon.comprehension_question_2_choice_3],
            [4, Lexicon.comprehension_question_2_choice_4]
        ], 
        blank=True
    )

    comprehension_3 = models.IntegerField(
        label="Which of the following statements is incorrect?",
        choices=[
            [1, Lexicon.comprehension_question_3_choice_1],
            [2, Lexicon.comprehension_question_3_choice_2],
        ], 
        blank=True
    )

    question_strategy = models.LongStringField(
        blank=False
    )

    

#-----------------------------------------------------------------------------------------------   
# FUNCTIONS


def creating_session(subsession):
    """ 
    This function is called before each subsession starts. 
    """

    #Set the TA treatment
    subsession.session.vars['TA_treatment'] = True if subsession.session.config['transaction_costs'] > 0 else False

    #Load the pre-drawn groupings and participant data
    participant_data = pd.read_pickle(CURRENT_PATH / 'randomization_values' / f'participant_data_{subsession.session.config["number_of_groups"]}_groups_{subsession.session.config["information_asymmetry"]}.pkl')

    is_valid_dataframe(participant_data, "participant_data")

    groups_data = pd.read_pickle(CURRENT_PATH / 'randomization_values' / f'round_groupings_{subsession.session.config["number_of_groups"]}_groups_{subsession.session.config["information_asymmetry"]}.pkl')

    is_valid_list(groups_data, "groups_data")

    termination_times_list = pd.read_pickle(CURRENT_PATH / 'randomization_values' / f'termination_times_{subsession.session.config["termination_treatment"]}.pkl')

    #Check if the subsession is a practice round
    subsession.is_practice_round = (
        subsession.round_number <= C.NUM_PRACTICE_ROUNDS
    )

    # In the first round, I set the role of the player which stays the same over the entire game
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.vars['role_in_game'] = participant_data.loc[
        participant_data['Participant_ID'] == player.participant.id_in_session, 'Role'
        ].values[0]

    # For the practice rounds, I set the parameters from the first round
    if subsession.is_practice_round:

        subsession.set_group_matrix([[p] for p in subsession.get_players()])

        for player in subsession.get_players():


            #Initialize valuation, transaction costs and delay list for each player
            player.valuation = participant_data.loc[
            participant_data['Participant_ID'] == player.participant.id_in_session, 'Valuation'
            ].values[0][2] # I set the second valuation for the practice rounds to avoid the 0 valuation for one buyer


            setup_player_transaction_costs(player=player, 
                                        cost_factor=subsession.session.config['transaction_costs'],
                                        total_bargaining_time=C.TOTAL_BARGAINING_TIME)
            
            
            player.termination_probabilities_list = json.dumps(create_list_with_termination_probabilities_from_geometric_distribution(number_of_seconds=C.TOTAL_BARGAINING_TIME,
            probability_of_termination=subsession.session.config['termination_treatment']))
            

        # I want to override the random termination time for the practice rounds so that the computer does not terminate the bargaining too early
        for group in subsession.get_groups():
            group.random_termination_time_current_round = 120

    # This initializes the parameters for the real rounds
    else:
        subsession.real_round_number = (
            subsession.round_number - C.NUM_PRACTICE_ROUNDS
        )

        subsession.set_group_matrix(groups_data[subsession.real_round_number-1])

        for player in subsession.get_players():


            #Initialize valuation, transaction costs and delay list for each player
            player.valuation = participant_data.loc[
            participant_data['Participant_ID'] == player.participant.id_in_session, 'Valuation'
            ].values[0][subsession.real_round_number-1]

            player.participant.vars['role_in_game'] = participant_data.loc[
            participant_data['Participant_ID'] == player.participant.id_in_session, 'Role'
            ].values[0]


            setup_player_transaction_costs(player=player, 
                                        cost_factor=subsession.session.config['transaction_costs'],
                                        total_bargaining_time=C.TOTAL_BARGAINING_TIME)
            
            
            setup_player_shrinking_pie_discount_factors(player=player,
                                                        delay_treatment_high=subsession.session.config['delay_treatment_high'],
                                                        total_bargaining_time=C.TOTAL_BARGAINING_TIME)
            
            player.termination_probabilities_list = json.dumps(create_list_with_termination_probabilities_from_geometric_distribution(number_of_seconds=C.TOTAL_BARGAINING_TIME,
                                                                                                                            probability_of_termination=0.01 if subsession.session.config['termination_treatment'] == 'low_prob' else 0.04))
            
        for group in subsession.get_groups():
            group.random_termination_time_current_round = termination_times_list[subsession.real_round_number-1]
   
        
        #Randomly determine the round in which the final payoffs are calculated
        if subsession.real_round_number == 1:


            for player in subsession.get_players():
                player.participant.vars['random_round'] = random.randint(1, C.NUM_REAL_ROUNDS)


          

        

     

    

#-----------------------------------------------------------------------------------------------
# PAGES

#---Page Template for Translation---#

class TranslationTemplate(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(Lexicon=Lexicon, **which_language)


#--Short Static Pages--#

class Consent(TranslationTemplate):
    form_model = 'player'
    form_fields = ['consent_form']

    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 1


class BargainInstructions(Page):
    form_model = 'player'
    form_fields = ['comprehension_1', 'comprehension_2', 'question_strategy']
    @staticmethod
    def vars_for_template(player: Player):

        dictionary_with_variables = create_dictionary_with_html_variables_for_bargain_instructions(player=player)

        dictionary_with_variables.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary_with_variables
    

    def error_message(self, values):

        # Check answers
        if values['comprehension_1'] != 3:
            return "You have not answered the first question correctly. Please try again."
        
        if values['comprehension_2'] != 4:
            return "You have not answered the second question correctly. Please try again."
    

    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 1
    

class PracticeRoundsIntro(Page):
    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        role_in_game = player.participant.vars['role_in_game']

        dictionary = {'role_in_game': role_in_game}

        dictionary.update(dict(Lexicon=Lexicon, **which_language))


        return dictionary



class BargainWaitPage(WaitPage):
    body_text = "Please wait while other players and the computer are getting ready. This can take up to a couple of minutes in some cases!"

    @staticmethod
    def after_all_players_arrive(group):
        # Set start time 5 seconds in the future
        group.bargain_start_time = time.time() + 5


class BargainPracticeOneIntro(TranslationTemplate):
    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 1
    
    
class BargainPracticeTwoIntro(TranslationTemplate):
    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 2
    
    
class BargainPracticeThreeIntro(TranslationTemplate):
    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 3
    

class BargainInfoRealGame(TranslationTemplate):
    @staticmethod
    def is_displayed(player):
        return player.subsession.field_maybe_none('real_round_number') == 1
    

class RoundResults(Page):
    @staticmethod
    def vars_for_template(player: Player):

        practice_round = player.subsession.is_practice_round

        dictionary_with_results = calculate_round_results(player=player, practice_round=practice_round)

        dictionary_with_results.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary_with_results

class FinalResults(Page):
    @staticmethod
    def vars_for_template(player: Player):

        dictionary_with_results = create_payoff_dictionary(player=player)

        dictionary_with_results.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary_with_results
    
    
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

#--Dynamic Bargain Pages--#

class BargainPracticeOne(Page):

    template_name = "global/Bargain.html"

    @staticmethod
    def vars_for_template(player: Player):

        dictionary = create_dictionary_with_html_variables_for_bargain_page(player=player, practice_round=True)

        #Language variables
        dictionary.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary


    @staticmethod
    def js_vars(player: Player):

        dictionary = create_dictionary_with_js_variables_for_bargain_page(player=player, C=C, practice_round=True, language_code=LANGUAGE_CODE)


        return dictionary

    @staticmethod
    def live_method(player: Player, data):

        #Initialize variables
        group = player.group
        broadcast = {}

        broadcast = update_broadcast_dict_with_basic_values(
            player=player,
            group=group,
            broadcast=broadcast
        )

        broadcast = update_broadcast_dict_with_other_player_values(
            player=player,
            broadcast=broadcast, 
            practice_round=True
        )

        broadcast = update_broadcast_dict_based_on_actions(broadcast = broadcast, 
                                                            data = data, 
                                                            player = player, 
                                                            group = group, 
                                                            practice_round = True)
        
        #Override the termination time to 30 for this practice round
        player.group.random_termination_time_current_round = 30


        return {0: broadcast}


    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        
        record_bargaining_time_on_group_level(player=player, C=C)
        record_player_payoff_from_round(player=player)


class BargainPracticeTwo(Page):

    template_name = "global/Bargain.html"

    @staticmethod
    def vars_for_template(player: Player):

        dictionary = create_dictionary_with_html_variables_for_bargain_page(player=player, practice_round=True)

        #Language variables
        dictionary.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary
    
    
    @staticmethod
    def js_vars(player: Player):

        dictionary = create_dictionary_with_js_variables_for_bargain_page(player=player, C=C, practice_round=True, language_code=LANGUAGE_CODE)

        return dictionary
    
    @staticmethod
    def live_method(player: Player, data):

        #Initialize variables
        group = player.group
        broadcast = {}
        bargaining_time_elapsed = round(time.time() - group.bargain_start_time)

        broadcast = update_broadcast_dict_with_basic_values(
            player=player,
            group=group,
            broadcast=broadcast
        )

        broadcast = update_broadcast_dict_with_other_player_values(
            player=player,
            broadcast=broadcast,
            practice_round=True
        )

        broadcast = update_broadcast_dict_based_on_actions(broadcast = broadcast, 
                                                            data = data, 
                                                            player = player, 
                                                            group = group, 
                                                            practice_round = True)
        
        
        #Write bot logic 
        broadcast = write_bot_giving_offer_and_improving(broadcast=broadcast, 
                                                        data=data, 
                                                        player=player, 
                                                        group=group, 
                                                        initial_offer_from_bot=15,
                                                        bargaining_time_elapsed=bargaining_time_elapsed)
        
        #Override the termination time to 60 for this practice round
        player.group.random_termination_time_current_round = 60

        return {0: broadcast}
    
    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 2
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        
        record_bargaining_time_on_group_level(player=player, C=C)
        record_player_payoff_from_round(player=player)

    

class BargainPracticeThree(Page):

    template_name = "global/Bargain.html"


    @staticmethod
    def vars_for_template(player: Player):

        dictionary = create_dictionary_with_html_variables_for_bargain_page(player=player, practice_round=True)

        #Language variables
        dictionary.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary
    
    
    @staticmethod
    def js_vars(player: Player):
        return create_dictionary_with_js_variables_for_bargain_page(player=player, C=C, practice_round=True, language_code=LANGUAGE_CODE)
    
    @staticmethod
    def live_method(player: Player, data):

        #Initialize variables
        group = player.group
        broadcast = {}
        bargaining_time_elapsed = round(time.time() - group.bargain_start_time)
        amount_proposed_list = json.loads(player.amount_proposed_list)

        broadcast = update_broadcast_dict_with_basic_values(
            player=player,
            group=group,
            broadcast=broadcast
        )

        broadcast = update_broadcast_dict_with_other_player_values(
            player=player,
            broadcast=broadcast,
            practice_round=True
        )

        broadcast = update_broadcast_dict_based_on_actions(broadcast = broadcast, 
                                                            data = data, 
                                                            player = player, 
                                                            group = group, 
                                                            practice_round = True)
        
        
        #Write bot logic 
        broadcast = write_bot_giving_offer_and_accepting_the_second_offer(
            broadcast=broadcast,
            data=data,
            player=player,
            group=group,
            initial_offer_from_bot=16,
            bargaining_time_elapsed=bargaining_time_elapsed,
            amount_proposed_list=amount_proposed_list
        )

        #Override the termination time to 120 for this practice round
        player.group.random_termination_time_current_round = 120

        return {0: broadcast}
    
    @staticmethod
    def is_displayed(player):
        return player.subsession.round_number == 3
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        
        record_bargaining_time_on_group_level(player=player, C=C)
        record_player_payoff_from_round(player=player)
    




class BargainReal(Page):

    timeout_seconds = C.TOTAL_BARGAINING_TIME

    template_name = "global/Bargain.html"
    

    @staticmethod
    def vars_for_template(player: Player):

        dictionary = create_dictionary_with_html_variables_for_bargain_page(player=player, practice_round=False)

        #Language variables
        dictionary.update(dict(Lexicon=Lexicon, **which_language))

        return dictionary

    @staticmethod
    def js_vars(player: Player):

        dictionary = create_dictionary_with_js_variables_for_bargain_page(player=player, C=C, practice_round=False, language_code=LANGUAGE_CODE)
        
        return dictionary

    @staticmethod
    def live_method(player: Player, data):

        #Initialize variables
        group = player.group
        broadcast = {}

        broadcast = update_broadcast_dict_with_basic_values(
            player=player,
            group=group,
            broadcast=broadcast
        )

        broadcast = update_broadcast_dict_with_other_player_values(
            player=player,
            broadcast=broadcast,
            practice_round=False
        )

        broadcast = update_broadcast_dict_based_on_actions(broadcast = broadcast, 
                                                            data = data, 
                                                            player = player, 
                                                            group = group, 
                                                            practice_round = False)
                        
    
        return {0: broadcast}
    



    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        
        record_bargaining_time_on_group_level(player=player, C=C)
        record_player_payoff_from_round(player=player)

        if player.round_number == C.NUM_ROUNDS:
            set_final_player_payoff(player=player, C=C)




    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if not group.is_finished:
            return "Game not finished yet"

    @staticmethod
    def is_displayed(player: Player):
        return not player.subsession.is_practice_round
    



page_sequence = [#Consent, 
                 #BargainInstructions,
                 PracticeRoundsIntro,
                 BargainPracticeOneIntro,
                 BargainPracticeTwoIntro,
                 BargainPracticeThreeIntro,
                 BargainInfoRealGame,
                 BargainWaitPage,
                 BargainPracticeOne,
                 BargainPracticeTwo,
                 BargainPracticeThree,
                 BargainReal, 
                 RoundResults, 
                 FinalResults
                 ]