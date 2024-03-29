# tradingcomdados

## Introduction
*Trading com Dados Library for quantitative finance*

The library consists of a collection of methods that can be used in order to help Data Scientists, Quantitative Analysts and data professionals during the development of quantitative finance applications. One of the main objectives of the library is to provide methods to connect to Trading com dados' data provider services.

## Library Motivation and Description
Trading com dados is an Edtech that provides educational content for people who want to know quantitative finance and in order to obtain that knowlegde, we need quality data, thus this library and our API service was created to solve that.

## API methods
-> get_data

-> get_data_tickers


## How to install
```python 
pip install tradingcomdados
```

## Machine Learning
This library has a few machine learning models that you can use in your daily activities.

With our lib, you can easily implement machine learning models to your daily activities in the financial market.

```python
from tradingcomdados import unsupervised_learning as ul

ul.clustering_pipeline()
```

## Alternative Data
You can obtain alternative data from the Brazilian Market using this library

Examples:
* Indexes, such as IBOV, IFIX but also S&P 500
* Economy sectors of companies listed in the Brazilian stock exchange


```python
from tradingcomdados import alternative_data as ad

# General function
ad.index_composition()

# Obtaining composition of IBOV
ad.index_composition('ibov')

# Obtaining sectors of Brazilian companies listed at B3
ad.get_sectors()

# Obtaining sector of a particular company
ad.get_sectors('PETR')

# Notice we are not using numbers at the end of tickers
ad.get_sectors('VALE')

```


## Funds Data
Fetches data of investment funds from the Brazilian Securities and Exchange Commission (CVM)


```python
from tradingcomdados import funds_data as fd

# Fetching daily data containing information such as quote value, number of investors, and so on
fd.get_funds_data()

# You can either leave it empty or specify a CNPJ
fd.get_funds_data('07.593.972/0001-86')


# Fetch the registration data of investment funds
fd.get_funds_info()

# You can either leave it empty or specify a CNPJ
fd.get_funds_info('07.593.972/0001-86')


```
