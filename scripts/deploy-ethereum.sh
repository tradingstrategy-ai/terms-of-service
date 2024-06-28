#!/bin/bash

set -e
set -x
set -u

forge create \
  --rpc-url $JSON_RPC_ETHEREUM \
  --private-key $DEPLOY_PRIVATE_KEY \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --verify \
  src/TermsOfService.sol:TermsOfService
