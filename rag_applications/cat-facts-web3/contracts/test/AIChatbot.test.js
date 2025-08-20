const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AIChatbot", function () {
  let chatbot, token, owner, user;

  beforeEach(async () => {
    [owner, user] = await ethers.getSigners();
    
    const CatToken = await ethers.getContractFactory("CatToken");
    token = await CatToken.deploy();
    
    const AIChatbot = await ethers.getContractFactory("AIChatbot");
    chatbot = await AIChatbot.deploy(
      ethers.utils.parseEther("0.01"),
      token.address
    );
    
    // Transfer tokens to chatbot for rewards
    await token.transfer(chatbot.address, ethers.utils.parseEther("1000"));
  });

  it("Should post query with correct payment", async function () {
    await expect(
      chatbot.connect(user).postQuery("Test question", {
        value: ethers.utils.parseEther("0.01")
      })
    ).to.emit(chatbot, "QueryPosted");
  });

  it("Should reject query with insufficient payment", async function () {
    await expect(
      chatbot.connect(user).postQuery("Test question", {
        value: ethers.utils.parseEther("0.005")
      })
    ).to.be.revertedWith("Insufficient payment");
  });

  it("Should allow owner to add response", async function () {
    await chatbot.connect(user).postQuery("Test question", {
      value: ethers.utils.parseEther("0.01")
    });
    
    await expect(
      chatbot.connect(owner).addResponse(0, "Qm...")
    ).to.emit(chatbot, "ResponseAdded");
  });

  it("Should reward user for asking", async function () {
    await chatbot.connect(user).postQuery("Test question", {
      value: ethers.utils.parseEther("0.01")
    });
    
    const balanceBefore = await token.balanceOf(user.address);
    await chatbot.connect(owner).addResponse(0, "Qm...");
    const balanceAfter = await token.balanceOf(user.address);
    
    expect(balanceAfter.sub(balanceBefore)).to.equal(
      ethers.utils.parseEther("10")
    );
  });
});
