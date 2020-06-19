import requests
import json
import os

data = {
    "text": "Hi this is for testing"
}

webhook = os.environ.get("webhook_slack")
requests.post(webhook, json.dumps(data))