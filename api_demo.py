from setting import PRIVATE_KEY, TARGET_NETWORK
from wallet import Wallet

import requests
import json
import time
import urllib
import random

api_url = ""
if TARGET_NETWORK == "ROPSTEN":
    api_url = "https://ropsten.mcdex.io/api"
elif TARGET_NETWORK == "MAINNET":
    api_url = "https://mcdex.io/api"
else:
    print("Error: unknown network.\n")

market_id = "ETHPERP"
wallet = Wallet(PRIVATE_KEY)
TIMEOUT = 5

def generate_auth_headers():
    timestamp = int(time.time() * 1000)
    signature = wallet.sign_hash(text=f"MAI-AUTHENTICATION@{timestamp}")
    return {"Mai-Authentication": f"{wallet.address}#MAI-AUTHENTICATION@{timestamp}#{signature}"}

def api_request(http_method, url, params=None, headers=None):
    if http_method.lower() == "get":
        if headers is None:
            headers = {"content-type": "application/x-www-form-urlencoded"}
        else:
            headers["content-type"] = "application/x-www-form-urlencoded"

        if params is None:
            params = ""
        else:
            params = urllib.parse.urlencode(params)
        response = requests.get(url, params, timeout=TIMEOUT, headers=headers)
        code = response.status_code
        if code == 200:
            return response.json()
        else:
            return {"status": "fail", "code": code}
    elif http_method.lower() == "post":
        if headers is None:
            headers = {"content-type": "application/json"}
        else:
            headers["content-type"] = "application/json"

        if params is not None:
            params = json.dumps(params)
        response = requests.post(url, params, timeout=TIMEOUT, headers=headers)
        code = response.status_code
        if code == 200:
            return response.json()
        else:
            return {"status": "fail", "code": code}
    elif http_method.lower() == "delete":
        response = requests.delete(url, headers=headers)
        code = response.status_code
        if code == 200:
            return response.json()
        else:
            return {"status": "fail", "code": code}

def get_balances():
    response_data = api_request("get", url=f"{api_url}/account/balances", params={"marketID": market_id}, headers=generate_auth_headers())
    print(f"[get balances response]{response_data}\n")

def get_active_orders():
    response_data = api_request("get", url=f"{api_url}/orders", params={"status": "pending"}, headers=generate_auth_headers())
    print(f"[get active orders response]{response_data}\n")

def build_unsigned_order(amount, price, side, order_type, expires, leverage):
    url = f"{api_url}/orders/build"
    headers = generate_auth_headers()
    params = {
        "amount": amount,
        "price": price,
        "side": side,
        "marketId": market_id,
        "orderType": order_type,
        "expires": expires,
        "targetLeverage": leverage
    }
    response_data = api_request('post', url=url, params=params, headers=headers)
    print(f"[build order response]{response_data}\n")
    return response_data["data"]["order"]

def place_order(amount, order_type, price, side, expires, leverage):
    unsigned_order = build_unsigned_order(amount=amount, price=price, side=side,
                                          order_type=order_type, expires=expires,
                                          leverage=leverage)
    order_id = unsigned_order["id"]
    signature = wallet.sign_hash(hexstr=order_id)
    signature = '0x' + signature[130:] + '0' * 62 + signature[2:130]
    params = {"orderID": order_id, "signature": signature, "method": 0}

    url = f"{api_url}/orders"
    response_data = api_request('post', url=url, params=params, headers=generate_auth_headers())
    print(f"[place order response]{response_data}\n")

def cancel_all_orders():
    url = f"{api_url}/orders"
    response_data = api_request('delete', url=url, params={"marketID": market_id}, headers=generate_auth_headers())
    print(f"[cancel all orders response]{response_data}\n")

if __name__ == "__main__":
    for i in range(5):
        get_balances()
        get_active_orders()
        time.sleep(5)
        side = "buy" if random.random() > 0.5 else "sell"
        place_order("10", "limit", "200", side, 300, "5")
        time.sleep(5)
    cancel_all_orders()

