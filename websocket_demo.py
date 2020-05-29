from setting import PRIVATE_KEY, TARGET_NETWORK, PUBLIC_KEY
from wallet import Wallet

import websockets
import time
import json
import asyncio

websocket_url = ""
if TARGET_NETWORK == "ROPSTEN":
    websocket_url = "wss://ropsten.mcdex.io/ws"
elif TARGET_NETWORK == "MAINNET":
    websocket_url = "wss://mcdex.io/ws"
else:
    print("Error: unknown network.\n")

market_id = "ETHPERP"
wallet = Wallet(PRIVATE_KEY, PUBLIC_KEY)

async def listen_for_order_book():
    async with websockets.connect(websocket_url) as ws:
        subscribe_request = {
            "type": "subscribe",
            "channels": ["Market#" + market_id]
        }
        await ws.send(json.dumps(subscribe_request))
        while True:
            raw_msg = await asyncio.wait_for(ws.recv(), timeout=None)
            msg = json.loads(raw_msg)
            print(f"[orderbook ws] Receive {msg['type']} message:{msg}\n")

async def listen_for_account():
    async with websockets.connect(websocket_url) as ws:
        subscribe_request = {
            "type": "subscribe",
            "channels": ["TraderAddress#" + wallet.address]
        }
        timestamp = int(time.time() * 1000)
        signature = wallet.sign_hash(text=f"MAI-AUTHENTICATION@{timestamp}")
        login_request = {
            "type": "login",
            "maiAuth": f"{wallet.address}#MAI-AUTHENTICATION@{timestamp}#{signature}"
        }
        await ws.send(json.dumps(login_request))
        while True:
            raw_msg = await asyncio.wait_for(ws.recv(), timeout=None)
            msg = json.loads(raw_msg)
            print(f"[account ws] Receive {msg['type']} message:{msg}\n")
            if msg["type"] == "login":
                if msg["code"] == 0:
                    await ws.send(json.dumps(subscribe_request))
                else:
                    print(f"Websocket login failed.\n")

if __name__ == "__main__":
    tasks = asyncio.gather(listen_for_order_book(), listen_for_account())
    asyncio.get_event_loop().run_until_complete(tasks)

