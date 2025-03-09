import os
import time

from dotenv import load_dotenv

from src.action_handler import register_action
from src.helpers import print_h_bar
from src.prompts import POST_TWEET_PROMPT, REPLY_TWEET_PROMPT
import requests

load_dotenv()
api_key = os.getenv("STABILITY_AI_API_KEY")

# Check if API key is loaded
if not api_key:
    raise ValueError("API key is missing. Ensure STABILITY_AI_API_KEY is set in the .env file.")

def generate_image(prompt: str, output_path: str):
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": 'jpeg',
        },
    )

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        return output_path
    else:
        raise Exception(str(response.json()))


@register_action("post-tweet-with-image")
def post_tweet_with_image(agent, **kwargs):
    current_time = time.time()

    if "last_tweet_time" not in agent.state:
        last_tweet_time = 0
    else:
        last_tweet_time = agent.state["last_tweet_time"]

    if current_time - last_tweet_time >= agent.tweet_interval:
        agent.logger.info("\n📝 GENERATING NEW TWEET WITH IMAGE")
        print_h_bar()

        # Generate tweet text
        text_prompt = POST_TWEET_PROMPT.format(agent_name=agent.name)
        tweet_text = agent.prompt_llm(text_prompt)

        # Generate image using Stable Diffusion
        # Usage in tweet posting function
        try:
            agent.logger.info("\n🎨 Generating image with Stable Diffusion...")
            prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
            image_path = generate_image(prompt, "./generated_image.jpeg")
            agent.logger.info(f"\n📷 Image generated and saved to: {image_path}")
        except Exception as e:
            agent.logger.error(f"\n❌ Failed to generate image: {e}")
            return False

        if tweet_text and image_path:
            agent.logger.info("\n🚀 Posting tweet with image:")
            agent.logger.info(f"'{tweet_text}'")
            agent.logger.info(f"📷 Image path: {image_path}")

            agent.connection_manager.perform_action(
                connection_name="twitter",
                action_name="post-tweet-with-media",
                params=[tweet_text, image_path]
            )
            agent.state["last_tweet_time"] = current_time
            agent.logger.info("\n✅ Tweet with image posted successfully!")
            return True
        else:
            agent.logger.error("\n❌ Failed to generate tweet or image.")
            return False
    else:
        agent.logger.info("\n👀 Delaying post until tweet interval elapses...")
        return False


@register_action("post-tweet")
def post_tweet(agent, **kwargs):
    current_time = time.time()

    if ("last_tweet_time" not in agent.state):
        last_tweet_time = 0
    else:
        last_tweet_time = agent.state["last_tweet_time"]

    if current_time - last_tweet_time >= agent.tweet_interval:
        agent.logger.info("\n📝 GENERATING NEW TWEET")
        print_h_bar()

        prompt = POST_TWEET_PROMPT.format(agent_name=agent.name)
        tweet_text = agent.prompt_llm(prompt)

        if tweet_text:
            agent.logger.info("\n🚀 Posting tweet:")
            agent.logger.info(f"'{tweet_text}'")
            agent.connection_manager.perform_action(
                connection_name="twitter",
                action_name="post-tweet",
                params=[tweet_text]
            )
            agent.state["last_tweet_time"] = current_time
            agent.logger.info("\n✅ Tweet posted successfully!")
            return True
    else:
        agent.logger.info("\n👀 Delaying post until tweet interval elapses...")
        return False


@register_action("reply-to-tweet")
def reply_to_tweet(agent, **kwargs):
    if "timeline_tweets" in agent.state and agent.state["timeline_tweets"] is not None and len(
            agent.state["timeline_tweets"]) > 0:
        tweet = agent.state["timeline_tweets"].pop(0)
        tweet_id = tweet.get('id')
        if not tweet_id:
            return

        agent.logger.info(f"\n💬 GENERATING REPLY to: {tweet.get('text', '')[:50]}...")

        base_prompt = REPLY_TWEET_PROMPT.format(tweet_text=tweet.get('text'))
        system_prompt = agent._construct_system_prompt()
        reply_text = agent.prompt_llm(prompt=base_prompt, system_prompt=system_prompt)

        if reply_text:
            agent.logger.info(f"\n🚀 Posting reply: '{reply_text}'")
            agent.connection_manager.perform_action(
                connection_name="twitter",
                action_name="reply-to-tweet",
                params=[tweet_id, reply_text]
            )
            agent.logger.info("✅ Reply posted successfully!")
            return True
    else:
        agent.logger.info("\n👀 No tweets found to reply to...")
        return False


@register_action("like-tweet")
def like_tweet(agent, **kwargs):
    if "timeline_tweets" in agent.state and agent.state["timeline_tweets"] is not None and len(agent.state["timeline_tweets"]) > 0:
        tweet = agent.state["timeline_tweets"].pop(0)
        tweet_id = tweet.get('id')
        if not tweet_id:
            return False

        is_own_tweet = tweet.get('author_username', '').lower() == agent.username
        if is_own_tweet:
            replies = agent.connection_manager.perform_action(
                connection_name="twitter",
                action_name="get-tweet-replies",
                params=[tweet.get('author_id')]
            )
            if replies:
                agent.state["timeline_tweets"].extend(replies[:agent.own_tweet_replies_count])
            return True

        agent.logger.info(f"\n👍 LIKING TWEET: {tweet.get('text', '')[:50]}...")

        agent.connection_manager.perform_action(
            connection_name="twitter",
            action_name="like-tweet",
            params=[tweet_id]
        )
        agent.logger.info("✅ Tweet liked successfully!")
        return True
    else:
        agent.logger.info("\n👀 No tweets found to like...")
    return False
