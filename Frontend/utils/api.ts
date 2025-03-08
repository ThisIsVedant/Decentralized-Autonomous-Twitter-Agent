export const fetchBalance = async () => {
    try {
        const response = await fetch("http://localhost:8001/connections/sonic/balance");
        if (!response.ok) throw new Error("Failed to fetch Sonic balance");
        return await response.json();
    } catch (err) {
        throw err;
    }
};

export const startAgent = async () => {
    try {
        const response = await fetch("http://localhost:8001/agent/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
        return await response.json();
    } catch (error) {
        throw error;
    }
};

export const stopAgent = async () => {
    try {
        const response = await fetch("http://localhost:8001/agent/stop", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
        return await response.json();
    } catch (error) {
        throw error;
    }
};

export const postTweet = async (prompt : string) => {
    try {
        const response = await fetch("http://localhost:8001/agent/post-tweet", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) throw new Error("Failed to tweet post");
        return await response.json();

    } catch (error) {
        return { status: 'error', message: error || 'An error occurred' };
    }
};

export const postTweetWithImage = async (prompt : string) => {
    try {
        const response = await fetch("http://localhost:8001/agent/post-with-image", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) throw new Error("Failed to tweet post");
        return await response.json();

    } catch (error) {
        return { status: 'error', message: error || 'An error occurred' };
    }
};

export const replyTweet = async () => {
    try {
        const response = await fetch("http://localhost:8001/agent/reply-to-tweet", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) throw new Error("Failed to reply to tweet");
        return await response.json();

    } catch (error) {
        return { status: 'error', message: error || 'An error occurred' };
    }
};

export const likeTweet = async () => {
    try {
        const response = await fetch("http://localhost:8001/agent/like-tweet", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) throw new Error("Failed to like tweet");
        return await response.json();

    } catch (error) {
        return { status: 'error', message: error || 'An error occurred' };
    }
};