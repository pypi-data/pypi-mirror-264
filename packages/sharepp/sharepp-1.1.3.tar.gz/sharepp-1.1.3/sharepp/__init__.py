"""SharePriceProvider is a small application that provides the current price
in EUR for a given ISIN. """

from enum import Enum
import re
import requests
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter

EXTRA_ETF_URL = "https://extraetf.com/de/etf-profile/{isin}"
COIN_GECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
)
EURO_CURRENCY = "eur"


class SharePPError(Exception):
    pass


class Coin(Enum):
    """Enum representing all currently supported cryptocurrencies."""

    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    BINANCE_COIN = "binancecoin"
    TETHER = "tether"
    SOLANA = "solana"
    CARDANO = "cardano"
    RIPPLE = "ripple"
    USD_COIN = "usd-coin"
    POLKADOT = "polkadot"
    DOGECOIN = "dogecoin"


def get_etf_price(isin: str, rounded: bool = False, currency: str = "EUR") -> float:
    """
    Gets the current price in euro of a given ETF.

    :param isin: the ISIN of the ETF
    :return: the current price
    """
    if not is_isin(isin):
        raise SharePPError(
            "You must provide a string object representing a valid ISIN!"
        )

    response = requests.get(EXTRA_ETF_URL.format(isin=isin))
    if response.status_code != 200:
        raise SharePPError(
            f"No price information for ISIN {isin} could be found!", response
        )

    parsed_html = BeautifulSoup(response.text, "html.parser")
    price_span = parsed_html.find("div", class_="real-time-course-wrapper").find(
        "span", class_="ng-star-inserted"
    )
    price_string = price_span.text.replace(".", "").replace(",", ".")
    price_string = re.search(r"^\d+\.\d{2}", price_string).group()

    currency_converter = CurrencyConverter()
    price = currency_converter.convert(float(price_string), "USD", currency)

    if rounded:
        return round(price, 2)
    return price


def get_coin_price(coin: Coin) -> float:
    """
    Gets the current price in euro of a given cryptocurrency.

    :param coin: the cryptocurrency
    :return: the current price of the cryptocurrency
    """
    response = requests.get(
        COIN_GECKO_URL.format(coin=coin.value, currency=EURO_CURRENCY)
    ).json()
    return float(response[coin.value][EURO_CURRENCY])


def is_isin(isin: str) -> bool:
    """
    Checks whether a string is a valid ISIN or not.

    :param isin: the string to be checked
    :return: true if the given string is a valid ISIN, otherwise false
    """
    if re.match(r"^[A-Za-z]{2}[A-Za-z0-9]{10}", isin):
        return True
    else:
        return False
