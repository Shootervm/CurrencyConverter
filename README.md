# CurrencyConverter

## Parameters
 - `-h, --help` show this help message and exit
 - `--amount AMOUNT, -a AMOUNT`
  - Amount of imputed currency, that will be calculated by conversion rate/rates
 - `--input_currency INPUT_CURRENCY, -i INPUT_CURRENCY`
  - Input currency (3 letters [Code ISO 4217] or currency
  symbol)
 - `--output_currency OUTPUT_CURRENCY [OUTPUT_CURRENCY ...], -o OUTPUT_CURRENCY [OUTPUT_CURRENCY ...]`
  - Requested/Output currency (3 letters [Code ISO 4217] or currency symbol)
  - If missing all know currencies will be outputted

## Functionality

## Output
- json with following structure.
```
{
    "input": { 
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```
## Examples
​
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{   
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2707.36, 
    }
}
```

```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{   
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20, 
    }
}
```

```
./currency_converter.py --amount 10.92 --input_currency £ 
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```
