  #!/bin/bash

set -e
set -x
set -u

forge verify-contract \
    --etherscan-api-key $POLYGONSCAN_API_KEY \
    --flatten \
    --force \
    --chain polygon \
    --constructor-args $(cast abi-encode "constructor()") \
     $CONTRACT_ADDRESS \
     src/VaultUSDCPaymentForwarder.sol:VaultUSDCPaymentForwarder

