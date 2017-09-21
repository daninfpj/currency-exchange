# Currency exchange worflow for Alfred 3

Convert between currencies (including Bitcoin) from Alfred using the `cur` keyword.

## Installation
- Grab the latest version from the [releases page](https://github.com/daninfpj/currency-exchange/releases/latest)

## Usage

- `cur USD EUR` - Shows the exchange rate between USD and EUR
- `cur USD` - Shows the exchange rate between USD and the default `to` currency
- `cur` — Shows the exchange rate between the default rates
- `cur 100 EUR USD` — Converts 100 EUR to USD
- `cur 100 EUR` — If you only type in one currency, it will convert from that to the deafult `to` currency
- `cur 100` — If you ommit currencies, it will convert between the default ones
- Press enter to copy the result to the clipboard

## Setting default currencies
- `cur from USD` — Sets the default `from` currency
- `cur to COP` — Sets the default `to` currency

## Credits

- Uses the [Alfred Workflow](https://github.com/deanishe/alfred-workflow) library 
- Partially inspired by [Currency Converter for Alfred 2](https://github.com/bigluck/alfred2-currencyconverter) (which no longer seems to work)
- Icon based on [Currency Exchange by Chanut is Industries from the Noun Project](https://thenounproject.com/search/?q=currency%20exchange&i=824774)
