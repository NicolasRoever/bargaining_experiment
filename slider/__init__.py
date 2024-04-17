from otree.api import *


doc = """
Slider example
"""


class Constants(BaseConstants):
    name_in_url = "slider"
    players_per_group = 2
    num_rounds = 1
    BUYER_ROLE = 'Buyer'
    SELLER_ROLE = 'Seller'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    offer = models.FloatField()
    #number = models.IntegerField()


def creating_session(subsession):
    subsession.group_randomly()


# PAGES
class BargainingPage(Page):
    form_model = "player"
    form_fields = ["offer"] #, "number"

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)

    @staticmethod
   # def live_method(player, data):
    #    print('received a bid from', player.id_in_group, ':', data)
#
    def live_method(player, data):
        print('data is', data)
        player.offer = data
        print(player.offer)




class Results(Page):
    pass


page_sequence = [BargainingPage]
