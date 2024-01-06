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
    new_hash = random.randbytes(32)
    tos.updateTermsOfService(new_version, new_hash, sender=deployer)

    assert not tos.hasAcceptedHash(random_user, new_hash)
    assert not tos.hasAcceptedVersion(random_user, 1)
    assert not tos.canProceed(sender=random_user)


def test_sign_twice(
    tos: ContractInstance,
    deployer: TestAccount,
    random_user: TestAccount,
):
    new_version = 1
    new_hash = random.randbytes(32)
    tx = tos.updateTermsOfService(new_version, new_hash, sender=deployer)



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



