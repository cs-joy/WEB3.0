import { ethers } from 'ethers';

export async function initWeb3() {
  if (!window.ethereum) {
    throw new Error("MetaMask not installed");
  }
  
  const provider = new ethers.providers.Web3Provider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  
  const signer = provider.getSigner();
  const address = await signer.getAddress();
  const network = await provider.getNetwork();
  
  return {
    provider,
    signer,
    address,
    chainId: network.chainId
  };
}

export function getContract(provider, address, abi) {
  return new ethers.Contract(address, abi, provider.getSigner());
}
