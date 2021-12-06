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

    
    // === Immutable Variables* ===
    // * They can't be changed, but they are not immutable as this is an upgradeable contract

    // Dev multisig, is the governance of most contracts
    // Should be able to do anything
    address public DEV_MULTISIG;
    
    // Techops is a faster less trusted multisig to execute operations urgently
    // Can pause but not unpause
    // Can blacklist
    address public TECHOPS_MULTISIG;

    // Can only pause
    address public WAR_ROOM_ACL;

    function initialize(address _devMultisig, address _techopsMultisig, address _warRoomAcl) external initializer {
        /**
            Admin manages roles for pausers, unpausers, and blacklist managers
            Blacklist Manager manages blacklist
        */

        // Set up the view variables
        DEV_MULTISIG = _devMultisig;
        TECHOPS_MULTISIG = _techopsMultisig;
        WAR_ROOM_ACL = _warRoomAcl;
        
        // No need as DEFAULT_ADMIN is already roleAdmin
        // _setRoleAdmin(PAUSER_ROLE, DEFAULT_ADMIN_ROLE);
        // _setRoleAdmin(UNPAUSER_ROLE, DEFAULT_ADMIN_ROLE);
        // _setRoleAdmin(BLACKLIST_MANAGER_ROLE, DEFAULT_ADMIN_ROLE);

        _setRoleAdmin(BLACKLISTED_ROLE, BLACKLIST_MANAGER_ROLE);

        _setupRole(DEFAULT_ADMIN_ROLE, _devMultisig);

        _setupRole(BLACKLIST_MANAGER_ROLE, _devMultisig);
        _setupRole(BLACKLIST_MANAGER_ROLE, _techopsMultisig);

        _setupRole(PAUSER_ROLE, _devMultisig);
        _setupRole(PAUSER_ROLE, _techopsMultisig);
        _setupRole(PAUSER_ROLE, _warRoomAcl);
        
        _setupRole(UNPAUSER_ROLE, _devMultisig);
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