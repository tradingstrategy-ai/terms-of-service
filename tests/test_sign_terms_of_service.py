"""Tests covering Terms of Service module."""
import datetime
import random

import pytest
from ape.contracts import ContractInstance
from ape.exceptions import ContractLogicError
from ape_test import TestAccount
from hexbytes import HexBytes

from terms_of_service.acceptance_message import generate_acceptance_message, get_signing_hash


@pytest.fixture(scope="module")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def random_user(accounts):
    return accounts[1]


@pytest.fixture()
def tos(networks, project, deployer):
    with networks.parse_network_choice("ethereum:local"):
        yield deployer.deploy(project.TermsOfService, sender=deployer)


def test_not_signed(
    tos: ContractInstance,
    deployer: TestAccount,
    random_user: TestAccount,
):
    new_version = 1
    new_hash = random.randbytes(32)
    tos.updateTermsOfService(new_version, new_hash, sender=deployer)

    assert not tos.hasAcceptedHash(random_user, new_hash)
    assert not tos.hasAcceptedVersion(random_user, 1)
    assert not tos.canProceed(sender=random_user)


def test_signed(
    tos: ContractInstance,
    deployer: TestAccount,
    random_user: TestAccount,
):
    new_version = 1

    # Generate the message user needs to sign in their wallet
    signing_content = generate_acceptance_message(
        1,
        datetime.datetime.utcnow(),
        "http://example.com/terms-of-service",
        random.randbytes(32),
    )
    new_hash = get_signing_hash(signing_content)

    tos.updateTermsOfService(new_version, new_hash, sender=deployer)

    assert not tos.hasAcceptedHash(random_user, new_hash)
    assert not tos.hasAcceptedVersion(random_user, 1)
    assert not tos.canProceed(sender=random_user)

    signature = random_user.sign_message(signing_content).encode_rsv()
    metadata = b"XX"

    tx = tos.signTermsOfServiceOwn(new_hash, signature, metadata, sender=random_user)

    logs = list(tx.decode_logs(tos.Signed))
    assert len(logs) == 1
    assert logs[0].signer == random_user.address
    assert logs[0].version == new_version
    assert logs[0].hash == new_hash
    assert logs[0].metadata == b"XX"

    assert tos.canProceed(sender=random_user)


def test_sign_twice(
    tos: ContractInstance,
    deployer: TestAccount,
    random_user: TestAccount,
):
    new_version = 1
    new_hash = random.randbytes(32)
    tx = tos.updateTermsOfService(new_version, new_hash, sender=deployer)

