// contracts/DataStorage.sol
pragma solidity ^0.8.0;

contract DataStorage {
    struct Data {
        uint id;
        string name;
        string description;
    }
    
    Data[] public dataItems;
    uint public nextId = 1;
    
    event DataCreated(uint id, string name, string description);
    event DataUpdated(uint id, string name, string description);
    event DataDeleted(uint id);
    
    function create(string memory _name, string memory _description) public {
        dataItems.push(Data(nextId, _name, _description));
        emit DataCreated(nextId, _name, _description);
        nextId++;
    }
    
    function read(uint _id) public view returns (uint, string memory, string memory) {
        require(_id > 0 && _id < nextId, "Invalid ID");
        Data memory item = dataItems[_id - 1];
        return (item.id, item.name, item.description);
    }
    
    function update(uint _id, string memory _name, string memory _description) public {
        require(_id > 0 && _id < nextId, "Invalid ID");
        Data storage item = dataItems[_id - 1];
        item.name = _name;
        item.description = _description;
        emit DataUpdated(_id, _name, _description);
    }
    
    function remove(uint _id) public {
        require(_id > 0 && _id < nextId, "Invalid ID");
        delete dataItems[_id - 1];
        emit DataDeleted(_id);
    }
    
    function getAllData() public view returns (Data[] memory) {
        return dataItems;
    }
}
