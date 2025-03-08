"use client";

import { useState } from "react";
import Image from "next/image";
import { MdError } from "react-icons/md";
import { getProvider } from "@/utils/wallet"; // Ensure this file exists
import { fetchBalance } from "@/utils/api"; // Ensure this function fetches balance

export default function WalletButton() {
    const [account, setAccount] = useState<string | null>(null);
    const [balance, setBalance] = useState<number | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const connectWallet = async () => {
        if (!(window as any).ethereum) {
            window.open("https://metamask.io/download/", "_blank");
            return;
        }

        try {
            setLoading(true);
            const provider = getProvider();
            const accounts = await (window as any).ethereum.request({ method: "eth_requestAccounts" });
            setAccount(accounts[0]);

            // Fetch balance after connection
            const data = await fetchBalance(accounts[0]);
            setBalance(data.balance);
        } catch (err) {
            setError("Wallet connection failed.");
            console.error("Wallet connection error:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <button
            onClick={connectWallet}
            className="flex items-center gap-2 px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-900 transition-all"
        >
            <Image src="/sonic.png" alt="logo" height={30} width={30} />

            {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : account ? (
                <>
                    {balance !== null ? `${balance.toFixed(3)} S` : <MdError className="text-red-500" />}
                    <span className="text-gray-400">{account.slice(0, 6)}...{account.slice(-4)}</span>
                </>
            ) : (
                "Connect Wallet"
            )}
        </button>
    );
}
