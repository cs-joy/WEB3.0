const { ethers } = require("hardhat");

async function main() {
  // Deploy CatToken
  const CatToken = await ethers.getContractFactory("CatToken");
  const catToken = await CatToken.deploy();
  await catToken.deployed();
  console.log("CatToken deployed to:", catToken.address);

  // Deploy AIChatbot (with 0.01 ETH query price)
  const AIChatbot = await ethers.getContractFactory("AIChatbot");
  const aiChatbot = await AIChatbot.deploy(
    ethers.utils.parseEther("0.01"),
    catToken.address
  );
  await aiChatbot.deployed();
  console.log("AIChatbot deployed to:", aiChatbot.address);

  // Transfer some tokens to the chatbot for rewards
  await catToken.transfer(aiChatbot.address, ethers.utils.parseEther("100000"));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
