// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/access/Ownable.sol";

// Support https://eips.ethereum.org/EIPS/eip-1271
// verification of smart contract signatures
import "@openzeppelin/utils/cryptography/SignatureChecker.sol";

/**
 * Terms of service acceptance tracker
 *
 * Manage signatures of users of different versions of terms of service.
 */
contract TermsOfService is Ownable {

    using SignatureChecker for address;

    // Terms of service acceptances
    //
    // Account can and may need to accept multiple terms of services.
    // Each terms of service is identified by its hash of text.
    // The acceptance is a message that signs this terms of service version.
    //
    mapping(address account => mapping(bytes32 textHash => bool accepted)) public acceptances;

    //
    // Published terms of services
    //
    mapping(uint16 version => bytes32 textHash) public versions;

    bytes32 public latestTermsOfServiceHash;

    //
    // Terms of service versions, starting from 1 and
    // increased with one for the each iteration.
    //
    uint16 public latestTermsOfServiceVersion;

    // Add a new terms of service version
    event UpdateTermsOfService(uint16 version, bytes32 textHash);

    constructor() Ownable() {
    }

    function hasAcceptedHash(address account, bytes32 textHash) public returns (bool accepted) {
        return acceptances[account][textHash];
    }

    function hasAcceptedVersion(address account, uint16 version) public returns (bool accepted) {
        bytes32 hash = versions[version];
        require(hash != bytes32(0), "No such version");
        return hasAcceptedHash(account, hash);
    }

    function updateTermsOfService(uint16 version, bytes32 textHash) public onlyOwner {
        require(version == latestTermsOfServiceVersion + 1, "Versions must be updated incrementally");
        latestTermsOfServiceHash = textHash;
        latestTermsOfServiceVersion = version;
        emit UpdateTermsOfService(version, textHash);
    }

    /**
     * Can the current user proceed to the next step, or they they need to sign
     * the latest terms of service.
     */
    function canProceed() public returns (bool accepted) {
        return hasAcceptedHash(msg.sender, latestTermsOfServiceHash);
    }

    /**
     * Sign terms of service
     *
     * - Externally Owned Account sign
     * - EIP-1271 sign
     *
     * The user can sign multiple times.
     *
     * See
     *
     * - Gnosis Safe signing example: https://github.com/safe-global/safe-eth-py/blob/master/gnosis/safe/tests/test_safe_signature.py#L195
     *
     * - OpenZeppelin SignatureChecker implementation: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol
     */
    function signTermsOfService(address signer, bytes32 hash, bytes memory signature) public {
        address signer = msg.sender;
        require(hash == latestTermsOfServiceHash, "Cannot sign older versions terms of services");
        require(signer.isValidSignatureNow(hash, signature), "Signature is not valid");
        require(acceptances[signer][latestTermsOfServiceHash] == false, "Already signed");
        acceptances[signer][latestTermsOfServiceHash] = true;
    }
}
