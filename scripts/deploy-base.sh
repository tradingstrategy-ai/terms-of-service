#!/bin/bash

set -e
set -x
set -u

forge create \
  --rpc-url $JSON_RPC_BASE \
  --private-key $DEPLOY_PRIVATE_KEY \
  --etherscan-api-key $BASE_ETHERSCAN_API_KEY \
  --broadcast \
  --verify \
  src/TermsOfService.sol:TermsOfService
