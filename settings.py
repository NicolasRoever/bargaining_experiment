from os import environ

SESSION_CONFIGS = [
    dict(
    name = "bargain_live",
    app_sequence = ["bargain_live"],
    num_demo_participants=2,
    TA_treatment_high = True,
    delay_treatment_high = True,
    information_asymmetry = "None", # Which valuation is known? # Buyer, Seller or None
    treatment_communication = False,
    ),
    #dict(
    #    name="test",
    #    app_sequence=[
    #        "slider",
    #    ],
    #    num_demo_participants=2,
    #),
    #dict(
    #    name="slider",
    #    app_sequence=[
    #        "slider_2",
    #    ],
    #    num_demo_participants=2,
    #),
    #dict(
    #    name = "bargain_example",
    #    app_sequence = ["bargain_example"],
    #    num_demo_participants=2,
    #),
    #dict(
    #    name = "bargain_example_slider",
    #    app_sequence = ["bargain_example_slider"],
    #    num_demo_participants=2,
    #),
    #dict(
    #name = "bargain_example_orig2",
    #app_sequence = ["bargain_example_orig2"],
    #num_demo_participants=2,
    #)
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8603094593043'
