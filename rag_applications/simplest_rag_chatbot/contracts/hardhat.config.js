require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.19",
  networks: {
    ganache: {
      url: "http://127.0.0.1:8545",
      chainId: 1337,
      gas: 2100000,
      gasPrice: 8000000000
    }
  }
};
