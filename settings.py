from os import environ
import pandas as pd

import pathlib

SOURCE_DIR = pathlib.Path(__file__)

SESSION_CONFIGS = [
    dict(
    name = "bargain_live",
    app_sequence = ["bargain_live"],
    num_demo_participants=8,
    number_of_groups = 1, 
    TA_treatment_high = True,
    delay_treatment_high = False,
    information_asymmetry = "Buyer", # Which valuation is known? # Buyer, Seller or None
    treatment_communication = False,
    termination_treatment = 'high_prob', # 'low_prob' or 'high_prob'
    doc="""
    Adjust the number of groups dependent on the number of participants. There are 8 participants per group."""
    )
    
]
    


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=20.00, doc=""
)

PARTICIPANT_FIELDS = [
    'random_round',
]

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8603094593043'
