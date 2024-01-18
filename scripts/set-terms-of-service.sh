#!/bin/bash

set -x
set -e
set -u

cast send \
  --private-key $DEPLOY_PRIVATE_KEY \
  --rpc-url $JSON_RPC_POLYGON \
  $CONTRACT_ADDRESS \
  "updateTermsOfService(uint16,bytes32,string)" \
  "$TERMS_OF_SERVICE_VERSION" \
  "$ACCEPTANCE_MESSAGE_HASH" \
  "$ACCEPTANCE_MESSAGE"