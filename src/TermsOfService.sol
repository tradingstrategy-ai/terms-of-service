// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.23;

import "@openzeppelin/access/Ownable.sol";

// Support https://eips.ethereum.org/EIPS/eip-1271
// verification of smart contract signatures
import "@openzeppelin/utils/cryptography/SignatureChecker.sol";


/**
 * Minimal MVP interface
 */
interface ITermsOfService {
    function canAddressProceed(address sender) external returns (bool accepted);
    function signTermsOfServiceBehalf(address signer, bytes32 hash, bytes calldata signature, bytes calldata metadata) external;
}

/**
 * Terms of service acceptance tracker
 *
 * Manage signatures of users of different versions of terms of service.
 */
contract TermsOfService is Ownable, ITermsOfService {

    // OpenZeppelin lib supporting smart contract based signing as opposite to EOA signing
    using SignatureChecker for address;

    // Terms of service acceptances
    //
    // Account can and may need to accept multiple terms of services.
    // Each terms of service is identified by its hash of text.
    // The acceptance is a message that signs this terms of service version.
    //
    mapping(address account => mapping(bytes32 acceptanceMessageHash => bool accepted)) public acceptances;

    //
    // Published terms of services
    //
    //
    // Terms of service versions, starting from 1 and
    // increased with one for the each iteration.
    //
    mapping(uint16 version => bytes32 acceptanceMessageHash) public versions;

    //
    // What is the hash of currently active terms of service version
    //
    bytes32 public latestAcceptanceMessageHash;

    //
    // What is the version numbe of current terms of service version
    //
    uint16 public latestTermsOfServiceVersion;

    // Add a new terms of service version
    event UpdateTermsOfService(uint16 version, bytes32 acceptanceMessageHash, string acceptanceMessage);

    // User accepted a specific terms of service version
    event Signed(address signer, uint16 version, bytes32 hash, bytes metadata);

    constructor() Ownable() {
    }

    function hasAcceptedHash(address account, bytes32 acceptanceMessageHash) public view returns (bool accepted) {
        return acceptances[account][acceptanceMessageHash];
    }

    function getTextHash(uint16 version) public view returns (bytes32 hash) {
        return versions[version];
    }

    function hasAcceptedVersion(address account, uint16 version) public view returns (bool accepted) {
        bytes32 hash = versions[version];
        require(hash != bytes32(0), "No such version");
        return hasAcceptedHash(account, hash);
    }

    /**
     * Update to the new terms of service version.
     *
     * We do not check whether acceptance message hash matches the message,
     * as the message string here is just for the event log keeping.
     *
     */
    function updateTermsOfService(uint16 version, bytes32 acceptanceMessageHash, string calldata acceptanceMessage) public onlyOwner {
        require(version == latestTermsOfServiceVersion + 1, "Versions must be updated incrementally");
        require(acceptanceMessageHash != latestAcceptanceMessageHash, "Setting the same terms of service twice");
        latestAcceptanceMessageHash = acceptanceMessageHash;
        latestTermsOfServiceVersion = version;
        versions[version] = acceptanceMessageHash;
        emit UpdateTermsOfService(version, acceptanceMessageHash, acceptanceMessage);
    }

    /**
     * Can the current user proceed to the next step, or they they need to sign
     * the latest terms of service.
     */
    function canProceed() public view returns (bool accepted) {
        return canAddressProceed(msg.sender);
    }

    /**
     * Can a user proceed to the next step, or they they need to sign
     * the latest terms of service.
     */
    function canAddressProceed(address sender) public view returns (bool accepted) {
        require(latestAcceptanceMessageHash != bytes32(0), "Terms of service not initialised");
        return hasAcceptedHash(sender, latestAcceptanceMessageHash);
    }

    /**
     * Sign terms of service
     *
     * - Externally Owned Account sign
     * - EIP-1271 sign
     * - EIP-191 formatted message
     *
     * The user can sign multiple times.
     *
     * See
     *
     * - ECDSA tryRecover https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol
     *
     * - Gnosis Safe signing example: https://github.com/safe-global/safe-eth-py/blob/master/gnosis/safe/tests/test_safe_signature.py#L195
     *
     * - OpenZeppelin SignatureChecker implementation: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol
     */
    function signTermsOfServiceBehalf(address signer, bytes32 hash, bytes calldata signature, bytes calldata metadata) public {
        require(hash == latestAcceptanceMessageHash, "Cannot sign older or unknown versions terms of services");
        require(signer.isValidSignatureNow(hash, signature), "Signature is not valid");
        require(acceptances[signer][latestAcceptanceMessageHash] == false, "Already signed");
        acceptances[signer][latestAcceptanceMessageHash] = true;
        emit Signed(signer, latestTermsOfServiceVersion, latestAcceptanceMessageHash, metadata);
    }

    function signTermsOfServiceOwn(bytes32 hash, bytes calldata signature, bytes calldata metadata) public {
        signTermsOfServiceBehalf(msg.sender, hash, signature, metadata);
    }

}
