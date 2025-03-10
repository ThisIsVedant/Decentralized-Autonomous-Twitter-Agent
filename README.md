# Decentralized Autonomous Twitter Agent

**Watch the Demo** 

[![Watch the demo](https://img.youtube.com/vi/6SYgVZ19Zlg/0.jpg)](https://www.youtube.com/watch?v=6SYgVZ19Zlg)

## Introduction

This project leverages the Web3 ecosystem, utilizing **Sonic** and **ZerePy** to create an autonomous AI agent for X/Twitter actions. By integrating with the **Sonic blockchain ecosystem**, the project ensures decentralization and alignment with the platform's infrastructure and mission. Additionally, **ZerePy** enables custom AI agent actions, including Sonic transactions, Ollama-based AI actions, and Twitter automation.

## How It Works

To use the agent, users must have **Sonic tokens** and connect their **Metamask wallet**. Each agent activation requires **1 Sonic token** to initiate the transaction process.

The project operates on **Sonic Blaze Testnet** and includes the following four key actions:

1. **Post Tweet** → Requires a prompt to generate a post.
2. **Post Tweet with Image** → Requires a prompt and generates a tweet with an AI-generated image.
3. **Reply to Tweet** → Fetches timeline data from X/Twitter and generates an automated reply using **Ollama LLM**.
4. **Like Tweet** → Fetches timeline data and automatically likes a relevant post.

## Step-by-Step Process

1. **Connect Metamask Wallet**
   - Connect your Metamask wallet to **Sonic** or **Sonic Blaze Testnet**.
   - Obtain Sonic tokens from:
     - [Sonic Mainnet](https://my.soniclabs.com/)
     - [Sonic Testnet](https://testnet.soniclabs.com/)
2. **Start the Agent**
   - Click the **Start Agent** button to initiate the process.
   - A transaction is made to the **Sonic contract address** via Metamask.
   - Once the transaction is confirmed, the agent starts running.
3. **Perform Actions**
   - Use the available four actions:
     - **Post Tweet** (requires a prompt)
     - **Post Tweet with Image** (requires a prompt)
     - **Reply to Tweet** (automated using Ollama LLM)
     - **Like Tweet** (automated based on timeline data)

## Technologies Used

- **ZerePy**: A Python framework for deploying autonomous agents across multiple platforms and blockchains. It enables integration between social media, blockchain, and AI capabilities. [Documentation](https://www.zerepy.org/docs/intro)
- **X/Twitter API**: For fetching and posting tweets. [Docs](https://developer.x.com/en/docs/x-api)
- **Ollama**: AI model for generating tweet content. [Website](https://ollama.com/)
- **Stability AI**: Used for generating images for tweets. [Docs](https://platform.stability.ai/)
- **Frontend**: Built using **Next.js** and **TailwindCSS**. [Next.js Guide](https://nextjs.org/learn)

## Project Links

- **GitHub Repository**: [Link](https://github.com/ThisIsVedant/Decentralized-Autonomous-Twitter-Agent)
- **X/Twitter API Docs**: [Docs](https://developer.x.com/en/docs/x-api)
- **ZerePy Docs**: [Docs](https://www.zerepy.org/docs/intro)
- **Stability AI**: [Docs](https://platform.stability.ai/)
- **Ollama**: [Website](https://ollama.com/)
- **Next.js Docs**: [Docs](https://nextjs.org/learn)

## How to Run the Project

Follow these steps to set up and run the agents:

### 1. Clone the Repository

```bash
 git clone https://github.com/ThisIsVedant/Decentralized-Autonomous-Twitter-Agent
```

### 2. Install Dependencies

Navigate to the **ZerePy** folder and run:

```bash
 pip install -r requirements.txt
```

### 3. Ollama Setup

Start Ollama and Install an LLM Model

**Note:** Ensure you have Ollama installed. If not, install it from [Ollama's website](https://ollama.ai).

After installing Ollama, you need to install a large language model before using it. To use this project, you must install the llama3.2 model:

```sh
 ollama pull llama3.2
```

Before running the backend, start the Ollama software or start Ollama by executing the following command:

```sh
 ollama serve
```

### 4. Configure Environment Variables

Create a `.env` file inside the **ZerePy** folder and add the following details:

```env
SONIC_PRIVATE_KEY=''
TWITTER_USER_ID=''
TWITTER_USERNAME=''
TWITTER_CONSUMER_KEY=''
TWITTER_CONSUMER_SECRET=''
TWITTER_ACCESS_TOKEN=''
TWITTER_ACCESS_TOKEN_SECRET=''
STABILITY_AI_API_KEY=''
```

### 5. Start the Backend Server

Run the following command inside the **ZerePy** folder:

```bash
 uvicorn src.server.app:create_app --host 0.0.0.0 --port 8001
```

### 6. Start the Frontend

Navigate to the frontend folder and use a code editor like **WebStorm** or **Visual Studio Code**.

Run the following commands:

```bash
 yarn install
 yarn run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to access the UI.

### 7. Setup Metamask & Sonic Token

- Install **Metamask**.
- Add **Sonic Token** or **Sonic Blaze Testnet**.

### 8. Modify Contract Address & Transaction Amount (Optional)

You can update the **contract address** and **Sonic transaction amount** directly in the frontend as they are hardcoded.

## Future Enhancements

- **Automated Agent Scheduling** → Ability to schedule tweets and interactions at specific times.  
- **Advanced AI Content Generation** → Improve tweet quality using enhanced **Ollama AI** models.  
- **Sentiment Analysis** → Analyze tweet sentiment before posting.  
- **Multi-Chain Support** → Expand support for other blockchain networks beyond **Sonic**.  
- **Support for More AI Models** → Enable integration with additional AI models for better content generation.  
- **Multi-Platform Support** → Extend agent capabilities to multiple social media platforms beyond **X/Twitter**.  
- **More Decentralized Execution Features** → Enhance on-chain automation and execution for improved decentralization.  

## Conclusion

This project successfully integrates Web3, AI, and automation to create an **autonomous Twitter agent** powered by **Sonic blockchain**. With the ability to generate and post tweets, reply using AI, and interact with content seamlessly, it demonstrates a practical use case for **decentralized autonomous agents**. Future updates will bring more intelligent features and expanded blockchain support.
