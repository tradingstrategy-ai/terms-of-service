"""Deploy the contract."""

from ape import accounts, project


def main():
    account = accounts.load("deploy")
    print("Deploy account is", account.address)
    account.deploy(project.TermsOfService, publish=True)