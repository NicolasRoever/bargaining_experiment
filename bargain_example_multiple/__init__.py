from otree.api import *
import json
import random
import time


doc = """
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining_multiple'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'
    TA_COSTS = 0.1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deal_price = models.IntegerField()
    is_finished = models.BooleanField(initial=False)
    accepted_by = models.IntegerField()

    first_proposal_by = models.IntegerField()
    latest_proposal_by = models.IntegerField()

    terminated = models.BooleanField(initial=False)
    terminated_by = models.IntegerField()

    bargain_start_time = models.FloatField()


class Player(BasePlayer):
    amount_proposed = models.IntegerField()
    amount_accepted = models.IntegerField()

    amount_proposed_list = models.StringField()

    valuation = models.IntegerField()
    current_payoff_accept = models.IntegerField()
    current_payoff_terminate = models.IntegerField()

    current_TA_costs = models.IntegerField(initial = 10)
    cumulated_TA_costs = models.IntegerField(initial = 10)

    
# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        player.valuation = random.randint(0, 1000)


# PAGES

class BargainWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        group.bargain_start_time = time.time()
        print(group.bargain_start_time)


class Bargain(Page):

    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role, 
                    valuation = cu(player.valuation/100),
                    )


    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):

        group = player.group
        [other] = player.get_others_in_group()

        #cumulated_TA_costs = group.field_maybe_none('cumulated_TA_costs')
        #if cumulated_TA_costs is not None:


        bargaining_time_elapsed = int(time.time() - group.bargain_start_time)
        
        if bargaining_time_elapsed > 0 and bargaining_time_elapsed % 10 == 0:
            player.cumulated_TA_costs += player.current_TA_costs
        
        player.current_TA_costs = (bargaining_time_elapsed // 10 + 1) * 10
    
        #print("Time elapsed", bargaining_time_elapsed)
        #print("Current costs", player.current_TA_costs)
        #print("Cumulated costs", player.cumulated_TA_costs)


        amount_proposed_list = player.field_maybe_none('amount_proposed_list')
        if amount_proposed_list is not None:
            amount_proposed_list = json.loads(amount_proposed_list)
        else:
            amount_proposed_list = []

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

                return {0: dict(finished=True)}
                
            if data['type'] == 'propose':
                try:
                    amount = int(float(data['amount']) * 100)
                except Exception:
                    print('Invalid message received', data)
                    return
                player.amount_proposed = amount
                player.group.latest_proposal_by = data['latest_proposal_by']
                amount_proposed_list.append(amount)

                if other.role == "Buyer":
                    other.current_payoff_accept = other.valuation - player.amount_proposed
                elif other.role == "Seller":
                    other.current_payoff_accept = player.amount_proposed - other.valuation
                #print(other.current_payoff_accept)

                if other.field_maybe_none('amount_proposed') == None:
                    group.first_proposal_by = data['latest_proposal_by']
            
            player.amount_proposed_list = json.dumps(amount_proposed_list)

        elif 'terminated_by' in data:
            group.is_finished = True
            group.terminated = True
            group.terminated_by = data['terminated_by']
            group.deal_price = 0

            return {0: dict(finished=True)}


        current_proposals = []
        current_payoffs_accept = []
        for p in [player, other]:
            amount_proposed = p.field_maybe_none('amount_proposed')
            current_payoff_accept = p.field_maybe_none('current_payoff_accept')
            
            if amount_proposed is not None:
                current_proposals.append([p.id_in_group, amount_proposed])
            if current_payoff_accept is not None:
                current_payoffs_accept.append([p.id_in_group, current_payoff_accept])
            #print(current_proposals)
            #print(other.field_maybe_none('amount_proposed'))
            #print(current_payoffs_accept)

        amount_proposed = player.field_maybe_none('amount_proposed')
        other_amount_proposed = other.field_maybe_none('amount_proposed')
        latest_proposal_by = player.group.field_maybe_none('latest_proposal_by')

        #if amount_proposed is not None and other_amount_proposed is None:
            

        if amount_proposed is not None and latest_proposal_by == player.id_in_group:
            latest_proposal = [player.id_in_group, amount_proposed]

            latest_proposal_by = latest_proposal[0]

        
        # Print time spent on this page
        #if 'time_left' in data:
        #    print(data['time_left'])
        #print(time.time())
        
        return {0: {
                'current_proposals':current_proposals, 
                'latest_proposal_by':latest_proposal_by,
                'current_payoffs_accept':current_payoffs_accept,
                'current_TA_costs':player.current_TA_costs,
                'cumulated_TA_costs':player.cumulated_TA_costs,}
                }
            

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


class Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(deal_price = cu(player.group.deal_price/100),
                    )


page_sequence = [BargainWaitPage, Bargain, Results]