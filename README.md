# Terms Of Service Acceptance Manager

**Note**: This project is still under initial development,
and not ready yet.

A Solidity smart contract for making sure the smart contract caller
has accepted the latest terms of service.

## Use cases

- Record on-chain that users have accepted some sort of a disclaimer 
- Enforce users to accept disclaimers when they use with the smart contract
- User signs an [EIP-191 message](https://eips.ethereum.org/EIPS/eip-191) from their wallet
- Multisignature wallet and protocol friendly [EIP-1271](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol) is supported

## Requirements

- Python 3.10+

## Workflow

### Deploying

Deploy [TermsOfService smart contract](./contracts/TermsOfService.sol) for your chain

- Each deployment has its own smart contract address
- Each chain needs its own deployment
- Each TermsOfService tracks the currently active terms of service text

### Updating terms of service

Creating terms of service

- Create a Markdown/plain text terms of service file
  - Must be dated
  - Must have a version number counter start from 1, then 2
  - Record SHA-256 bit hash of the text 
- Use update script to bump the new terms of service live

### Users to sign the terms of service

- The smart contract has `canProceed` function to check if a 
  particular address has signed the latest terms of service version
- The user signs a [template message](./terms_of_service/acceptance_message.py)
  with their wallet. Note that this message only refers to the actual 
  terms of service based on its version, hash, date and link,
- The address must have always signed the latest terms of service,
  and should be prompted to sign again if this is not the case
- The terms of service signing payload can be passed part 
  as another smart contract transaction, and **does not** need
  to be a separate transaction

On hashes: There are two hashes. One for the actual terms of service
file (never referred in the smart contracts) and one for the message
(template-based) that users need to sign with their wallet.

## Getting started

Install framework with Poetry:

```
poetry install
```

## Compiling

```shell
poetry shell
ape compile
```

## Running tests

```shell
poetry shell
ape test
```

## Deploying

Using Foundry.

Compile:

```shell
forge build
```

Then:

```shell 
export DEPLOY_PRIVATE_KEY=
export JSON_RPC_POLYGON=
forge create --rpc-url $JSON_RPC_POLYGON --private-key $DEPLOY_PRIVATE_KEY contracts/TermsOfService.sol:TermsOfService
```

### Initialising

The following placeholder terms of service message is used.

```

```



## More information

- [Join Discord for any questions](https://tradingstrategy.ai/community).
- [Watch tutorials on YouTube](https://www.youtube.com/@tradingstrategyprotocol)
- [Follow on Twitter](https://twitter.com/TradingProtocol)
- [Follow on Telegram](https://t.me/trading_protocol)
- [Follow on LinkedIn](https://www.linkedin.com/company/trading-strategy/)
