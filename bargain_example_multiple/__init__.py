from otree.api import *
import json
import random


doc = """
For oTree beginners, it would be simpler to implement this as a discrete-time game 
by using multiple rounds, e.g. 10 rounds, where in each round both players can make a new proposal,
or accept the value from the previous round.

However, the discrete-time version has more limitations
(fixed communication structure, limited number of iterations).

Also, the continuous-time version works smoother & faster, 
and is less resource-intensive since it all takes place in 1 page.
"""


class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining_multiple'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    deal_price = models.CurrencyField()
    is_finished = models.BooleanField(initial=False)
    accepted_by = models.IntegerField()

    all_proposals = models.StringField()
    first_proposal_by = models.IntegerField()
    latest_proposal_by = models.IntegerField()


class Player(BasePlayer):
    amount_proposed = models.IntegerField()
    amount_accepted = models.IntegerField()

    amount_proposed_list = models.StringField()

    valuation = models.IntegerField()
    current_payoff_accept = models.IntegerField()

    
# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        player.valuation = random.randint(0, 10)



class Bargain(Page):
    #timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):

        group = player.group
        [other] = player.get_others_in_group()

        amount_proposed_list = player.field_maybe_none('amount_proposed_list')
        if amount_proposed_list is not None:
            amount_proposed_list = json.loads(amount_proposed_list)
        else:
            amount_proposed_list = []

        if 'amount' in data:
            try:
                amount = int(data['amount'])
            except Exception:
                print('Invalid message received', data)
                return
            if data['type'] == 'accept':
                if amount == other.amount_proposed:
                    player.amount_accepted = amount
                    group.deal_price = amount
                    group.is_finished = True
                    group.accepted_by = data['accepted_by']
                    return {0: dict(finished=True)}
            if data['type'] == 'propose':
                player.amount_proposed = amount
                player.group.latest_proposal_by = data['latest_proposal_by']
                amount_proposed_list.append(amount)

                if other.role == "Buyer":
                    other.current_payoff_accept = other.valuation - player.amount_proposed
                elif other.role == "Seller":
                    other.current_payoff_accept = player.amount_proposed - other.valuation
                #print(other.current_payoff_accept)
            
            player.amount_proposed_list = json.dumps(amount_proposed_list)


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
            #print(current_payoffs_accept)

        all_proposals = player.group.field_maybe_none('all_proposals')
        if all_proposals is not None: 
            all_proposals = json.loads(all_proposals)
        else:
            all_proposals = []

        amount_proposed = player.field_maybe_none('amount_proposed')
        latest_proposal_by = player.group.field_maybe_none('latest_proposal_by')

        if amount_proposed is not None and latest_proposal_by == player.id_in_group:
            latest_proposal = [player.id_in_group, amount_proposed]
            all_proposals.append(latest_proposal)

            latest_proposal_by = latest_proposal[0]

            if len(all_proposals) < 2:
                group.first_proposal_by = data['latest_proposal_by']
        
        player.group.all_proposals = json.dumps(all_proposals)

        # Define current payoffs in case of accepting other's offer
        # buyer gets v - p
        # seller gets p - v
        #for p in [player, other]:
        #    try: 
        #        int(other.amount_proposed)
        #    except Exception:
        #        print("No offer yet")
        #    if p.role == "Buyer":
        #        current_payoff = p.valuation - other.amount_proposed
        #    elif p.role == "Seller":
        #        current_payoff = other.amount_proposed - p.valuation
        #    print(current_payoff)


        # Define current payoffs in case of terminating bargaining

        
        return {0: {#'all_proposals':all_proposals, 
                'current_proposals':current_proposals, 
                'latest_proposal_by':latest_proposal_by,
                'current_payoffs_accept':current_payoffs_accept,}
                #'payoff_buyer_accept':},
                #player.get_others_in_group(latest_proposal_by): {
                #    'current_payoff_accept':player.field_maybe_none('current_payoff_accept'),
                #    }
                
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
    pass


page_sequence = [Bargain, Results]