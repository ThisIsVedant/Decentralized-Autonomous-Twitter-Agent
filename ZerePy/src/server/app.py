import time

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import asyncio
import threading
from pathlib import Path

from src.actions.twitter_actions import generate_image
from src.prompts import POST_TWEET_PROMPT, REPLY_TWEET_PROMPT

from src.cli import ZerePyCLI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server/app")

app = FastAPI(title="ZerePy Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class TweetRequest(BaseModel):
    """Model for receiving tweet prompts from the frontend"""
    prompt: str

class ActionRequest(BaseModel):
    """Request model for agent actions"""
    connection: str
    action: str
    params: Optional[List[str]] = []


class ConfigureRequest(BaseModel):
    """Request model for configuring connections"""
    connection: str
    params: Optional[Dict[str, Any]] = {}


class ServerState:
    """Simple state management for the server"""

    def __init__(self):
        self.cli = ZerePyCLI()
        self.agent_running = False
        self.agent_task = None
        self._stop_event = threading.Event()

        self.cli._load_agent_from_file("social_agent")

    def _run_agent_loop(self):
        """Run agent loop in a separate thread"""
        try:
            log_once = False
            while not self._stop_event.is_set():
                if self.cli.agent:
                    try:
                        if not log_once:
                            logger.info("Loop logic not implemented")
                            log_once = True

                    except Exception as e:
                        logger.error(f"Error in agent action: {e}")
                        if self._stop_event.wait(timeout=30):
                            break
        except Exception as e:
            logger.error(f"Error in agent loop thread: {e}")
        finally:
            self.agent_running = False
            logger.info("Agent loop stopped")

    async def start_agent_loop(self):
        """Start the agent loop in background thread"""
        if not self.cli.agent:
            raise ValueError("No agent loaded")

        if self.agent_running:
            raise ValueError("Agent already running")

        self.agent_running = True
        self._stop_event.clear()
        self.agent_task = threading.Thread(target=self._run_agent_loop)
        self.agent_task.start()

    async def stop_agent_loop(self):
        """Stop the agent loop"""
        if self.agent_running:
            self._stop_event.set()
            if self.agent_task:
                self.agent_task.join(timeout=5)
            self.agent_running = False


class ZerePyServer:
    def __init__(self):
        self.app = app
        self.state = ServerState()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        async def root():
            """Server status endpoint"""
            return {
                "status": "running",
                "agent": self.state.cli.agent.name if self.state.cli.agent else None,
                "agent_running": self.state.agent_running,
            }

        @self.app.get("/agents")
        async def list_agents():
            """List available agents"""
            try:
                agents = []
                agents_dir = Path("agents")
                if agents_dir.exists():
                    for agent_file in agents_dir.glob("*.json"):
                        if agent_file.stem != "general":
                            agents.append(agent_file.stem)
                return {"agents": agents}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/agents/{name}/load")
        async def load_agent(name: str):
            """Load a specific agent"""
            try:
                self.state.cli._load_agent_from_file(name)
                return {
                    "status": "success",
                    "agent": name
                }
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.get("/connections")
        async def list_connections():
            """List all available connections"""
            if not self.state.cli.agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            try:
                connections = {}
                for name, conn in self.state.cli.agent.connection_manager.connections.items():
                    connections[name] = {
                        "configured": conn.is_configured(),
                        "is_llm_provider": conn.is_llm_provider
                    }
                return {"connections": connections}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/agent/action")
        async def agent_action(action_request: ActionRequest):
            """Execute a single agent action"""
            if not self.state.cli.agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            try:
                result = await asyncio.to_thread(
                    self.state.cli.agent.perform_action,
                    connection=action_request.connection,
                    action=action_request.action,
                    params=action_request.params
                )
                return {"status": "success", "result": result}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.post("/agent/start")
        async def start_agent():
            """Start the agent loop"""
            if not self.state.cli.agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            try:
                await self.state.start_agent_loop()
                return {"status": "success", "message": "Agent started"}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.post("/agent/stop")
        async def stop_agent():
            """Stop the agent loop"""
            try:
                await self.state.stop_agent_loop()
                return {"status": "success", "message": "Agent stopped"}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.post("/connections/{name}/configure")
        async def configure_connection(name: str, config: ConfigureRequest):
            """Configure a specific connection"""
            if not self.state.cli.agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            try:
                connection = self.state.cli.agent.connection_manager.connections.get(name)
                if not connection:
                    raise HTTPException(status_code=404, detail=f"Connection {name} not found")

                success = connection.configure(**config.params)
                if success:
                    return {"status": "success", "message": f"Connection {name} configured successfully"}
                else:
                    raise HTTPException(status_code=400, detail=f"Failed to configure {name}")

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/connections/{name}/status")
        async def connection_status(name: str):
            """Get configuration status of a connection"""
            if not self.state.cli.agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            try:
                connection = self.state.cli.agent.connection_manager.connections.get(name)
                if not connection:
                    raise HTTPException(status_code=404, detail=f"Connection {name} not found")

                return {
                    "name": name,
                    "configured": connection.is_configured(verbose=True),
                    "is_llm_provider": connection.is_llm_provider
                }

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/connections/sonic/balance")
        async def get_sonic_balance():
            """Fetch Sonic Balance"""
            if not self.state.cli.agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            try:
                # Get Sonic connection
                connection = self.state.cli.agent.connection_manager.connections.get("sonic")
                if not connection:
                    raise HTTPException(status_code=404, detail="Sonic connection not found")

                # Check if the connection is configured
                if not connection.is_configured():
                    raise HTTPException(status_code=400, detail="Sonic connection is not configured")

                # Fetch balance (assuming Sonic API has a `get_balance()` method)
                balance = connection.get_balance()
                return {"status": "success", "balance": balance}

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/agent/like-tweet")
        async def like_tweet():
            """Automatically like a tweet from the agent's timeline"""
            agent = self.state.cli.agent  # Ensure the agent exists

            if not agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            tweet_connection = agent.connection_manager.connections.get("twitter")
            timeline_data = tweet_connection.read_timeline(count=1)
            agent.logger.info(timeline_data)
            tweet_id = timeline_data[0]["id"] if timeline_data else ""

            if timeline_data:
                if not tweet_id:
                    return False

                agent.connection_manager.perform_action(
                    connection_name="twitter",
                    action_name="like-tweet",
                    params=[tweet_id]
                )
                agent.logger.info("✅ Tweet liked successfully!")
                return {"status": "success", "message": "Tweet liked successfully!", "timeline": timeline_data}
            else:
                agent.logger.info("\n👀 No tweets found to like...")
            return False

        @app.post("/agent/post-tweet")
        async def post_tweet(request: TweetRequest):
            """Post a tweet with a prompt from the frontend"""
            agent = self.state.cli.agent  # Ensure agent exists

            if not agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            current_time = time.time()
            last_tweet_time = agent.state.get("last_tweet_time", 0)

            # Check if we can post a new tweet based on the interval
            if current_time - last_tweet_time < agent.tweet_interval:
                return {"status": "failed", "message": "Tweet interval not elapsed"}

            agent.logger.info("\n📝 Generating a new tweet from the provided prompt")

            # Use the prompt from the frontend
            prompt = request.prompt
            agent.logger.info(f"user prompt: {prompt}")
            connection = self.state.cli.agent.connection_manager.connections.get("ollama")
            tweet_text = connection.generate_text(prompt=prompt, system_prompt=POST_TWEET_PROMPT)
            agent.logger.info(f"tweet text: {tweet_text}")

            if not tweet_text:
                raise HTTPException(status_code=400, detail="Tweet generation failed")

            agent.logger.info("\n🚀 Posting tweet:")
            agent.logger.info(f"'{tweet_text}'")

            # Perform the tweet post action
            result = agent.connection_manager.perform_action(
                connection_name="twitter",
                action_name="post-tweet",
                params=[tweet_text]
            )

            # Update last tweet time
            agent.state["last_tweet_time"] = current_time

            return {"status": "success", "message": "Tweet posted successfully!", "result": result, "tweetText": tweet_text}

        @app.post("/agent/reply-to-tweet")
        async def reply_to_tweet():
            """Reply to tweet"""

            agent = self.state.cli.agent  # Ensure agent exists

            if not agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            # tweet_connection = agent.connection_manager.connections.get("twitter")
            # timeline_data = tweet_connection.read_timeline(count=1)
            # agent.logger.info(f"timeline: {timeline_data}")
            # tweet_id = timeline_data[0]["id"] if timeline_data else ""
            # agent.logger.info(f"Tweet id: {tweet_id}")

            timeline_data = [{'id': '1898512735530553766', 'text': 'RT @tesla_na: The future is golden and bright', 'author_id': '44196397', 'created_at': '2025-03-08T23:14:43.000Z', 'edit_history_tweet_ids': ['1898512735530553766'], 'author_name': 'Elon Musk', 'author_username': 'elonmusk'}]
            tweet_id = timeline_data[0]["id"]
            if timeline_data:
                if not tweet_id:
                    return

                connection = self.state.cli.agent.connection_manager.connections.get("ollama")
                base_prompt = REPLY_TWEET_PROMPT.format(tweet_text=timeline_data[0]['text'])
                system_prompt = agent._construct_system_prompt()
                reply_text = connection.generate_text(prompt=base_prompt, system_prompt=system_prompt)

                if reply_text:
                    agent.logger.info(f"\n🚀 Posting reply: '{reply_text}'")
                    agent.connection_manager.perform_action(
                        connection_name="twitter",
                        action_name="reply-to-tweet",
                        params=[tweet_id, reply_text]
                    )
                    agent.logger.info("✅ Reply posted successfully!")
                return {"status": "success", "message": "Tweet Reply successfully!", "timeline": timeline_data, "replyText" : reply_text}

            else:
                agent.logger.info("\n👀 No tweets found to reply to...")
                return False

        @app.post("/agent/post-with-image")
        async def post_with_image(request: TweetRequest):
            """Post image tweet  with a prompt from the frontend"""

            agent = self.state.cli.agent  # Ensure agent exists

            if not agent:
                raise HTTPException(status_code=400, detail="No agent loaded")

            current_time = time.time()

            if "last_tweet_time" not in agent.state:
                last_tweet_time = 0
            else:
                last_tweet_time = agent.state["last_tweet_time"]

            if current_time - last_tweet_time >= agent.tweet_interval:
                agent.logger.info("\n📝 GENERATING NEW TWEET WITH IMAGE")


                # Generate tweet text
                prompt = request.prompt
                agent.logger.info(f"user prompt: {prompt}")
                connection = agent.connection_manager.connections.get("ollama")
                tweet_text = connection.generate_text(prompt=prompt, system_prompt=POST_TWEET_PROMPT)
                agent.logger.info(f"tweet text: {tweet_text}")

                # Generate image using Stable Diffusion
                # Usage in tweet posting function
                try:
                    agent.logger.info("\n🎨 Generating image with Stable Diffusion...")
                    image_path = generate_image(prompt, "./generated_image.jpeg")
                    agent.logger.info(f"\n📷 Image generated and saved to: {image_path}")
                except Exception as e:
                    agent.logger.error(f"\n❌ Failed to generate image: {e}")
                    return False

                if tweet_text and image_path:
                    agent.logger.info("\n🚀 Posting tweet with image:")
                    agent.logger.info(f"'{tweet_text}'")
                    agent.logger.info(f"📷 Image path: {image_path}")

                    result = agent.connection_manager.perform_action(
                        connection_name="twitter",
                        action_name="post-tweet-with-image",
                        params=[tweet_text, image_path]
                    )
                    agent.state["last_tweet_time"] = current_time
                    agent.logger.info("\n✅ Tweet with image posted successfully!")
                    return {"status": "success", "message": "Tweet posted successfully!","result": result, "tweetText": tweet_text}
                else:
                    agent.logger.error("\n❌ Failed to generate tweet or image.")
                    return False
            else:
                agent.logger.info("\n👀 Delaying post until tweet interval elapses...")
                return False




def create_app():
    server = ZerePyServer()
    return server.app
