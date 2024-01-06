"""Tests covering Terms of Service module."""
import random

import pytest
from ape.contracts import ContractInstance
from ape.exceptions import ContractLogicError
from ape_test import TestAccount
from hexbytes import HexBytes


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


def test_start_zero_version(tos: ContractInstance):
    assert tos.latestTermsOfServiceVersion() == 0
    assert tos.latestTermsOfServiceHash() == HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000')


def test_first_terms_of_service(tos: ContractInstance, deployer: TestAccount):
    new_version = 1
    new_hash = random.randbytes(32)
    tx = tos.updateTermsOfService(new_version, new_hash, sender=deployer)
    assert tos.latestTermsOfServiceVersion() == 1
    assert tos.latestTermsOfServiceHash() == new_hash

    # https://academy.apeworx.io/articles/testing
    logs = list(tx.decode_logs(tos.UpdateTermsOfService))
    assert len(logs) == 1
    assert logs[0].version == new_version
    assert logs[0].textHash == new_hash

    assert tos.getTextHash(new_version) == new_hash


def test_second_terms_of_service(tos: ContractInstance, deployer: TestAccount):
    new_version = 1
    new_hash = random.randbytes(32)
    tos.updateTermsOfService(new_version, new_hash, sender=deployer)
    assert tos.latestTermsOfServiceVersion() == 1
    assert tos.latestTermsOfServiceHash() == new_hash

    new_version = 2
    new_hash = random.randbytes(32)
    tos.updateTermsOfService(new_version, new_hash, sender=deployer)
    assert tos.latestTermsOfServiceVersion() == 2
    assert tos.latestTermsOfServiceHash() == new_hash


def test_wrong_owner(tos: ContractInstance, random_user: TestAccount):
    new_version = 1
    new_hash = random.randbytes(32)

    with pytest.raises(ContractLogicError):
        tos.updateTermsOfService(new_version, new_hash, sender=random_user)

    assert tos.latestTermsOfServiceVersion() == 0


def test_wrong_version(tos: ContractInstance, deployer: TestAccount):
    new_version = 2
    new_hash = random.randbytes(32)

    with pytest.raises(ContractLogicError):
        tos.updateTermsOfService(new_version, new_hash, sender=deployer)

    assert tos.latestTermsOfServiceVersion() == 0


def test_hash_reuse(tos: ContractInstance, deployer: TestAccount):
    new_version = 1
    new_hash = random.randbytes(32)
    tos.updateTermsOfService(new_version, new_hash, sender=deployer)

    new_version = 2
    with pytest.raises(ContractLogicError):
        tos.updateTermsOfService(new_version, new_hash, sender=deployer)


def test_transfer_ownership(tos: ContractInstance, deployer: TestAccount, random_user: TestAccount):
    tos.transferOwnership(random_user, sender=deployer)
    assert tos.owner() == random_user


def test_transfer_ownership_only_owner(tos: ContractInstance, deployer: TestAccount, random_user: TestAccount):
    with pytest.raises(ContractLogicError):
        tos.transferOwnership(random_user, sender=random_user)



