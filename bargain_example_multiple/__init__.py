from otree.api import *
import json


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

    all_proposals = models.StringField()
    latest_proposal = models.StringField()
    latest_offer_by = models.IntegerField()


class Player(BasePlayer):
    amount_proposed = models.IntegerField()
    amount_accepted = models.IntegerField()

    


class Bargain(Page):
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
                    return {0: dict(finished=True)}
            if data['type'] == 'propose':
                player.amount_proposed = amount
                player.group.latest_offer_by = data['latest_offer_by']
            
            #if data['latest_offer_by'] == player.id_in_group:
            #    print("I made an offer")
            #    print(player.id_in_group)

        current_proposals = []
        for p in [player, other]:
            amount_proposed = p.field_maybe_none('amount_proposed')
            if amount_proposed is not None:
                current_proposals.append([p.id_in_group, amount_proposed])
            #print(current_proposals)
        #return {0: dict(current_proposals=current_proposals)}

        all_proposals = player.group.field_maybe_none('all_proposals')
        if all_proposals is not None: 
            all_proposals = json.loads(all_proposals)
        else:
            all_proposals = []
        #for p in [player, other]:
        
        amount_proposed = player.field_maybe_none('amount_proposed')
        latest_offer_by = player.group.field_maybe_none('latest_offer_by')

        if amount_proposed is not None and latest_offer_by == player.id_in_group:
            latest_proposal = [player.id_in_group, amount_proposed, latest_offer_by]
            all_proposals.append(latest_proposal)

            latest_offer_by = latest_proposal[-1]

            print(all_proposals)
            print(latest_offer_by)
        player.group.all_proposals = json.dumps(all_proposals)
        
        #group.save()
        return {0: {'all_proposals':all_proposals, 
                'current_proposals':current_proposals, 
                'latest_offer_by':latest_offer_by}
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