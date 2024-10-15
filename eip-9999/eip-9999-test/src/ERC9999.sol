// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.16;

import "forge-std/Test.sol";
import "./IERC9999.sol";
import "@openzeppelin/contracts/ownership/Ownable.sol";

contract ERC9999 is IERC9999, Ownable {

    struct UserRentalInfo {
        address user;   
        uint64 expires; 
        uint256 licenseId;
    }

    struct RentalLicense {
        uint256 tokenId;        
        uint256 parentLicenseId;
        string uri;              
    }
  
    mapping (uint256 => UserRentalInfo) private _users;     // maps from an NFT to its user, expiration, and rental license identifier
    mapping (uint256 => RentalLicense) private _licenses;   // maps from a rental license identifier to a rental license struct object
    mapping (uint256 => uint256) private _licenseIds;       // maps from an NFT to its rental license identifier

    /// @notice Get a user's rental license.
    /// @dev The zero value indicates no license.
    /// Throws if `tokenId` is not a valid NFT.
    /// @param tokenId The NFT to get the rental license for.
    /// @return licenseId The identifier of the rental license.
    function userRentalLicense(uint256 tokenId) external view returns(uint256) {

        require(tokenId != 0, "ERC9999: tokenId is not valid");

        return _users[tokenId].licenseId;
    }

    /// @notice Set the temporary user, expires, and rental license of an NFT.
    /// @dev The zero address indicates that the rental NFT has no user. 
    /// Throws if `tokenId` is not valid NFT.
    /// Throws if `licenseId` is not a valid license.
    /// Throws if `msg.sender` is not the owner of the NFT.
    /// Throws if `expires` is in the past.
    /// @param tokenId The NFT to be rented.
    /// @param user The new user of the NFT.
    /// @param licenseId The identifier of the rental license.
    /// @param expires UNIX timestamp the new user can use the NFT before it expires.
    function setUserRentalLicense(uint256 tokenId, address user, uint256 licenseId, uint64 expires) external onlyOwner {

            require(tokenId != 0, "ERC9999: tokenId is not valid");
            require(licenseId != 0, "ERC9999: licenseId is not valid");
            require(expires > block.timestamp, "ERC9999: expires is not valid");

            _users[tokenId] = UserRentalInfo(user, expires, licenseId);     

            emit UpdateRentalLicense(tokenId, licenseId, user, expires);
    }

    /// @notice Create a new rental license.
    /// @dev The zero value for parentLicenseId indicates the license has no parent.
    /// Throws if `tokenId` is not valid NFT.
    /// Throws if `msg.sender` is not the owner of the NFT.
    /// Throws uri is invalid.
    /// @param tokenId The NFT the rental license is issued upon.
    /// @param parentLicenseId The identifier for the parent license.
    /// @param uri The URI of the license terms.
    /// @return licenseId The identifier of the created rental license.
    function createRentalLicense(uint256 tokenId, uint256 parentLicenseId, string memory uri) external onlyOwner returns (uint256) { 

        require(tokenId != 0, "ERC9999: tokenId is not valid");
        require(bytes(uri).length != 0, "ERC9999: uri is not valid");

        uint256 licenseId = _getNextLicenseId();
        _licenses[licenseId] = RentalLicense(tokenId, parentLicenseId, uri);
        _licenseIds[tokenId] = licenseId;

        emit CreateRentalLicense(licenseId, tokenId, parentLicenseId, uri);

        return licenseId;
    }

    /// @notice Get the next rental license identifier.
    /// @dev Throws if the identifier overflows.
    /// @return licenseId The next rental license identifier.
    function _getNextLicenseId() private view returns (uint256) {

        uint256 _licenseIdTracker = 1;
        while (true) {
            if (_licenseIds[_licenseIdTracker] == 0) {
                break;
            }
            _licenseIdTracker++;

        }

        require(_licenseIdTracker < 2**256 - 1, "ERC9999: licenseId overflow");

        return _licenseIdTracker;
    }

    /// @notice Get the URI of a rental license.
    /// @dev Throws if `licenseId` is not a valid license.
    /// @param licenseId The identifier of the rental license.
    /// @return uri The URI of the rental license.
    function getLicenseURI(uint256 licenseId) external view returns (string memory) {

        require(licenseId != 0, "ERC9999: licenseId is not valid");
        
        return _licenses[licenseId].uri;
    }
} 
