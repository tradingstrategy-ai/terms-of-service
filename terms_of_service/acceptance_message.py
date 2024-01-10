"""The default terms of service message that is signed.

- Uses EIP-151

- See `EthAccout.sign_message implementation <https://github.com/ethereum/eth-account/blob/b4883627557839bed906c89b93eec0fbbb017ec5/eth_account/account.py#L535>`__.
"""
import datetime

from eth_account.messages import encode_defunct, _hash_eip191_message

DEFAULT_ACCEPTANCE_MESSAGE_TEMPLATE = """
I read and agree on terms of service (version {version}) to use
smart contract software deployed on a blockchain.

The terms of service text was published {human_date} at {link}.
The unique identifier hash for this terms of service text was {hash}.
""".strip()

INITIAL_ACCEPTANCE_MESSAGE = """
I read and agree on terms of service (version 1) to use
smart contract software deployed on a blockchain.

The terms of service text was published 10.1.2024 at https://example.com.
The unique identifier hash for this terms of service text was 0x0000000000000000000000000000000000000000.
""".strip()


def generate_acceptance_message(
        version: int,
        date: datetime.datetime,
        link: str,
        hash: bytes,
        template=DEFAULT_ACCEPTANCE_MESSAGE_TEMPLATE):
    assert type(version) == int
    assert type(link) == str
    assert type(hash) == bytes
    assert len(hash) == 32, "Must be 256-bit sha of terms of service file"
    assert isinstance(date, datetime.datetime)
    human_date = date.strftime("%Y-%m-%d")
    return template.format(version=version, link=link, hash=hash.hex(), human_date=human_date)


def get_signing_hash(message: str) -> bytes:
    assert type(message) == str
    signable_message = encode_defunct(text=message)
    hash = _hash_eip191_message(signable_message)
    return hash


def get_initial_hash() -> bytes:
    """"""