# Example Code for MCDEX2 Perpetual Order Book

This example code shows how to:
* Keep track with the order book
* Show your margin balance
* Keep track with your active orders
* Place an order every 10 seconds at the index price
* Cancel all orders and quit after 5 orders

The default settings interacts with the Ropsten testnet. Try the Ropsten before moves to the Mainnet.

## Getting Started

1. Create an account in your MetaMask
2. Switch MetaMask to ropsten. Press "Deposit" button in the MetaMask to get some ETH from facuet
3. Goto [mcdex ropsten account page](https://ropsten.mcdex.io/account/wallet). Press "Deposit" button in mcdex
4. Goto [mcdex ropsten trade page](https://ropsten.mcdex.io/trade). Place a very small order, the website will prompt you to "set broker to the orderbook". You can close the modal window after the "set broker" progress
5. Checkout the example code
```
git clone https://github.com/mcdexio/example-perpetual-orderbook.py.git
cd example-perpetual-orderbook.py
pip install -r requirements.txt
```
6. Editing `settings.py`:
  * Set the private key (you may need [export the private key from MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key))
  * Confirm that you are going to connect to the ropsten
7. Run it `python mm.py`
8. You'll see the order book
9. The demo will place an order every 10 seconds at the index price
10. The demo will cancel all orders and quit after 5 orders

## Overview

Check [Orderbook API](https://mcdex.io/doc/api/) for details. The typical usage of Order Book API is:
* Connect to the [websocket](https://mcdex.io/doc/api/#api-endpoints). Subscribe a [Market channel](https://mcdex.io/doc/api/#market-channel), the channel will provide a snapshot of the order book immediately, then keep pushing changes.
* Login (by [signing a text message with your private key](TODO)) in the websocket and subscribe the [Trader channel](https://mcdex.io/doc/api/#trader-channel), the channel will push order changes.
* Fetch account's [balance](https://mcdex.io/doc/api/#available-balances) by reading API. The most important balances are `MarginBalance` and `AvailableMargin`. Check [Margin-Account Model](https://github.com/mcdexio/documents/blob/master/en/margin-account-model.md) for details.
* In order to place an order, call [Build Order](https://mcdex.io/doc/api/#build-order) and [Place Order](https://mcdex.io/doc/api/#place-order). The status of an order could be: `pending`, `partial_filled`, `full_filled`, `canceled`.

