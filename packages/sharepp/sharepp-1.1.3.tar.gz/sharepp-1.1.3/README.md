# SharePriceProvider

![Testing](https://github.com/Plebo13/sharepp/actions/workflows/test.yml/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fb03b5a446ae4a058e483c916e18d06c)](https://www.codacy.com/gh/Plebo13/sharepp/dashboard?utm_source=github.com&utm_medium=referral&utm_content=Plebo13/sharepp&utm_campaign=Badge_Grade)

## Installation

The best way to install SharePriceProvider is by using pip:
`pip install sharepp`

## Usage

To use SharePriceProvider simply import it into your python project. There are two main functions
available:

- get_etf_price: Returns the current price of an ETF
- get_coin_price: Returns the current price of a cryptocurrency

Supported coins:

- Bitcoin
- Ethereum
- Binance Coin
- Tether
- Solana
- Cardano
- Ripple
- USD Coin
- Polkadot
- Dogecoin

### Example

```python
import sharepp
from sharepp import Coin

print(sharepp.get_etf_price("LU1781541179"))
print(sharepp.get_coin_price(Coin.ETHEREUM))
```

The above example prints the current prices of the _Lyxor Core MSCI World ETF_
and the current price of Ethereum.
