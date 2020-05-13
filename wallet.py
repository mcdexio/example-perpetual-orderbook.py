from eth_account import Account
from eth_account.messages import defunct_hash_message

class Wallet:
    def __init__(self, private_key):
        self._account = Account.privateKeyToAccount(private_key)

    def sign_hash(self, text=None, hexstr=None):
        msg_hash = defunct_hash_message(hexstr=hexstr, text=text)
        signature_dict = self._account.signHash(msg_hash)
        signature = signature_dict["signature"].hex()
        return signature

    @property
    def address(self) -> str:
        return self._account.address

