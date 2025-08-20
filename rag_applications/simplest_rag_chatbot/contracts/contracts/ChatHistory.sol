// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ChatHistory {
    struct ChatEntry {
        address user;
        string query;
        string response;
        uint256 timestamp;
    }
    
    ChatEntry[] public chatHistory;
    mapping(address => uint256[]) public userChats;
    
    event ChatAdded(
        address indexed user,
        uint256 indexed entryId,
        string query,
        string response,
        uint256 timestamp
    );
    
    function addChat(string memory _query, string memory _response) public {
        uint256 newEntryId = chatHistory.length;
        chatHistory.push(ChatEntry({
            user: msg.sender,
            query: _query,
            response: _response,
            timestamp: block.timestamp
        }));
        
        userChats[msg.sender].push(newEntryId);
        
        emit ChatAdded(
            msg.sender,
            newEntryId,
            _query,
            _response,
            block.timestamp
        );
    }
    
    function getChatHistoryCount() public view returns (uint256) {
        return chatHistory.length;
    }
    
    function getChatEntry(uint256 _index) public view returns (
        address,
        string memory,
        string memory,
        uint256
    ) {
        require(_index < chatHistory.length, "Index out of bounds");
        ChatEntry memory entry = chatHistory[_index];
        return (entry.user, entry.query, entry.response, entry.timestamp);
    }
    
    function getUserChats(address _user) public view returns (uint256[] memory) {
        return userChats[_user];
    }
    
    function getUserChatsCount(address _user) public view returns (uint256) {
        return userChats[_user].length;
    }
}
