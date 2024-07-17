from otree.api import *
import json
import random
import time


doc = """
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'
    TOTAL_BARGAINING_TIME = 10 * 60


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deal_price = models.IntegerField()
    is_finished = models.BooleanField(initial=False)

    acceptance_time = models.IntegerField()
    accepted_by = models.IntegerField()

    first_proposal_by = models.IntegerField()
    latest_proposal_by = models.IntegerField()

    terminated = models.BooleanField(initial=False)
    termination_time = models.IntegerField()
    terminated_by = models.IntegerField()

    bargain_start_time = models.FloatField()
    bargain_duration = models.IntegerField()


class Player(BasePlayer):
    amount_proposed = models.IntegerField()
    amount_accepted = models.IntegerField()

    amount_proposed_list = models.StringField()
    offer_time_list = models.StringField()

    valuation = models.IntegerField()
    current_deal_accept = models.IntegerField()
    current_payoff_accept = models.IntegerField()

    current_deal_other_accepts = models.IntegerField()
    current_payoff_other_accepts = models.IntegerField()

    initial_TA_costs = models.IntegerField()
    decrease_TA_costs_per_second = models.IntegerField()
    current_TA_costs = models.IntegerField()
    cumulated_TA_costs = models.IntegerField()

    payment_delay = models.IntegerField(initial=0)
    additional_delay = models.IntegerField()

    current_payoff_terminate = models.IntegerField()

    current_costs_list = models.StringField()
    total_costs_list = models.StringField()
    total_delay_list = models.StringField()

    

    
# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        # Randomly draw valuations in each round
        if player.role == "Seller":
            valuation_list = list(range(0, 501, 10))
        elif player.role == "Buyer":
            valuation_list = list(range(1000, 1501, 10))
        player.valuation = random.choice(valuation_list)


        # Set transaction costs treatment
        if player.group.subsession.session.config['TA_treatment_high'] == True:
            player.initial_TA_costs = player.current_TA_costs = player.cumulated_TA_costs =  100
            player.decrease_TA_costs_per_second = 1
        elif player.group.subsession.session.config['TA_treatment_high'] == False:
            player.initial_TA_costs = player.current_TA_costs = player.cumulated_TA_costs =  50
            player.decrease_TA_costs_per_second = 1

        player.current_payoff_terminate = -player.current_TA_costs

        # Set payment delay treatment
        if player.group.subsession.session.config['delay_treatment_high'] == True:
            player.additional_delay = 2
        elif player.group.subsession.session.config['delay_treatment_high'] == False:
            player.additional_delay = 1

    current_costs_list = [player.current_TA_costs]
    total_costs = player.current_TA_costs
    decrease_TA_costs_per_second = player.decrease_TA_costs_per_second

    total_delay = 0
    total_costs_list = []
    total_delay_list = []
    
    # Initiate list of total transaction costs
    for i in range(C.TOTAL_BARGAINING_TIME):
        if (i > 0):
            updated_costs = current_costs_list[i] - decrease_TA_costs_per_second 
            if updated_costs < 0:
                updated_costs = 0
            
            total_costs += updated_costs
            total_delay += player.additional_delay
        else:
            updated_costs = current_costs_list[i]

        current_costs_list.append(updated_costs)            
        total_costs_list.append(total_costs)
        total_delay_list.append(total_delay)
    #print(total_costs_list)

    for player in subsession.get_players():
        player.total_costs_list = json.dumps(total_costs_list)
        player.current_costs_list = json.dumps(current_costs_list)
        player.total_delay_list = json.dumps(total_delay_list)

    # Set up grouping mechanism of random grouping in each round with fixed roles across rounds
    #subsession.group_randomly(fixed_id_in_group = True) # Disable for testing


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
        print(group.bargain_start_time)


class Bargain(Page):

    timeout_seconds = C.TOTAL_BARGAINING_TIME

    @staticmethod
    def vars_for_template(player: Player):
        return dict(my_role=player.role,
                    other_role=player.get_others_in_group()[0].role, 
                    valuation=cu(player.valuation/100),
                    other_valuation=cu(player.get_others_in_group()[0].valuation/100),
                    additional_delay=player.additional_delay,
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
                    TA_treatment_high=player.group.subsession.session.config['TA_treatment_high'],
                    initial_TA_costs=player.initial_TA_costs,
                    decrease_TA_costs_per_second=player.decrease_TA_costs_per_second,
                    additional_delay=player.additional_delay,
                    delay_treatment_high=player.group.subsession.session.config['delay_treatment_high'],
                    information_asymmetry=player.group.subsession.session.config['information_asymmetry'],
                    maximum_bargain_time=C.TOTAL_BARGAINING_TIME,
                    )

    @staticmethod
    def live_method(player: Player, data):
        
        group = player.group
        [other] = player.get_others_in_group()

        # Adjust total transaction costs after each seconds
        bargaining_time_elapsed = int(time.time() - group.bargain_start_time)

        total_costs_list = json.loads(player.total_costs_list) 
        current_costs_list = json.loads(player.current_costs_list)
        total_delay_list = json.loads(player.total_delay_list)
        
        if bargaining_time_elapsed > 0:
            # Current transaction costs decrease every second by $0.01
            player.current_TA_costs = int(current_costs_list[bargaining_time_elapsed])
            player.cumulated_TA_costs = int(total_costs_list[bargaining_time_elapsed])

            # Termination payoff is just negative transaction costs
            player.current_payoff_terminate = - player.cumulated_TA_costs
            
            # Total delay in payment increases every second by additional delay
            player.payment_delay = int(total_delay_list[bargaining_time_elapsed])
            
        
        # Total payoff if other's current proposal is accepted
        if player.field_maybe_none('current_deal_accept') is not None:
            player.current_payoff_accept = player.current_deal_accept - player.cumulated_TA_costs

        if player.field_maybe_none('current_deal_other_accepts') is not None:
            player.current_payoff_other_accepts = player.current_deal_other_accepts - player.cumulated_TA_costs

        amount_proposed_list = player.field_maybe_none('amount_proposed_list')
        if amount_proposed_list is not None:
            amount_proposed_list = json.loads(amount_proposed_list)
        else:
            amount_proposed_list = []
        
        offer_time_list = player.field_maybe_none('offer_time_list')
        if offer_time_list is not None:
            offer_time_list = json.loads(offer_time_list)
        else:
            offer_time_list = []


        if 'amount' in data:
            
            if data['type'] == 'accept':
                try:
                    amount = int(data['amount'])
                except Exception:
                    print('Invalid message received', data)
                    return
                if amount == other.amount_proposed:
                    player.amount_accepted = amount
                    group.deal_price = amount
                    group.is_finished = True
                    group.accepted_by = data['accepted_by']
                    group.acceptance_time = data['acceptance_time']

                return {0: dict(finished=True)}
                
            if data['type'] == 'propose':
                try:
                    amount = int(float(data['amount']) * 100)
                except Exception:
                    print('Invalid message received', data)
                    return
                
                player.amount_proposed = amount
                amount_proposed_list.append(amount)

                offer_time = data['offer_time']
                offer_time_list.append(offer_time)

                player.group.latest_proposal_by = data['latest_proposal_by']

                if other.role == "Buyer":
                    other.current_deal_accept = other.valuation - player.amount_proposed
                    player.current_deal_other_accepts = player.amount_proposed - player.valuation
                elif other.role == "Seller":
                    other.current_deal_accept = player.amount_proposed - other.valuation
                    player.current_deal_other_accepts = player.valuation - player.amount_proposed
                
                #other.current_payoff_accept = other.current_deal_accept - other.cumulated_TA_costs

                

                if other.field_maybe_none('amount_proposed') == None:
                    group.first_proposal_by = data['latest_proposal_by']

            
            player.amount_proposed_list = json.dumps(amount_proposed_list)
            player.offer_time_list = json.dumps(offer_time_list)

        elif 'terminated_by' in data:
            group.is_finished = True
            group.terminated = True
            group.termination_time = data['termination_time']
            group.terminated_by = data['terminated_by']
            group.deal_price = 0

            return {0: dict(finished=True)}


        current_proposals = []
        #current_payoffs_accept = []
        current_payoffs_other_accepts = []
        for p in [player, other]:
            amount_proposed = p.field_maybe_none('amount_proposed')
            current_payoff_accept = p.field_maybe_none('current_payoff_accept')
            current_payoff_other_accepts = p.field_maybe_none('current_payoff_other_accepts')
            
            if amount_proposed is not None:
                current_proposals.append([p.id_in_group, amount_proposed])
            #if current_payoff_accept is not None:
            #    current_payoffs_accept.append([p.id_in_group, current_payoff_accept])
            #if current_payoff_other_accepts is not None:
            #   current_payoffs_other_accepts.append([p.id_in_group, current_payoff_other_accepts])

        amount_proposed = player.field_maybe_none('amount_proposed')
        other_amount_proposed = other.field_maybe_none('amount_proposed')
        latest_proposal_by = player.group.field_maybe_none('latest_proposal_by')

        if amount_proposed is not None and latest_proposal_by == player.id_in_group:
            latest_proposal = [player.id_in_group, amount_proposed]

            latest_proposal_by = latest_proposal[0]
        
        return {0: {
                'current_proposals':current_proposals, 
                'latest_proposal_by':latest_proposal_by,
                #'current_payoffs_accept':current_payoffs_accept,
                #'current_payoffs_other_accepts':current_payoffs_other_accepts,
                'current_TA_costs':player.current_TA_costs,
                'cumulated_TA_costs':player.cumulated_TA_costs,
                'current_payoff_terminate':player.current_payoff_terminate,
                'payment_delay':player.payment_delay,
                'bargaining_time_elapsed':bargaining_time_elapsed,
                }
                }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.group.is_finished == True:
            if player.group.terminated == False:
                if player.role == "Buyer":
                    player.payoff = (player.valuation - player.group.deal_price - player.cumulated_TA_costs)/100
                    
                elif player.role == "Seller":
                    player.payoff = (player.group.deal_price - player.valuation - player.cumulated_TA_costs)/100
            elif player.group.terminated == True:
                player.payoff = -player.cumulated_TA_costs/100
        
        else:
            player.payoff = 0
            player.group.deal_price = 0

        # Record total bargaininig time
        if player.group.is_finished == True:
            if player.group.field_maybe_none('acceptance_time') is not None:
                player.group.bargain_duration = player.group.acceptance_time 
            elif player.group.field_maybe_none('termination_time') is not None:
                player.group.bargain_duration = player.group.termination_time 
        else:
            player.group.bargain_duration = C.TOTAL_BARGAINING_TIME
        
        # Set final payoffs
        if player.round_number == C.NUM_ROUNDS:
            player.participant.random_round = random.choice(list(range(1, C.NUM_ROUNDS)))
            player.participant.payoff = player.in_round(player.participant.random_round).payoff



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
        return dict(deal_price = cu(player.group.deal_price/100),
                    other_role=player.get_others_in_group()[0].role, 
                    TA_costs = cu(player.cumulated_TA_costs / 100)
                    )

class FinalResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                    payoff_group_finished = player.in_round(player.participant.random_round).group.is_finished,
                    payoff_group_terminated = player.in_round(player.participant.random_round).group.field_maybe_none('terminated'),
                    payoff_group_terminated_by = player.in_round(player.participant.random_round).group.field_maybe_none('terminated_by'),
                    payoff_group_accepted_by = player.in_round(player.participant.random_round).group.field_maybe_none('accepted_by'),
                    payoff_valuation = cu(player.in_round(player.participant.random_round).valuation / 100),
                    payoff_TA_costs = cu(player.in_round(player.participant.random_round).cumulated_TA_costs / 100),
                    payoff_delay = player.in_round(player.participant.random_round).payment_delay,
                    payoff_bargaining_time = player.in_round(player.participant.random_round).group.bargain_duration,
                    payoff_deal_price = cu(player.in_round(player.participant.random_round).group.deal_price/100),
                    other_role=player.get_others_in_group()[0].role, 
                    )
    
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [#WelcomeAndConsent, 
                 BargainInstructions,
                 BargainWaitPage, 
                 Bargain, 
                 RoundResults, 
                 FinalResults]