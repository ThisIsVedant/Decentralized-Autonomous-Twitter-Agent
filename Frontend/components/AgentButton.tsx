"use client";
import React, { useState } from "react";
import { getSigner } from "@/utils/wallet";
import { ethers } from "ethers";
import { FaPlayCircle, FaStopCircle } from "react-icons/fa";
import Image from "next/image";

const SONIC_RECIPIENT = "0x039e2fB66102314Ce7b64Ce5Ce3E5183bc94aD38"; // Hardcoded recipient contract address
const SONIC_AMOUNT = "1"; // Fixed amount

interface StartStopButtonProps {
    isRunning: boolean;
    handleStartStop: () => void;
}

const AgentButton: React.FC<StartStopButtonProps> = ({ isRunning, handleStartStop }) => {
    const [transactionLink, setTransactionLink] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [transactionComplete, setTransactionComplete] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const handleTransfer = async () => {
        try {
            setLoading(true);
            setErrorMessage(null); // Clear previous errors

            const signer = await getSigner();
            const amountWei = ethers.parseUnits(SONIC_AMOUNT, "ether");

            // Native Sonic (S) Transfer
            const tx = await signer.sendTransaction({
                to: SONIC_RECIPIENT,
                value: amountWei,
                gasLimit: 40000,
                gasPrice: ethers.parseUnits("1.1", "gwei"),
            });

            await tx.wait(); // Wait for transaction to be confirmed

            setTransactionLink(`https://testnet.sonicscan.org/tx/${tx.hash}`);
            setTransactionComplete(true);
            return true; // Success
        } catch (error) {
            console.error("Transaction failed:", error);
            setErrorMessage("Transaction failed or canceled. Please try again.");
            return false; // Failure
        } finally {
            setLoading(false);
        }
    };

    const handleButtonClick = async () => {
        if (!isRunning && !transactionComplete) {
            const success = await handleTransfer(); // Ensure transaction completes before toggling
            if (success) {
                handleStartStop(); // Only start agent if the transaction was successful
            }
        } else {
            handleStartStop(); // Stop Agent logic
        }
    };

    return (
        <div className="text-center">
            {transactionLink && (
                <p className="mt-4 text-black">
                    ✅ Transaction:{" "}
                    <a href={transactionLink} className="text-blue-300 underline" target="_blank">
                        View on SonicScan
                    </a>
                </p>
            )}

            {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}

            <button
                className={`mt-3 w-full px-4 py-2 rounded-md font-medium flex items-center justify-center text-white ${
                    isRunning ? "bg-red-500" : "bg-black"
                }`}
                onClick={handleButtonClick}
                disabled={loading} // Disable the button while transaction is processing
            >
                {loading ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : isRunning ? (
                    <>
                        <FaStopCircle className="mr-2" />
                        Stop Agent
                    </>
                ) : (
                    <>
                        <FaPlayCircle className="mr-2" />
                        Start Agent
                    </>
                )}
            </button>

            {!isRunning && (
                <span className="flex text-black items-center justify-center mt-2">
                    <Image className="mr-1" src="/sonic.png" alt="logo" height={20} width={20} />{SONIC_AMOUNT}
                </span>
            )}
        </div>
    );
};

export default AgentButton;
