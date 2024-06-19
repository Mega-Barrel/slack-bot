"""
Script to integrate Slack API
"""
import os
from flask import Flask
from dotenv import load_dotenv
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter

load_dotenv()

# initialize a flask application
app = Flask(__name__)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(
    slack_signing_secret,
    "/slack/events",
    app
)

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(token=slack_bot_token)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    """
    Method to read incoming messages
    """
    message = event_data.get('event', {})
    if message.get("subtype") is None and "hi" in message.get('text'):
        print(message['text'])
        # user_name = slack_client.users_info(user=user_id)
        # channel = message["channel"]
        # message = f"Hello {user_name['user']['name']}! :tada:"
        # slack_client.chat_postMessage(channel=channel, text=message)
    else:
        user_id = message["user"]
        channel_id = message["channel"]
        print(event_data)
        print()
        print(slack_client.users_info(user=user_id))
        print()
        print(slack_client.conversations_info(channel=channel_id))

if __name__ == '__main__':
    app.run(debug=True)
