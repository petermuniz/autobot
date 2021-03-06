from slackeventsapi import SlackEventAdapter
from slack import WebClient
from slack.errors import SlackApiError
import os

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(slack_bot_token)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "Hello" in message.get('text'):
        channel = message["channel"]
        message = "Howdy <@%s>! :tada:" % message["user"]
        #slack_client.api_call("chat.postMessage", channel=channel, text=message)
        response = slack_client.chat_postMessage(
            channel=channel,
            text=message
        )
        assert response["ok"]
    elif message.get("subtype") is None and "Begone" in message.get('text'):
        channel = message["channel"]
        message = "Fine, BYE! :fb-sad:"
        #slack_client.api_call("chat.postMessage", channel=channel, text=message)
        response = slack_client.chat_postMessage(
            channel=channel,
            text=message
        )
        assert response["ok"]
    else:
        print("command not found")

# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    timestamp = event["item"]["ts"]
    #text = ":%s:" % emoji
    #slack_client.api_call("chat.postMessage", channel=channel, text=text)
    response = slack_client.reactions_add(
        channel=channel,
        name=emoji,
        timestamp=timestamp
    )

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
