# Example Code for MCDEX2 Perpetual Order Book

This example code shows how to:
* keep track with the order book
* show your margin balance
* keep track with your active orders
* place an order every 10 seconds at the index price
* cancel all orders and quit after 5 orders

The default settings interacts with the Ropsten testnet. Try the Ropsten before moves to the Mainnet.

## Getting Started

1. Create an account in your MetaMask
2. Switch MetaMask to ropsten. Press "Deposit" button in the MetaMask to get some ETH from facuet
3. Goto (mcdex ropsten account page)[https://ropsten.mcdex.io/account/wallet]. Press "Deposit" button in mcdex
4. Goto (mcdex ropsten trade page)[https://ropsten.mcdex.io/trade]. Place a very small order, the website will prompt you to "set broker to the orderbook". You can close the modal window after the "set broker" progress
5. Checkout the example code
```
git clone https://github.com/mcdexio/example-perpetual-orderbook.py.git
cd example-perpetual-orderbook.py
pip install -r requirements.txt
```
6. Editing `settings.py`:
  * Set the private key (you may need (export the private key from MetaMask)[https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key])
  * Confirm that you are going to connect to the ropsten
7. Run it `python mm.py`
8. You'll see the order book
9. The demo will place an order every 10 seconds at the index price
10. The demo will Cancel all orders and quit after 5 orders

