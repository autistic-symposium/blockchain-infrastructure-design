// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.13;

import {Test} from "forge-std/Test.sol";
import {ERC9999} from "../src/erc9999.sol";

contract ERC9999Test is Test {

    ERC9999 e;
    address user = address(0xbeef);
    string tokenURI = "someTokenURI";
    string licenseURI = "someLicenseURI";
    uint256 tokenId = 1;
    uint256 parentLicenseId = 0;
    uint64 expires = 1737586800;

    event CreateRentalLicense(uint256 licenseId, uint256 tokenId, uint256 parentLicenseId, string uri);
    event UpdateRentalLicense(uint256 tokenId, uint256 licenseId, address user, uint64 expires);

    function setUp() public {
        vm.deal(user, 10 ether);
        e = new ERC9999();
    }

    function testERC9999() public {
        
        // Test license creation (createRentalLicense)
        vm.expectEmit(); 
        emit CreateRentalLicense(1, tokenId, parentLicenseId, licenseURI);
        uint256 licenseId = e.createRentalLicense(tokenId, parentLicenseId, licenseURI);
        assertEq(e.getLicenseURI(licenseId), licenseURI, "License URI should match");
        
        // Test setting userRentalLicense
        vm.expectEmit();
        emit UpdateRentalLicense(tokenId, licenseId, user, expires);
        e.setUserRentalLicense(tokenId, user, licenseId, expires);        

        // Test license lookup (userRentalLicense)
        assertEq(e.userRentalLicense(tokenId), licenseId, "LicenseId should match");

    }
}
