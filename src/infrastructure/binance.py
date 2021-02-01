import hmac
import time
import hashlib
import requests
import json
from urllib.parse import urlencode
import datetime as dt
import concurrent.futures
from decimal import Decimal
import pandas as pd


class EncryptedRequest():
    """ 
    EncryptedRequest(KEY, SECRET, BASE_URL)
    
    Provide the api key and secret key, and it's ready to go
    Because USER_DATA endpoints require signature:
    - call `send_signed_request` for USER_DATA endpoints
    - call `send_public_request` for public    endpoints
    """
    
    def __init__(self, KEY, SECRET, BASE_URL):
        self.__KEY = KEY
        self.__SECRET = SECRET
        self.BASE_URL = BASE_URL
        
    def hashing(self, query_string):
        return hmac.new(self.__SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    
    def dispatch_request(self, http_method):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.__KEY
        }) 
        return {
            'GET': session.get,
            'DELETE': session.delete,
            'PUT': session.put,
            'POST': session.post,
        }.get(http_method, 'GET')
        
    def get_timestamp(self):
        res = requests.get("https://fapi.binance.com/fapi/v1/time")
        res_json = res.json()
        server_time = res_json['serverTime']
        return server_time

    # used to send a request that requires a signature
    def send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload)
        # replace single quote to double quote
        query_string = query_string.replace('%27', '%22')
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())

        url = self.BASE_URL + url_path + '?' + query_string + '&signature=' + self.hashing(query_string)
        params = {'url': url, 'params': {}}
        response = self.dispatch_request(http_method)(**params)
        return response.json()

    # used to send a request that doesn't requires a signature
    def send_public_request(self, url_path, payload={}):
        query_string = urlencode(payload, True)
        url = self.BASE_URL + url_path
        if query_string:
            url = url + '?' + query_string
        response = self.dispatch_request('GET')(url=url)
        return response.json()

