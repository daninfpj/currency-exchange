# Currency exchange worflow for Alfred 2 and 3

Convert between currencies (including Bitcoin) from Alfred using the `cur` keyword.

## Installation
- Grab the latest version from the [releases page](https://github.com/daninfpj/currency-exchange/releases/latest)

## Usage

- `cur USD EUR` - Shows the exchange rate between USD and EUR
- `cur USD` - Shows the exchange rate between USD and the default `to` currency
- `cur` — Shows the exchange rate between the default rates
- `cur 100 EUR USD` — Converts 100 EUR to USD
- `cur 100 EUR` — If you only type in one currency, it will convert from that to the default `to` currencies
- `cur 100` — If you omit currencies, it will convert between the default ones
- Press enter to copy the result to the clipboard

## Setting default currencies
- `cur from USD` — Sets the default `from` currency
- `cur to COP` — Sets the default `to` currency
- `cur to COP EUR` — Sets the default `to` currencies to COP and EUR
