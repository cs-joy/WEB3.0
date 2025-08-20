// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AIChatbot {
    address public owner;
    uint256 public queryPrice;
    IERC20 public rewardToken;
    
    enum QueryStatus { PENDING, ANSWERED }
    
    struct Query {
        address user;
        string question;
        string responseCID;
        uint256 timestamp;
        QueryStatus status;
    }
    
    Query[] public queries;
    
    event QueryPosted(uint256 indexed queryId, address indexed user, string question);
    event ResponseAdded(uint256 indexed queryId, string responseCID);
    
    constructor(uint256 _queryPrice, address _rewardToken) {
        owner = msg.sender;
        queryPrice = _queryPrice;
        rewardToken = IERC20(_rewardToken);
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    function postQuery(string memory _question) external payable {
        require(msg.value >= queryPrice, "Insufficient payment");
        
        queries.push(Query({
            user: msg.sender,
            question: _question,
            responseCID: "",
            timestamp: block.timestamp,
            status: QueryStatus.PENDING
        }));
        
        emit QueryPosted(queries.length - 1, msg.sender, _question);
    }
    
    function addResponse(uint256 _queryId, string memory _responseCID) external onlyOwner {
        require(_queryId < queries.length, "Invalid query ID");
        require(queries[_queryId].status == QueryStatus.PENDING, "Already answered");
        
        queries[_queryId].responseCID = _responseCID;
        queries[_queryId].status = QueryStatus.ANSWERED;
        
        // Reward user for asking
        rewardToken.transfer(queries[_queryId].user, 10 * 10**18);
        
        emit ResponseAdded(_queryId, _responseCID);
    }
    
    function withdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
    
    function setQueryPrice(uint256 _newPrice) external onlyOwner {
        queryPrice = _newPrice;
    }
}
