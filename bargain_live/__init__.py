from otree.api import *
import json
import random
import time
import math
import pandas as pd
import re
import numpy as np
import pathlib

from bargain_live.bargaining_functions import calculate_total_delay_list, calculate_transaction_costs, update_broadcast_dict_with_basic_values, update_player_database_with_proposal, update_group_database_upon_acceptance, update_group_database_upon_termination, update_broadcast_dict_with_other_player_values, setup_player_valuation, setup_player_transaction_costs, setup_player_delay_list, record_player_payoff_from_round, record_bargaining_time_on_group_level, set_final_player_payoff, is_valid_dataframe, is_valid_list, setup_player_shrinking_pie_discount_factors, calculate_round_results, create_payoff_dictionary


doc = """
"""

CURRENT_PATH = pathlib.Path(__file__).parent


#-----------------------------------------------------------------------------------------------
# Global Classes
class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'
    TOTAL_BARGAINING_TIME = 120


class Subsession(BaseSubsession):
    pass


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


class Player(BasePlayer):

    proposal_made = models.BooleanField(initial=False)
    amount_proposed = models.FloatField()#
    amount_accepted = models.IntegerField()#
    current_amount_proposed = models.FloatField()

    amount_proposed_list = models.StringField()#
    offer_time_list = models.StringField()#

    valuation = models.IntegerField()#
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
    

#-----------------------------------------------------------------------------------------------   
# FUNCTIONS


def creating_session(subsession):
    """ 
    This function is called before each subsession starts. In its current implementation, it initializes the players' valuations and transaction costs, thus, valuations are new in each subsession. 
    """

    subsession_number = subsession.round_number

    participant_data = pd.read_pickle(CURRENT_PATH / 'randomization_values' / f'participant_data_{subsession.session.config["number_of_groups"]}_groups.pkl')

    is_valid_dataframe(participant_data, "participant_data")

    groups_data = pd.read_pickle(CURRENT_PATH / 'randomization_values' / f'round_groupings_{subsession.session.config["number_of_groups"]}_groups.pkl')

    is_valid_list(groups_data, "groups_data")

    subsession.set_group_matrix(groups_data[subsession_number-1])

    for player in subsession.get_players():

        #Record the time when the bargaining starts for each subsession
        player.group.bargain_start_time = time.time() 

        #Initialize valuation, transaction costs and delay list for each player

        player.valuation = participant_data.loc[
        participant_data['Participant_ID'] == player.participant.id_in_session, 'Valuation'
        ].values[0][subsession_number-1]


        setup_player_transaction_costs(player=player, 
                                    ta_treatment=subsession.session.config['TA_treatment_high'],
                                    delay_treatment=subsession.session.config['delay_treatment_high'],
                                    total_bargaining_time=C.TOTAL_BARGAINING_TIME)
        
        setup_player_delay_list(player=player,
                                delay_treatment_high=subsession.session.config['delay_treatment_high'],
                                total_bargaining_time=C.TOTAL_BARGAINING_TIME
                                )
        
        setup_player_shrinking_pie_discount_factors(player=player,
                                                    delay_treatment_high=subsession.session.config['delay_treatment_high'],
                                                    total_bargaining_time=C.TOTAL_BARGAINING_TIME)
    
    #Randomly determine the round in which the final payoffs are calculated
    if subsession_number == 1:

        for player in subsession.get_players():
            player.participant.vars['random_round'] = random.randint(1, C.NUM_ROUNDS)


    
  

        



        



    

#-----------------------------------------------------------------------------------------------
# PAGES

