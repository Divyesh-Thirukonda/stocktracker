import requests
import os
from dotenv import load_dotenv

load_dotenv()  # This loads variables from the .env file into the environment

nytArticleAPI = os.getenv('nytArticleAPI')
alphavantageapi = os.getenv('alphavantageapi')
twelveapi = os.getenv('twelveapi')

def fetch_nyt_article_title():
    url = "https://api.nytimes.com/svc/topstories/v2/business.json"
    params = {
        "api-key": nytArticleAPI
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        titles = "          |          ".join([article['title'] for article in data['results']])
        return titles
        # data = response.json()
        # return data['results'][0]['title']
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
    
def fetch_forex():
    forexUrl = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json" # https://github.com/fawazahmed0/exchange-api
    forexResponse = requests.get(forexUrl)

    if forexResponse.status_code == 200:
        # Parse the JSON response
        return forexResponse.json()
    else:
        # Print the status code if the request was unsuccessful
        print(f"Failed to retrieve data. Status code: {forexResponse.status_code}")
        return [0, 0, 0, 0, 0]
    
def fetch_gainLose():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={alphavantageapi}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        # Print the status code if the request was unsuccessful
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return [0, 0, 0, 0, 0]
        

def fetch_searchResults(keyword):
    '''
    {
    "data": [
        {
        "symbol": "HOOD",
        "instrument_name": "Robinhood Markets, Inc.",
        "exchange": "NASDAQ",
        "mic_code": "XNGS",
        "exchange_timezone": "America/New_York",
        "instrument_type": "Common Stock",
        "country": "United States",
        "currency": "USD"
        },
        {
        "symbol": "HOOD",
        "instrument_name": "Robinhood Markets, Inc.",
        "exchange": "BMV",
        "mic_code": "XMEX",
        "exchange_timezone": "America/Swift_Current",
        "instrument_type": "Common Stock",
        "country": "Mexico",
        "currency": "MXN"
        }
    ],
    "status": "ok"
    }
    '''

    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={alphavantageapi}"
    url = f"https://api.twelvedata.com/symbol_search?symbol={keyword}&apikey={twelveapi}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        
        data = response.json()['data']
        # Filter results where country is United States
        filtered_data = [item for item in data if item['country'] == 'United States']
        return filtered_data
        # return response.json()['data']
    
    else:
        # Print the status code if the request was unsuccessful
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return []
    
def fetch_companyOverview(ticker):
    '''
    "Symbol": "IBM",
    "Name": "International Business Machines",
    "Exchange": "NYSE",
    "MarketCapitalization": "180637139000",
    "EBITDA": "14625000000",
    "PERatio": "21.64",
    "PEGRatio": "4.039",
    "BookValue": "26.08",
    "DividendPerShare": "6.65",
    "DividendYield": "0.0341",
    "EPS": "9.06",
    '''

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={alphavantageapi}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return {
            "symbol": data.get("Symbol") or 'AAPL',
            "name": data.get("Name") or "Apple Inc",
            "exchange": data.get("Exchange") or "NASDAQ",
            "MarketCapitalization": data.get("MarketCapitalization") or 0,
            "EBITDA": data.get("EBITDA") or 0,
            "PERatio": data.get("PERatio") or 0,
            "PEGRatio": data.get("PEGRatio") or 0,
            "BookValue": data.get("BookValue") or 0,
            "DividendPerShare": data.get("DividendPerShare") or 0,
            "DividendYield": data.get("DividendYield") or 0,
            "EPS": data.get("EPS") or "0",
        }
    
    else:
        # Print the status code if the request was unsuccessful
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return {}
    
# fetch graph at some point
  
def fetch_companyQuote(ticker):
    '''
    "01. symbol": "IBM",
    "02. open": "196.7900",
    "03. high": "197.3800",
    "04. low": "194.3900",
    "05. price": "196.1000",
    "06. volume": "2321961",
    "07. latest trading day": "2024-08-23",
    "08. previous close": "195.9600",
    "09. change": "0.1400",
    "10. change percent": "0.0714%"
    '''

    # url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={alphavantageapi}"
    url = f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={twelveapi}&source=docs"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json() # .get("Global Quote", {})
        return {
            "symbol": data.get("symbol") or 'AAPL',
            "name": data.get("name") or "Apple Inc",
            "exchange": data.get("exchange") or "NASDAQ",
            "open": data.get("open") or 0,
            "high": data.get("high") or 0,
            "low": data.get("low") or 0,
            "price": data.get("close") or 0,
            "volume": data.get("volume") or 0,
            # "latest_trading_day": data.get("07. latest trading day") or 0,
            "previous_close": data.get("previous_close") or 0,
            "change": data.get("change") or 0,
            "change_percent": data.get("percent_change") or "0",
        }
    else:
        # Print the status code if the request was unsuccessful
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return {
            "symbol": "AAPL",
            "open": "0",
            "high": "0",
            "low": "0",
            "price": "0",
            "volume": "0",
            "latest_trading_day": "0",
            "previous_close": "0",
            "change": "0",
            "change_percent": "0",
        }
    