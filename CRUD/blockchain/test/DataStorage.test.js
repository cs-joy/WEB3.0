const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DataStorage", function () {
  let DataStorage, contract;

  before(async () => {
    DataStorage = await ethers.getContractFactory("DataStorage");
    contract = await DataStorage.deploy();
  });

  it("Should create and read data", async () => {
    await contract.create("Test", "Description");
    const [id, name, desc] = await contract.read(1);
    expect(name).to.equal("Test");
    expect(desc).to.equal("Description");
  });

  it("Should update data", async () => {
    await contract.update(1, "Updated", "New Description");
    const [_, name] = await contract.read(1);
    expect(name).to.equal("Updated");
  });

  it("Should delete data", async () => {
    await contract.remove(1);
    const [id] = await contract.read(1);
    expect(id).to.equal(0); // Assuming your contract sets ID to 0 when deleted
  });
});