class Binance(EncryptedRequest):
    """
    Binance(KEY, SECRET) deals with master account related operations.
    
    KEY    : master acccount's api key
    SECRET : master acccount's secret key
    """
    BASE_URL = 'https://api.binance.com' 

    def __init__(self, KEY, SECRET):
        super().__init__(KEY, SECRET, Binance.BASE_URL)

    def get_sub_account_list(self):
        """
        Returns a sub acocunt list in descending order of creation time.
        """
        end_point = "/sapi/v1/broker/subAccount"
        response = self.send_signed_request('GET', end_point)
        return response
    
    def get_sub_account_email(self, sub_account_id):
        sub_account_email = None
        sub_account_list = self.get_sub_account_list()
        
        for account in sub_account_list[::-1]:
            if account['subaccountId'] == sub_account_id:
                sub_account_email = account['email']
                break

        return sub_account_email
    
    def create_sub_account(self):
        end_point = "/sapi/v1/broker/subAccount"

        response = self.send_signed_request('POST', end_point)
        return response

    def create_sub_account_api_key(self, sub_account_id):
        end_point = "/sapi/v1/broker/subAccountApi"
        params = {
            "subAccountId" : sub_account_id,
            "canTrade" : "true"
            # "marginTrade" : "true",
            # "futuresTrade" : "true"
        }
        response = self.send_signed_request('POST', end_point, params)
        return response

    def get_sub_account_deposit_address(self, email, coin, network):
        end_point = "/sapi/v1/capital/deposit/subAddress"
        params = {
            "email" : email,
            "coin" : coin,
            "network" : network
        }
        response = self.send_signed_request('GET', end_point, params)
        return response
    
    def get_sub_account_info(self, sub_account_id=None):
        end_point = "/sapi/v1/broker/subAccount"
        if sub_account_id:
            params = {"subAccountId" : sub_account_id}
            response = self.send_signed_request('GET', end_point, params)
        else:
            response = self.send_signed_request('GET', end_point)
        return response
        
    def get_sub_account_asset(self, email):
        end_point = "/wapi/v3/sub-account/assets.html"
        params = {
            "email":email
        }
        
        response = self.send_signed_request("GET", end_point, params)
        return response
    
    def intra_account_transfer(self, email, asset, amount, tr_type=2):
        """
        tr_type
        1: transfer from sub-account's spot account to its USDT-margined futures account 
        2: transfer from sub-account's USDT-margined futures account to its spot account 
        3: transfer from sub-account's spot account to its COIN-margined futures account 
        4: transfer from sub-account's COIN-margined futures account to its spot account
        """
        end_point = "/sapi/v1/sub-account/futures/transfer"
        params = {
            "email":email,
            "asset":asset,
            "amount":amount,
            "type":tr_type
        }

        response = self.send_signed_request('POST', end_point, params)
        return response     
    
    def inter_account_transfer(self, from_id, to_id, asset, amount, tr_type="SPOT"):
        """
        Parameters
            fromId : giver sub-account Id
            toId : receiver sub-account Id
            asset : transferring asset symbol
            amount : the amount of the asset to be transferred.
            tr_type : "SPOT" or "FUTURES"
        """
        if tr_type == "FUTURES":
            end_point = "/sapi/v1/broker/transfer/futures"
            params = {
                "fromId": from_id,
                "toId": to_id,
                "futuresType":1,
                "asset": asset,
                "amount":amount
            }
        elif tr_type == "SPOT":
            end_point = "/sapi/v1/broker/transfer"
            params = {
                "fromId": from_id,
                "toId": to_id,
                "asset": asset,
                "amount":amount
            }

        response = self.send_signed_request('POST', end_point, params)
        return response
    
    def external_withdraw(self, asset, address, network, amount):
        end_point = "/sapi/v1/capital/withdraw/apply"
        params = {
            "coin":asset,
            "address":address,
            "amount":amount,
            "network":network
        }
        
        response = self.send_signed_request('POST', end_point, params)
        return response
    
    def get_withdrawal_history(self, **kwargs):
        """
        get_withdrawal_history(**kwargs)
        
        Optional Parameters
        asset     
        status    : 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6:Completed)
        startTime : Default: 90 days from current timestamp
        endTime   : Default: current timestamp
        """
        end_point = "/sapi/v1/capital/withdraw/history"
        params = {key : value for key, value in kwargs.items()}
        res = self.send_signed_request('GET', end_point, params)
        return res
    
    def get_order_amt_unit(self, symbol):
        # There is minimum order "price" unit in terms of USDT(BTC etc.)
        number_of_below_zero = {"BTCUSDT": 6, "ETHUSDT": 3, "XRPUSDT": 1}
        return number_of_below_zero[symbol]

    def get_order_prc_unit(self, symbol):
        # There is minimum order "amount" unit in terms of the base asset(BTC etc.)
        number_of_below_zero = {"BTCUSDT": 2, "ETHUSDT": 2, "XRPUSDT": 4}
        return number_of_below_zero[symbol]
    
    def get_order_book(self, symbol='BTCUSDT'):
        end_point="/api/v3/depth"
        params = {"symbol":symbol}
        response = self.send_public_request(end_point, params)
        print(response)
        return response
    
    def get_mid_price(self, symbol='BTCUSDT'):
        order_book = self.get_order_book(symbol)
        bids = order_book['bids']
        asks = order_book['asks']

        bids_highest_prc = bids[0][0]
        asks_lowest_prc = asks[0][0]
        prc_unit = self.get_order_prc_unit(symbol)

        mid_prc = Decimal(0.5) * (Decimal(bids_highest_prc) + Decimal(asks_lowest_prc))
        rounded_mid_prc = round(mid_prc, prc_unit)
        return rounded_mid_prc
    
    def make_market_order(self, symbol, side, base_qty=0):
        """
        Parameters
         symbol   : a market symbol of the trading asset.
         side     : BUY or SELL
         base_qty : the number of units to trade in terms of the base asset.
        """
        order_type="MARKET"
        order_amt_unit = self.get_order_amt_unit(symbol)
        order_amt = round(base_qty, order_amt_unit)
        
        end_point = "/api/v3/order"
        params = {
            "symbol":symbol,
            "side" : side,
            "type" : order_type,
            "quantity" : order_amt
        }
        response = self.send_signed_request("POST", end_point, params)
        return response
    
    def make_limit_order(self, symbol, price, base_qty, price_buffer_rate=0):
        """
        Whether to 'buy' or 'sell' is automatically determined.
        For example, if the price parameter's value is higher than the current market price,
        'SELL' side order is created and delivered to the server.
        
        Parameters
            symbol : what kind of contract to be traded.
            price  : USDT
            base_qty : the number of units to trade in terms of the base asset.
            price_buffer_rate : depending on an order side, lower or raise order price.
        """
        end_point = "/fapi/v1/order"
        
        if base_qty > 0:
            side = "BUY"
            price_buffer = -1 * price * price_buffer_rate
        else:
            side = "SELL"
            price_buffer = price * price_buffer_rate
            
        order_amt_unit = self.get_order_amt_unit(symbol)
        order_prc_unit = self.get_order_prc_unit(symbol)
        
        order_amt = round(base_qty, order_amt_unit)
        order_prc = round(price + price_buffer, order_prc_unit)
        
        params = {
            "symbol":symbol,
            "side" : side,
            "quantity": abs(order_amt),
            "price":order_prc,
            "type" :"LIMIT",
            "timeInForce":"GTC",
            }
        
        response = self.send_signed_request("POST", end_point, params)
        datetime_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{datetime_now} : {symbol} {abs(order_amt)} {side} contract at ${order_prc} ")
        return response
    
    
class BinanceFutures(EncryptedRequest):
    """
    BTCUSDT, ETHUSDT, XRPUSDT pairs are tradable.
    """    
    BASE_URL = 'https://fapi.binance.com' # production base url
    
    def __init__(self, KEY, SECRET):
        super().__init__(KEY, SECRET, self.BASE_URL)
    
    def get_timestamp(self):
        response = self.send_public_request('/fapi/v1/time')
        timestamp = response['serverTime']
        return timestamp
    
    def get_account_info(self):
        end_point = "/fapi/v2/account"
        response = self.send_signed_request("GET", end_point)
        return response

    def get_position_info(self, symbol):
        end_point = "/fapi/v2/positionRisk"
        params = {
            "symbol":symbol
        }
        response = self.send_signed_request("GET", end_point, params)[0]
        
        positions =  self.get_account_info()['positions']
        position = next(position for position in positions if  position["symbol"] == symbol)

        response['leverage'] = position['leverage']
        response['unrealizedProfit'] = position['unrealizedProfit']
        response['maintMargin'] = position['maintMargin']    
        return response
    
    def get_balance_info(self):
        end_point = "/fapi/v2/balance"
        response = self.send_signed_request("GET", end_point)
        return response
