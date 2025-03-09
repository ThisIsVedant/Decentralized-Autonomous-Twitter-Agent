"use client";

import React, { useState } from "react";
import {FaImage, FaRegHeart,} from "react-icons/fa";
import {FaXTwitter} from "react-icons/fa6";
import {likeTweet, postTweet, postTweetWithImage, replyTweet, startAgent, stopAgent} from "@/utils/api";
import {FiMessageSquare} from "react-icons/fi";
import AgentButton from "@/components/AgentButton";

export default function Actions({ setLogs }: { setLogs: React.Dispatch<React.SetStateAction<string[]>> }) {
    const [prompt, setPrompt] = useState("");
    const [isRunning, setIsRunning] = useState(false);
    const [agentLoading, setAgentLoading] = useState(false);
    const [loading, setLoading] = useState(false);
    const [activeAction, setActiveAction] = useState<string | null>(null)

    const handleAction = async (action: string) => {
        if (activeAction) return // Prevent multiple actions from running simultaneously
        setActiveAction(action)

        // Simulating an API call
        await new Promise((resolve) => setTimeout(resolve, 2000))

        setActiveAction(null)
    }

    const handleStartStop = async () => {
        setAgentLoading(true);
        try {
            if(!isRunning) {
                // Start the agent
                const data = await startAgent();
                setIsRunning(true);
                setLogs((prev) => [...prev, data.message]);
            } else {
                // Stop the agent
                const data = await stopAgent();
                setIsRunning(false);
                setLogs((prev) => [...prev, `🛑 ${data.message}`]);
            }

        } catch(error) {
            setLogs((prev) => [...prev, `Failed to start agent: ${error.message || error}`]);
        } finally {
            setAgentLoading(false);
        }
    };

    const handlePostTweet = async () => {
        setLoading(true);
        setLogs((prev) => [...prev, "Posting tweet..."]);
        try {
            if(isRunning) {
                const data = await postTweet(prompt);
                setLogs((prev) => [...prev, `${data.tweetText}`]);
                setLogs((prev) => [...prev, `${data.message}`]);
            } else {
                setLogs((prev) => [...prev, "Agent not started!"]);
            }
        } catch(error) {
            setLogs((prev) => [...prev, `Failed to post tweet: ${error.message || error}`]);
        } finally {
            setLoading(false);
        }
    };

    const handlePostTweetWithImage = async () => {
        setLoading(true);
        setLogs((prev) => [...prev, "Posting tweet..."]);
        try {
            if(isRunning) {
                const data = await postTweetWithImage(prompt);
                setLogs((prev) => [...prev, `${data.tweetText}`]);
                setLogs((prev) => [...prev, `${data.message}`]);
            } else {
                setLogs((prev) => [...prev, "Agent not started!"]);
            }
        } catch (error) {
            setLogs((prev) => [...prev, `Failed to post tweet with image: ${error.message || error}`]);
        } finally {
            setLoading(false);
        }
    };

    const handleReplyToTweet = async () => {
        setLoading(true);
        setLogs((prev) => [...prev, "Reply to tweet..."]);
        try {
            if(isRunning) {
                const data = await replyTweet();
                setLogs((prev) => [...prev, `${JSON.stringify(data.timeline)}`]);
                setLogs((prev) => [...prev, `${data.replyText}`]);
                setLogs((prev) => [...prev, `${data.message}`]);
            } else {
            setLogs((prev) => [...prev, "Agent not started!"]);
            }
        } catch (error) {
            setLogs((prev) => [...prev, `Failed to reply to tweet: ${error.message || error}`]);
        } finally {
            setLoading(false);
        }
    };

    const handleLikeTweet = async () => {
        setLoading(true);
        setLogs((prev) => [...prev, "like tweet..."]);
        try {
            if(isRunning) {
                const data = await likeTweet();
                setLogs((prev) => [...prev, `${JSON.stringify(data.timeline)}`]);
                setLogs((prev) => [...prev, `${data.message}`]);
            } else {
                setLogs((prev) => [...prev, "Agent not started!"]);
            }
        } catch (error) {
            setLogs((prev) => [...prev, `Failed to like tweet: ${error.message || error}`]);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="p-6 border rounded-lg shadow">
            <div className="mb-4">
                <h3 className="text-2xl font-semibold text-black">Generate and Automate</h3>
                <h1 className="text-sm text-gray-500">Enter your prompt and select actions</h1>
            </div>
            <textarea
                className={`w-full p-2 border rounded text-black ${
                    activeAction === "Post Tweet" || activeAction === "Post Tweet with Image"
                        ? "border-red-500" // Red border when action is active
                        : "border-gray-300" // Default border
                }`}
                placeholder="Enter your tweet prompt..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <div className="space-y-2 mt-4">
                <div className="flex justify-between ">
                    <label htmlFor="actions" className="font-medium text-black">Select Actions</label>
                </div>
                <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4 text-black">
                        <ActionButton handleAction={handleAction} executeAction={handlePostTweet}
                                      activeAction={activeAction} actionName="Post Tweet" icon={<FaXTwitter/>} loading={loading}/>
                        <ActionButton handleAction={handleAction} executeAction={handlePostTweetWithImage}
                                      activeAction={activeAction} actionName="Post Tweet with Image" icon={<FaImage/>} loading={loading}/>
                        <ActionButton handleAction={handleAction} executeAction={handleReplyToTweet}
                                      activeAction={activeAction} actionName="Reply to Tweet"
                                      icon={<FiMessageSquare/>} loading={loading}/>
                        <ActionButton handleAction={handleAction} executeAction={handleLikeTweet}
                                      activeAction={activeAction} actionName="Like Tweet" icon={<FaRegHeart/>} loading={loading}/>

                    </div>
                </div>
            </div>
            <AgentButton isRunning={isRunning} handleStartStop={handleStartStop}/>
        </div>
    );
}

const ActionButton = ({executeAction, handleAction, activeAction, icon, actionName, loading }) => (
    <button
        className="border p-4 rounded-lg flex flex-col items-center justify-center"
        onClick={() => {
            handleAction(actionName)
            executeAction()
        }}
        disabled={!!activeAction}
    >
        {(activeAction === actionName ) && loading ? (
            <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
        ) : (
            icon
        )}
        <span>{actionName}</span>
    </button>
);