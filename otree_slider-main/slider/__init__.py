from otree.api import *


doc = """
Slider example
"""


class Constants(BaseConstants):
    name_in_url = "slider"
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    price = models.FloatField()
    number = models.IntegerField()


# PAGES
class SliderPage(Page):
    form_model = "player"
    form_fields = ["price", "number"]


class Results(Page):
    pass


page_sequence = [SliderPage, Results]
