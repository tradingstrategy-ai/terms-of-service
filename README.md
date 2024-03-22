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
# TODO: there is a bug in pytest/ape test that it does not find the tests
# unless you explicitly pass it the tests folder
ape test tests
```

## Deploying

Using Foundry.

Compile:

```shell
foundry up
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
export CONTRACT_ADDRESS=0xbe1418df0bAd87577de1A41385F19c6e77312780
scripts/verify-deployment.sh
```

### Initialising

[The INITIAL_ACCEPTANCE_MESSAGE placeholder terms of service message](./terms_of_service/acceptance_message.py) is used.


Get the hash of the message:

```shell
ipython 
```

Then type `%cpaste` and copy-paste in:

```python
from terms_of_service.acceptance_message import INITIAL_ACCEPTANCE_MESSAGE, get_signing_hash
new_line_escaped_msg = INITIAL_ACCEPTANCE_MESSAGE.replace("\n", "\\n")
print("Paste to your shell:")
print("")
print(f"""export ACCEPTANCE_MESSAGE_HASH={get_signing_hash(INITIAL_ACCEPTANCE_MESSAGE).hex()}""")
print(f"""export ACCEPTANCE_MESSAGE="{new_line_escaped_msg}" """)
````

```shell
export ACCEPTANCE_MESSAGE_HASH=  # Copy from above output
export ACCEPTANCE_MESSAGE=  # Copy from above output
export TERMS_OF_SERVICE_VERSION=1
export CONTRACT_ADDRESS=0xbe1418df0bAd87577de1A41385F19c6e77312780  # Set your deployed contract
```

Then set the initial version:

```shell
cast send \
  --private-key $DEPLOY_PRIVATE_KEY \
  --rpc-url $JSON_RPC_POLYGON \
  $CONTRACT_ADDRESS \
  "updateTermsOfService(uint16,bytes32,string)" \
  "$TERMS_OF_SERVICE_VERSION" \
  "$ACCEPTANCE_MESSAGE_HASH" \
  "$ACCEPTANCE_MESSAGE"
```

You can also run the above command using [scripts/set-terms-of-service.sh](./scripts/set-terms-of-service.sh).
The script will complain if you have some variables unset.

See here troubleshooting if [cast send fails](https://ethereum.stackexchange.com/questions/161808/foundtry-cast-code-32000-message-replacement-transaction-underpriced-data).

## Updating terms of service version

With `ipython`:

```python
from terms_of_service.acceptance_message import INITIAL_ACCEPTANCE_MESSAGE, get_signing_hash

NEW_ACCEPTANCE_MESSAGE="""Update: December 23th, 2023

In our ongoing commitment to adhere to legal regulations, we will restrict IP addresses located in certain jurisdictions from accessing our application’s frontend user interface. These jurisdictions include: United States, United Kingdom, Cuba, Iran, North Korea, Syria and Russia. Thank you for your understanding and ongoing support

Last Modified: December 23rd, 2023"""

new_line_escaped_msg = NEW_ACCEPTANCE_MESSAGE.replace("\n", "\\n")
print("Paste to your shell:")
print("")
print(f"""export ACCEPTANCE_MESSAGE_HASH={get_signing_hash(NEW_ACCEPTANCE_MESSAGE).hex()}""")
print(f"""export ACCEPTANCE_MESSAGE="{new_line_escaped_msg}" """)
print(f"""export TERMS_OF_SERVICE_VERSION=2""")
```

Then run:

```shell
scripts/set-terms-of-service.sh
```

## Updating terms of service w/ frontend

- Configure environment vars `DEPLOY_PRIVATE_KEY` and `JSON_RPC_POLYGON`, `$CONTRACT_ADDRESS`
- Get the latest Terms of Service version from the smart contract using PolygonScan:m https://polygonscan.com/address/0xbe1418df0bAd87577de1A41385F19c6e77312780#readContract
- Bump the version up by one
- Get the Microsoft Word document from a laywer (lawyers love Microsoft Word)
- Convert to Markdown using e.g. https://word2md.com/
- Checkout frontend repo
- Add the file as .txt file to `lib/assets/tos/` e.g.`lib/assets/tos/2024-03-20.txt`
- Set environment variables as in [update.py](./scripts/update.py)
- Run `python scripts/update.py` to change on-chain state and get a new hash
- Update `lib/assets/tos/tos-map.js`

## Deployment

A deployment can be found on Polygon [0xbe1418df0bAd87577de1A41385F19c6e77312780](https://polygonscan.com/address/0xbe1418df0bAd87577de1A41385F19c6e77312780).

## More information

- [Join Discord for any questions](https://tradingstrategy.ai/community).
- [Watch tutorials on YouTube](https://www.youtube.com/@tradingstrategyprotocol)
- [Follow on Twitter](https://twitter.com/TradingProtocol)
- [Follow on Telegram](https://t.me/trading_protocol)
- [Follow on LinkedIn](https://www.linkedin.com/company/trading-strategy/)
