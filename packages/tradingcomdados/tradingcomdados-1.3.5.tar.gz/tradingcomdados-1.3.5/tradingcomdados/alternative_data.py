import pandas as pd
import requests 
import zipfile  
import numpy as np

# Parsing data from IBOV


def _parse_ibov():

    try:

        url = "https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/IBOV.csv"
        df = pd.read_csv(
            url, encoding="latin-1", sep="delimiter", header=None, engine="python"
        )
        df = pd.DataFrame(df[0].str.split(";").tolist())

        return df

    except:

        print("An error occurred while parsing data from IBOV.")


def _standardize_ibov():

    try:

        df = _parse_ibov()
        df.columns = list(df.iloc[1])
        df = df[2:][["Código", "Ação", "Tipo", "Qtde. Teórica", "Part. (%)"]]
        df.reset_index(drop=True, inplace=True)

        return df

    except:

        print("An error occurred while manipulating data from IBOV.")


def _standardize_sp500():

    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

    df = table[0]

    return df


def _adapt_index(
    index: object, assets: object = "all", mode: object = "df", reduction: bool = True
):
    """
    This function processes the data from the latest composition of either IBOV or S&P 500. 
    
    Parameters
    ----------
    index : choose the index to be returned, if IBOV or S&P 500
    ativos : you can pass a list with the desired tickets. Default = 'all'.
    mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
    reduction: you can choose whether the result should come with the reduction and theorical quantitiy provided by B3. Default = True.
    
    """

    if index == "ibov":

        df = _standardize_ibov()

        if reduction == False:
            df = df[:-2]

        if assets != "all":
            df = df[df["Código"].isin(assets)]

        if mode == "list":
            df = list(df.Código)

    if index == "sp500":

        df = _standardize_sp500()

        if assets != "all":
            df = df[df["Symbol"].isin(assets)]

        if mode == "list":
            df = list(df.Symbol)

    return df


def index_composition(
    index: object, assets: object = "all", mode: object = "df", reduction: bool = True
):
    """
    This function captures the latest composition of either IBOV or S&P 500. It is updated every 4 months.
    
    Parameters
    ----------
    index : choose the index to be returned, if IBOV or S&P 500
    ativos : you can pass a list with the desired tickets. Default = 'all'.
    mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
    reduction: you can choose whether the result should come with the reduction and theorical quantitiy provided by B3. Default = True.
    
    """

    df = _adapt_index(index, assets, mode, reduction)

    return df


def get_sectors(ticker:object = None):
    """
    This function get the B3 listed companies' classification into economic and activity sectors.
    You can leave the parameter 'ticker' empty if you wish to return all companies, or 
    specify a ticker without the numbers at the end, for example: "PETR"
    
    Parameters
    ----------
    ticker : you can pass a specific company's ticker. Default = None. 

    """    

    url_dataset = r"https://www.b3.com.br/data/files/57/E6/AA/A1/68C7781064456178AC094EA8/ClassifSetorial.zip"

    download = requests.get(url_dataset)
    with open('ClassifSetorial.zip', "wb") as dataset_B3:
        dataset_B3.write(download.content)
    arquivo_zip = zipfile.ZipFile('ClassifSetorial.zip')
    dataset = arquivo_zip.open(arquivo_zip.namelist()[0])

    df = pd.read_excel(dataset, header = 6)

    #Rename df columns:  
    df.rename(columns = {'LISTAGEM': 'CÓDIGO', 'Unnamed: 4':'SEGMENTO B3'}, inplace = True)
    #Create a new column:
    df['NOME NO PREGÃO'] = df['SEGMENTO'].copy()
    # Delete empty rows and duplicates:
    df.dropna(subset = ['NOME NO PREGÃO'], inplace = True)
    indexNames = df[df['SETOR ECONÔMICO'] == 'SETOR ECONÔMICO'].index
    df.drop(indexNames, inplace=True)
    df['SEGMENTO'] = np.where(df['CÓDIGO'].isna(),df['NOME NO PREGÃO'],pd.NA )    
    df['SETOR ECONÔMICO'] = df['SETOR ECONÔMICO'].ffill()
    df['SUBSETOR'] = df['SUBSETOR'].ffill()
    df['SEGMENTO'] = df['SEGMENTO'].ffill()
    df.dropna(subset = ['CÓDIGO'], inplace = True)
    
    #reset index:
    df.reset_index(drop=True, inplace=True)

    #
    df = df[['SETOR ECONÔMICO','SUBSETOR','SEGMENTO','NOME NO PREGÃO','CÓDIGO','SEGMENTO B3']]

    if ticker == None:
        df = df

    else:
        ticker = ticker[:4]
        df = df[df['CÓDIGO'] == ticker]

    return df
