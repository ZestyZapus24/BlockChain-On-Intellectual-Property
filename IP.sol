// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IntellectualPropertyRegistry {
    address public owner;
    
    // Struct to represent intellectual property
    struct IntellectualProperty {
        address owner;
        string name;
        uint256 timestamp;
    }
    
    // Mapping to store intellectual properties
    mapping(uint256 => IntellectualProperty) public intellectualProperties;
    uint256 public intellectualPropertyCount;

    // Events to log changes
    event IntellectualPropertyCreated(address indexed owner, uint256 indexed id, string name, uint256 timestamp);
    event IntellectualPropertyTransferred(uint256 indexed id, address indexed previousOwner, address indexed newOwner, uint256 timestamp);

    constructor() {
        owner = msg.sender;
    }

    // Modifier to check if the caller is the owner of an intellectual property
    modifier onlyOwnerOf(uint256 id) {
        require(msg.sender == intellectualProperties[id].owner, "You are not the owner of this intellectual property.");
        _;
    }

    // Create a new intellectual property
    function createIntellectualProperty(string memory name) external {
        require(bytes(name).length > 0, "Name cannot be empty.");
        uint256 id = intellectualPropertyCount++;
        intellectualProperties[id] = IntellectualProperty(msg.sender, name, block.timestamp);
        emit IntellectualPropertyCreated(msg.sender, id, name, block.timestamp);
    }

    // Transfer ownership of an intellectual property
    function transferIntellectualProperty(uint256 id, address newOwner) external onlyOwnerOf(id) {
        require(newOwner != address(0), "Invalid new owner address.");
        intellectualProperties[id].owner = newOwner;
        emit IntellectualPropertyTransferred(id, msg.sender, newOwner, block.timestamp);
    }
}
