# encoding: utf-8

import json
import totoboto
from flask import Flask, request, make_response, render_template

pyBot = totoboto.TotoBoto()
slack = pyBot.client

app = Flask(__name__)


def _event_handler(event_type, slack_event):
    if event_type == "pin_added":
        # Update the onboarding message
        pyBot.update_pin(slack_event)
        return make_response("Welcome message updates with pin", 200,)

    message = "You have not added an event handler for the %s" % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/totem", methods=["GET", "POST"])
def hears():

    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })
    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)

        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True)
