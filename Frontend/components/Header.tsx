"use client";
import BalanceButton from "./WalletButton";
import Image from "next/image";

export default function Header() {
    return (
        <header className="flex justify-between items-center mb-8">
            <div className="flex items-center gap-2 text-3xl font-bold text-black">
                {/*<FaXTwitter />*/}
                <Image src="/appIcon.png" alt="appIcon" height={60} width={60} />
                {/*<span>Automation Tool</span>*/}
                <h1 className="font-extrabold text-center">
                    Decentralized
                        <span className="block text-base font-semibold w-full text-center font-mono">Autonomous Twitter Agent</span>
                </h1>
            </div>
            <BalanceButton />
        </header>
    );
}