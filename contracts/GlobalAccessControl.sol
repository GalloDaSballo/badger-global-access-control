// SPDX-License-Identifier: MIT

pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelin-contracts-upgradeable/math/SafeMathUpgradeable.sol";
import "@openzeppelin-contracts-upgradeable/token/ERC20/IERC20Upgradeable.sol";
import "@openzeppelin-contracts-upgradeable/token/ERC20/SafeERC20Upgradeable.sol";
import "@openzeppelin-contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin-contracts-upgradeable/utils/PausableUpgradeable.sol";
import "@openzeppelin-contracts-upgradeable/utils/EnumerableSetUpgradeable.sol";

/**
 * @title Badger Geyser
 @dev Tracks stakes and pledged tokens to be distributed, for use with 
 @dev BadgerTree merkle distribution system. An arbitrary number of tokens to 
 distribute can be specified.
 */

contract GlobalAccessControl is Initializable, AccessControlUpgradeable, PausableUpgradeable {
    using SafeERC20Upgradeable for IERC20Upgradeable;
    using SafeMathUpgradeable for uint256;

    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant UNPAUSER_ROLE = keccak256("UNPAUSER_ROLE");

    bytes32 public constant BLACKLIST_MANAGER_ROLE = keccak256("BLACKLIST_MANAGER_ROLE");
    bytes32 public constant BLACKLISTED_ROLE = keccak256("BLACKLISTED_ROLE");

    // Dev multisig, is the governance of most contracts
    // Should be able to do anything
    address public constant DEV_MULTISIG = 0xB65cef03b9B89f99517643226d76e286ee999e77;
    // Techops is a faster less trusted multisig to execute operations urgently
    // Can pause but not unpause
    // Can blacklist
    address public constant TECHOPS_MULTISIG = 0x86cbD0ce0c087b482782c181dA8d191De18C8275;

    // Can only pause
    address public constant WAR_ROOM_ACL = 0x6615e67b8B6b6375D38A0A3f937cd8c1a1e96386;

    function initialize() external initializer {
        
        /**
            Admin manages roles for pausers, unpausers, and blacklist managers
            Blacklist Manager manages blacklist
        */

        // No need as DEFAULT_ADMIN is already roleAdmin
        // _setRoleAdmin(PAUSER_ROLE, DEFAULT_ADMIN_ROLE);
        // _setRoleAdmin(UNPAUSER_ROLE, DEFAULT_ADMIN_ROLE);
        // _setRoleAdmin(BLACKLIST_MANAGER_ROLE, DEFAULT_ADMIN_ROLE);

        _setRoleAdmin(BLACKLISTED_ROLE, BLACKLIST_MANAGER_ROLE);

        _setupRole(DEFAULT_ADMIN_ROLE, DEV_MULTISIG);

        _setupRole(BLACKLIST_MANAGER_ROLE, DEV_MULTISIG);
        _setupRole(BLACKLIST_MANAGER_ROLE, TECHOPS_MULTISIG);

        _setupRole(PAUSER_ROLE, WAR_ROOM_ACL);
        _setupRole(PAUSER_ROLE, TECHOPS_MULTISIG);
        _setupRole(PAUSER_ROLE, DEV_MULTISIG);

        _setupRole(UNPAUSER_ROLE, DEV_MULTISIG);
    }

    function pause() external {
        require(hasRole(PAUSER_ROLE, msg.sender), "PAUSER_ROLE");
        _pause();
    }

    function unpause() external {
        require(hasRole(UNPAUSER_ROLE, msg.sender), "UNPAUSER_ROLE");
        _unpause();
    }

    function isBlacklisted(address account) external view returns (bool) {
        return hasRole(BLACKLISTED_ROLE, account);
    }
}