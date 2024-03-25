import argparse

from sharepp import SharePPError, get_etf_price


def run():
    parser = argparse.ArgumentParser(
        prog="sharepp",
        description="""SharePriceProvider is a small application
         that provides the current price in EUR for a given ISIN.""",
    )
    subparsers = parser.add_subparsers(
        title="command", help="Command to execute", dest="command", required=True
    )

    # create the parser for the "etf-price" command
    share_price = subparsers.add_parser(
        "etf-price", help="Get the current price for an ETF"
    )
    share_price.add_argument("--isin", help="The ISIN of the ETF", required=True)
    args = parser.parse_args()

    if args.command == "etf-price":
        try:
            price = get_etf_price(args.isin)
            print(f"{price:.2f}€")
        except SharePPError as e:
            print(e)
