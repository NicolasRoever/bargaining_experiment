from otree.api import *

import datetime

doc = """
CLER payment app 1
"""


class C(BaseConstants):
    NAME_IN_URL = "clerpay_start"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Start(Page):
    @staticmethod
    def is_displayed(player):
        if "clerpay_amount" not in player.participant.vars:
            player.participant.vars["clerpay_amount"] = 0
            player.participant.vars["clerpay_start"] = datetime.datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            )

        return False


page_sequence = [Start]
