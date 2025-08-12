const hre = require("hardhat");

async function main() {
  const DataStorage = await hre.ethers.getContractFactory("DataStorage");
  const contract = await DataStorage.deploy();

  await contract.waitForDeployment();

  console.log(
    `DataStorage deployed to ${await contract.getAddress()}`
  );
  
  // This is needed for your Java backend configuration
  console.log("Contract ABI:", JSON.stringify(contract.interface.format("json")));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
