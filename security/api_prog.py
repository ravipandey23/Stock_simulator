import requests
import time

class Markit:
    def __init__(self):
        # self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json?input="
        # self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol="
        # self.lookup_url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords="
        # self.quote_url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=amzn&apikey=4V8L9IX444UZOSOA"
        self.quote_url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=amzn&apikey=4V8L9IX444UZOSOA"
        # self.lookup_url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=amzn&apikey=4V8L9IX444UZOSOA"
        self.lookup_url = "https://financialmodelingprep.com/api/v3/quote/AMZN?apikey=5fdd8554ae41dc8c10ad59fd3616e99c"

def get_company_sym(string):
    # url_concat = "http://dev.markitondemand.com/Api/v2/Lookup/json?input=" + string
    url_concat = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + string + "&apikey=4V8L9IX444UZOSOA"
    r = requests.get(url_concat)
    data = r.json()
    cnt=0
    lis=[]
    lis = data['bestMatches'][0]
    if r.status_code == 200:
        if len(lis) == 0:
            return False
        else:
            symbol = lis['1. symbol']
            return  symbol
    else:
        return False


def get_stock_price(string):
    none = 0.0
    if string is not None:
        string = string.upper()
        # url_concat = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol=" + string
        url_concat = "https://financialmodelingprep.com/api/v3/quote/"+string+"?apikey=5fdd8554ae41dc8c10ad59fd3616e99c"
        r = requests.get(url_concat)
        if r.status_code == 200:
            data = r.json()
            # lis = []
            # for key in data:
            #     if key!='Global Quote':
            #         return [None, none]
            # lis = data['Global Quote']
            # time.sleep(1.0)
            name = None
            price = 0.0
            # print(data)
            if len(data[0]) > 0:
                for key in data[0]:
                    if key == 'price':
                        price = float(data[0][key])
                    if key == 'name':
                        name = (data[0][key])
            return [name, price]
        else:
            print('\n\n\n')
            print('API STATUS CODE:' + str(r.status_code))
            print('\n\n\n')
            return [None, none]
    else:
        return [None, none]


def get_stock_change(string):
    none = 0.0
    if string is not None:
        string = string.upper()
        # url_concat = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol=" + string
        # url_concat = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + string + "&apikey=4V8L9IX444UZOSOA"
        url_concat = "https://financialmodelingprep.com/api/v3/quote/"+string+"?apikey=5fdd8554ae41dc8c10ad59fd3616e99c"
        r = requests.get(url_concat)
        if r.status_code == 200:
            data = r.json()
            price = 0.0
            per_ch = 0.0
            today_ch = 0.0
            if len(data[0]) > 0:
                for key in data[0]:
                    if key == 'price':
                        price = float(data[0][key])
                    if key == 'change':
                        today_ch = float(data[0][key])
                    if key == 'changesPercentage':
                        per_ch = float(data[0][key])
            return [price, today_ch,per_ch]
        else:
            print('\n\n\n')
            print('API STATUS CODE:' + str(r.status_code))
            print('\n\n\n')
            return [none, none, none]
    else:
        return [none, none, none]

def get_stock_details(string):
    none = 0.0
    name=""
    if string is not None:
        string = string.upper()
        print(string)
        # url_concat = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol=" + string
        # url_concat = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + string + "&apikey=4V8L9IX444UZOSOA"
        url_concat = "https://financialmodelingprep.com/api/v3/quote/"+string+"?apikey=5fdd8554ae41dc8c10ad59fd3616e99c"
        r = requests.get(url_concat)
        if r.status_code == 200:
            data = r.json()
            # print(data['Global Quote'])
            # for key in data:
            #     if key!='Global Quote':
            #         return [name, price, change, per_change, high, low]
            # lis = data['Global Quote']
            # print(data[0][])
            price = 0.0
            change =0.0
            per_change = 0.0
            high = 0.0
            low = 0.0
            # print(len(data))
            if len(data[0]) > 0:
                for key in data[0]:
                    if key == 'price':
                        price = (data[0][key])
                    if key == 'name':
                        name = (data[0][key])
                    if key == 'change':
                        change = float(data[0][key])
                    if key == 'changesPercentage':
                        per_change = float(data[0][key])
                    if key == 'dayHigh':
                        high = float(data[0][key])
                    if key == 'dayLow':
                        low = float(data[0][key])           
            print(name)
            print("\n")
            print(price)         
            return [name, price, change, per_change, high, low]
        else:
            print('\n\n\n')
            print('API STATUS CODE:' + str(r.status_code))
            print('\n\n\n')
            return [name, none, none, none, none, none]
    else:
        return [name, none, none, none, none, none]






if __name__ == "__main__":
    # get company info test
    # print(get_company_info('apple'))
    session.commit()
    # # get stock price test - returns name and price
    # print(get_stock_price('aapl'))
