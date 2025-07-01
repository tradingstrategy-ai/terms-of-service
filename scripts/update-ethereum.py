"""Update terms of service"""

import os
import json
import sys
from pathlib import Path
from terms_of_service.acceptance_message import TRADING_STRATEGY_ACCEPTANCE_MESSAGE, get_signing_hash
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware, construct_sign_and_send_raw_middleware
from eth_account import Account


def get_abi_by_filename(fname: str) -> dict:
    """Reads a embedded ABI file and returns it.

    Example::

        abi = get_abi_by_filename("ERC20Mock.json")

    You are most likely interested in the keys `abi` and `bytecode` of the JSON file.

    Loaded ABI files are cache in in-process memory to speed up future loading.

    Any results are cached.

    :param web3: Web3 instance
    :param fname: `JSON filename from supported contract lists <https://github.com/tradingstrategy-ai/web3-ethereum-defi/tree/master/eth_defi/abi>`_.
    :return: Full contract interface, including `bytecode`.
    """

    here = Path(__file__).resolve().parent
    abi_path = here / ".." / "abi" / Path(fname)
    with open(abi_path, "rt", encoding="utf-8") as f:
        abi = json.load(f)
    return abi["abi"]


assert os.environ.get("DEPLOY_PRIVATE_KEY"), "Set DEPLOY_PRIVATE_KEY env"
assert os.environ.get("JSON_RPC_ETHEREUM"), "Set JSON_RPC_ETHEREUM env"
assert os.environ.get("CONTRACT_ADDRESS"), "Set $CONTRACT_ADDRESS env"
assert os.environ.get("TOS_DATE"), "Set $TOS_DATE env"

web3 = Web3(HTTPProvider(os.environ["JSON_RPC_ETHEREUM"]))
account = Account.from_key(os.environ["DEPLOY_PRIVATE_KEY"])
web3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

abi = get_abi_by_filename("TermsOfService.json")
Contract = web3.eth.contract(abi=abi)
contract = Contract(os.environ["CONTRACT_ADDRESS"])

current_version = contract.functions.latestTermsOfServiceVersion().call()
version = current_version + 1

date = os.environ["TOS_DATE"]
new_line_escaped_msg = TRADING_STRATEGY_ACCEPTANCE_MESSAGE.format(
    version=version,
    date=date,
)

acceptance_message_hash = get_signing_hash(new_line_escaped_msg)
acceptance_message = f"{new_line_escaped_msg}"
terms_of_service_version = str(version)
gas = web3.eth.get_balance(account.address) / 10**18

new_line = "\n"
escaped_new_line = "\\n"

print(f"Deployer: {account.address}")
print(f"Contract: {contract.address}")
print(f"Acceptance message: {acceptance_message.replace(new_line, escaped_new_line)}")
print(f"Acceptance hash: {acceptance_message_hash.hex()}")
print(f"Version: {version}")
print(f"Date: {date}")
print(f"Gas balance: {gas}")

confirm = input("Confirm send tx [y/n] ")
if confirm != "y":
    sys.exit(1)

tx_hash = contract.functions.updateTermsOfService(version, acceptance_message_hash, acceptance_message).transact({"from": account.address})
print("Confirming ", tx_hash.hex())
web3.eth.wait_for_transaction_receipt(tx_hash)
