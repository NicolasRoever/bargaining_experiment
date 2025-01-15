from otree.api import *

import datetime
import requests
import random

doc = """
CLER payment app 2
"""


class C(BaseConstants):
    NAME_IN_URL = "clerpay_end"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    METHOD = "paypal"  # "sepa" or "paypal"

    with open(".clerpay_zahllauf") as f:
        ZAHLLAUF = f.read().strip()

    with open(".clerpay_credential") as f:
        CREDENTIAL = f.read().strip()


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ok = models.BooleanField(initial=False)
    code = models.StringField(blank=True)


def custom_export(players):
    clerpay_relevant = [
        k for k in players[0].participant.vars.keys() if k.startswith("clerpay_")
    ]
    yield ["participant.code"] + clerpay_relevant

    for player in players:
        if not player.ok:
            yield [player.participant.code] + [
                player.participant.vars[key] if key in player.participant.vars else ""
                for key in clerpay_relevant
            ]


# PAGES
class Format(Page):
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player):
        try:
            amount = float(str(player.participant.vars["clerpay_amount"]))
        except:
            return True

        return False

    @staticmethod
    def vars_for_template(player):
        return dict(noset="clerpay_amount" not in player.participant.vars)


class Auszahlung(Page):
    timeout_seconds = 4 * 60 * 60

    @staticmethod
    def is_displayed(player):
        if "clerpay_skip" in player.participant.vars:
            return False

        if "clerpay_code" not in player.participant.vars:
            player.participant.vars["clerpay_method"] = C.METHOD
            player.participant.vars["clerpay_credential"] = C.CREDENTIAL

            player.participant.vars[
                "clerpay_zahllauf"
            ] = f"{C.ZAHLLAUF}/{player.session.code}"

            player.participant.vars["clerpay_end"] = datetime.datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            )

            try:
                req = requests.get(
                    "https://lab.uni-koeln.de/auszahlung/new/",
                    params={
                        k[8:]: v
                        for k, v in player.participant.vars.items()
                        if k.startswith("clerpay_")
                    },
                )

                if req.ok and req.text.strip().isnumeric():
                    player.ok = True
                    player.participant.vars["clerpay_code"] = int(req.text.strip())
                else:
                    raise ValueError(
                        f"not ok: {req.ok}, {req.text.strip().isnumeric()}"
                    )
            except Exception as e:
                print(f"clerpay_end: request failed: {e}")

                player.ok = False

                player.code = str(37000000000 + random.randrange(0, 100000000))
                player.participant.vars["clerpay_code"] = player.code

        return True

    @staticmethod
    def vars_for_template(player):
        return dict(code=player.participant.vars["clerpay_code"])


class Ende(Page):
    @staticmethod
    def is_displayed(player):
        return "clerpay_skip" in player.participant.vars

    @staticmethod
    def vars_for_template(player):
        return dict(
            msg=player.participant.vars["clerpay_skip_msg"]
            if "clerpay_skip_msg" in player.participant.vars
            else ""
        )


page_sequence = [Format, Auszahlung, Ende]
