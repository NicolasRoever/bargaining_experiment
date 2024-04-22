from otree.api import *


doc = """
Slider example
"""


class Constants(BaseConstants):
    name_in_url = "slider_2"
    players_per_group = 2
    num_rounds = 1
    BUYER_ROLE = 'Buyer'
    SELLER_ROLE = 'Seller'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    price = models.FloatField()
    number = models.IntegerField()

def creating_session(subsession):
    subsession.group_randomly()

# PAGES
class BuyerPage(Page):
    form_model = "player"
    form_fields = ["price", "number"]

    @staticmethod
    def live_method(player, data):
        print('received a bid from', player.id_in_group, ':', data)

    def live_method(player, data):
        player.price = data
        print(player.price)



class Results(Page):
    pass


page_sequence = [BuyerPage, Results]