class WelcomeAndConsent(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class BargainInstructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class BargainWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.bargain_start_time = time.time()


class Bargain(Page):

    timeout_seconds = C.TOTAL_BARGAINING_TIME

    @staticmethod
    def vars_for_template(player: Player):

        return dict(my_role=player.role,
                    other_role=player.get_others_in_group()[0].role, 
                    valuation=player.valuation,
                    delay_multiplier=player.delay_multiplier,  
                    double_delay_multiplier=player.delay_multiplier * 2, 
                    other_valuation=player.get_others_in_group()[0].valuation,
                    information_asymmetry=player.group.subsession.session.config['information_asymmetry'],
                    treatment_communication=player.group.subsession.session.config['treatment_communication'],
                    )


    @staticmethod
    def js_vars(player: Player):

        return dict(my_id=player.id_in_group, 
                    other_id=player.get_others_in_group()[0].id_in_group,
                    start_time=player.group.bargain_start_time, 
                    my_role=player.role,
                    my_valuation=player.valuation,
                    other_valuation=player.get_others_in_group()[0].valuation,
                    other_role=player.get_others_in_group()[0].role,
                    delay_multiplier=player.delay_multiplier,
                    information_asymmetry=player.group.subsession.session.config['information_asymmetry'],
                    maximum_bargain_time=C.TOTAL_BARGAINING_TIME,
                    x_values_TA_graph=json.loads(player.x_axis_values_TA_graph),
                    x_values_delay_graph=json.loads(player.x_axis_values_delay_graph), 
                    y_axis_maximum_TA_graph=player.y_axis_maximum_TA_graph,
                    y_axis_maximum_delay_graph=player.y_axis_maximum_delay_graph
                    )


    @staticmethod
    def live_method(player: Player, data):

        #Initialize variables
        group = player.group
        [other] = player.get_others_in_group()
        broadcast = {}

        broadcast = update_broadcast_dict_with_basic_values(
            player=player,
            group=group,
            broadcast=broadcast
        )

        broadcast = update_broadcast_dict_with_other_player_values(
            player=player,
            other=other,
            broadcast=broadcast
        )

        
        # Update database and broadcast if a proposal was made
        if data.get('type') == 'propose':

            if player.id_in_group == data.get('latest_proposal_by'):

               update_player_database_with_proposal(
                   player=player,
                   data=data
               )

            if data.get("proposal_by_role") == "Seller":

                group.current_seller_offer = data.get('amount')
                broadcast["seller_proposal"] = data.get('amount')


            elif data.get("proposal_by_role") == "Buyer":

                group.current_buyer_offer = data.get('amount')    
                broadcast["buyer_proposal"] = data.get('amount')



        #Update database and finish bargaining if a deal was accepted
        if data.get('type') == 'accept':

            update_group_database_upon_acceptance(
                group=group, 
                data=data)

            group.is_finished = True

            broadcast["finished"] = True

        #Update database and finish bargaining if a deal was terminated
        if data.get('terminated_by'):
        
            update_group_database_upon_termination(
                group=group,
                data=data
            )

            group.is_finished = True #This ensures no error is thrown

            broadcast["finished"] = True


        #Update broadcast if offers were already sent so that the client updates the payoffs (which change every second because of the transaction costs)
        if group.field_maybe_none('current_seller_offer'):

            broadcast.setdefault("seller_proposal", group.current_seller_offer)

        if group.field_maybe_none('current_buyer_offer'):

            broadcast.setdefault("buyer_proposal", group.current_buyer_offer)

        return {0: broadcast}
    



    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        record_player_payoff_from_round(player=player)
        record_bargaining_time_on_group_level(player=player, C=C)

        if player.round_number == C.NUM_ROUNDS:
            set_final_player_payoff(player=player, C=C)




    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if not group.is_finished:
            return "Game not finished yet"

    @staticmethod
    def is_displayed(player: Player):
        """Skip this page if a deal has already been made"""
        group = player.group
        deal_price = group.field_maybe_none('deal_price')
        return deal_price is None
    
    


class RoundResults(Page):
    @staticmethod
    def vars_for_template(player: Player):

        dictionary_with_results = calculate_round_results(player=player)

        return dictionary_with_results
    


class FinalResults(Page):
    @staticmethod
    def vars_for_template(player: Player):

        dictionary_with_results = create_payoff_dictionary(player=player)

        return dictionary_with_results
    
    
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [#WelcomeAndConsent, 
                 BargainInstructions,
                 BargainWaitPage, 
                 Bargain, 
                 RoundResults, 
                 FinalResults]