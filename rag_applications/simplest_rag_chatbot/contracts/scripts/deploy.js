const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await ethers.provider.getBalance(deployer.address)).toString());

  const ChatHistory = await ethers.getContractFactory("ChatHistory");
  const chatHistory = await ChatHistory.deploy();
  await chatHistory.waitForDeployment();

  const chatHistoryAddress = await chatHistory.getAddress();
  console.log("ChatHistory address:", chatHistoryAddress);
  
  // Save contract address to a file for backend use
  const contractsDir = __dirname + "/../backend/contracts";
  
  if (!fs.existsSync(contractsDir)) {
    fs.mkdirSync(contractsDir, { recursive: true });
  }
  
  fs.writeFileSync(
    contractsDir + "/chatHistory-address.json",
    JSON.stringify({ ChatHistory: chatHistoryAddress }, undefined, 2)
  );
  
  // Get contract ABI
  const ChatHistoryArtifact = await artifacts.readArtifact("ChatHistory");
  
  fs.writeFileSync(
    contractsDir + "/ChatHistory.json",
    JSON.stringify(ChatHistoryArtifact, null, 2)
  );

  console.log("Contract artifacts saved to backend/contracts/");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
