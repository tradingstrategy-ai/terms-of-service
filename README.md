# Terms Of Service Acceptance Manager

**Note**: This project is still under initial development,
and not ready yet. It's currently a frankenstein between Foundry and Ape.

A Solidity smart contract for making sure the smart contract caller
has accepted the latest terms of service.

## Use cases

- Record on-chain that users have accepted some sort of a disclaimer 
- Enforce users to accept disclaimers when they use with the smart contract
- User signs an [EIP-191 message](https://eips.ethereum.org/EIPS/eip-191) from their wallet
- Multisignature wallet and protocol friendly [EIP-1271](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol) is supported

## Requirements

- Python 3.10+
- Foundry

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
export POLYGONSCAN_API_KEY=
forge create \
  --rpc-url $JSON_RPC_POLYGON \
  --private-key $DEPLOY_PRIVATE_KEY \
  --etherscan-api-key $POLYGONSCAN_API_KEY \
  --verify \
  src/TermsOfService.sol:TermsOfService
```

#### PolygonScan verification failures with Forge 

Save the address. Because Polygonscan is a hard mistress and tends to crash, verify manually:

```shell
export CONTRACT_ADDRESS=0xDCD7C644a6AA72eb2f86781175b18ADc30Aa4f4d
scripts/verify-deployment.sh
```

### Initialising

[The INITIAL_ACCEPTANCE_MESSAGE placeholder terms of service message](./terms_of_service/acceptance_message.py) is used.


Get the hash of the message:

```shell
ipython 
```

```python
from terms_of_service.acceptance_message import INITIAL_ACCEPTANCE_MESSAGE, get_signing_hash
print(get_signing_hash(INITIAL_ACCEPTANCE_MESSAGE).hex())
```

```shell
export ACCEPTANCE_MESSAGE_HASH=808318f1c18ddfb861cd9755fe5005e3028f816039dc42a1b52e4f5031b645a4
export TERMS_OF_SERVICE_VERSION=1
export CONTRACT_ADDRESS=0xDCD7C644a6AA72eb2f86781175b18ADc30Aa4f4d
```

Then set the initial version:

```shell
cast send \
  --private-key $DEPLOY_PRIVATE_KEY \
  --rpc-url $JSON_RPC_POLYGON \
  $CONTRACT_ADDRESS \
  "updateTermsOfService(uint16,bytes32)" \
  $TERMS_OF_SERVICE_VERSION \
  $ACCEPTANCE_MESSAGE_HASH
```

## Deployment

A test deployment can be found on Polygon [0xDCD7C644a6AA72eb2f86781175b18ADc30Aa4f4d](https://polygonscan.com/address/0xDCD7C644a6AA72eb2f86781175b18ADc30Aa4f4d).

## More information

- [Join Discord for any questions](https://tradingstrategy.ai/community).
- [Watch tutorials on YouTube](https://www.youtube.com/@tradingstrategyprotocol)
- [Follow on Twitter](https://twitter.com/TradingProtocol)
- [Follow on Telegram](https://t.me/trading_protocol)
- [Follow on LinkedIn](https://www.linkedin.com/company/trading-strategy/)
