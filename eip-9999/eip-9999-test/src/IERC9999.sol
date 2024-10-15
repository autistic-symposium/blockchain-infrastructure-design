// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

/// @title ERC-9999: Rental NFTs with Rights Management
interface IERC9999 /* is IERC721, IERC165 */{

  /// @dev Emits when a rental license is set to a rental NFT.
  /// The zero address for the user indicates that there is no user address.
  event UpdateRentalLicense(uint256 tokenId, uint256 licenseId, address user, uint64 expires);

  /// @dev Emits when a new rental license is created. 
  /// The zero value for `parentLicenseId` indicates there is no parent license.
  event CreateRentalLicense(uint256 licenseId, uint256 tokenId, uint256 parentLicenseId, string uri);

  /// @notice Get a user's rental license.
  /// @dev The zero value indicates no license.
  /// Throws if `tokenId` is not a valid NFT.
  /// @param tokenId The NFT to get the rental license for.
  /// @return licenseId The identifier of the rental license.
  function userRentalLicense(uint256 tokenId) external view returns(uint256);

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
  function setUserRentalLicense(uint256 tokenId, address user, uint256 licenseId, uint64 expires) external;

  /// @notice Create a new rental license.
  /// @dev The zero value for parentLicenseId indicates the license has no parent.
  /// Throws if `tokenId` is not valid NFT.
  /// Throws if `msg.sender` is not the owner of the NFT.
  /// Throws uri is invalid.
  /// @param tokenId The NFT the rental license is issued upon.
  /// @param parentLicenseId The identifier for the parent license.
  /// @param uri The URI of the license terms.
  /// @return licenseId The identifier of the created rental license.
  function createRentalLicense(uint256 tokenId, uint256 parentLicenseId, string memory uri) external returns (uint256);
}
