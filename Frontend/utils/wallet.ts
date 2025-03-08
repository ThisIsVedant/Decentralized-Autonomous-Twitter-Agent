import { ethers } from "ethers";

const SONIC_RPC = "https://rpc.blaze.soniclabs.com"; // Sonic Blaze Testnet RPC

export const getProvider = () => {
    if (typeof window !== "undefined" && (window as any).ethereum) {
        return new ethers.BrowserProvider((window as any).ethereum);
    }
    return new ethers.JsonRpcProvider(SONIC_RPC);
};

export const getSigner = async () => {
    const provider = getProvider();
    return provider.getSigner();
};