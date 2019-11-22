from django.conf import settings

BTC = "bitcoin"
LTC = "litecoin"
ETH = "ethereum"
DASH = "dash"
BCH = "bitcoincash"
XRP = "xrp"
LTCT = "litecointestnet"

USD = "USD"
EUR = "EUR"

CURRENCY_CHOICES = (
    (LTC, 'Litecoin'),
    (BTC, 'Bitcoin'),
    (DASH, 'Dash'),
    (BCH, 'Bitcoin Cash'),
    (XRP, 'XRP'),
    (ETH, 'Ethereum'),
    (LTCT, 'Litecoin Testnet')
)

STANDARD_CURRENCY_CHOICES = (
    (USD, 'US Dollars'),
    (EUR, 'European Pounds'),
)


def get_coins_list():
    coins = getattr(settings, 'ALFACOINS_ACCEPTED_COINS', None)
    if not coins:
        coins = CURRENCY_CHOICES
    return coins


def get_standard_currency():
    currencies = STANDARD_CURRENCY_CHOICES
    return currencies
