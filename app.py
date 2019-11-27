import json
import logging
import requests
import sys
import traceback

from flask import Flask, request, redirect
from flask_apscheduler import APScheduler
from objectify_json import ObjectifyJSON

from gh_token import get_token, store_token
from gh_utils import API_BASE_URL, add_pr_comment, make_github_api_call


log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:%(process)s:%(name)s:%(message)s')

# Create the Flask App.
app = Flask(__name__)


@app.route('/webhooks', methods=['POST'])
def process_message():
    log.info('Incoming webhook')
    webhook = ObjectifyJSON(request.json)

    # Let's react only when a new Pull Requests has been opened.
    if request.headers['X-Github-Event'] == 'pull_request' and str(webhook.action).lower() == 'opened':
        # Webhook schema - https://developer.github.com/v3/activity/events/types/#pullrequestevent
        add_pr_comment(webhook)
    else:
        log.info("Irrelavant webhook.")

    return 'GOOD'


@app.route("/authenticate/<app_id>", methods=["GET"])
def authenticate(app_id):
    """Incoming Installation Request. Accept and get a new token."""
    try:
        app_id = str(app_id)
        installation_id = request.args.get('installation_id')
        store_token(app_id, get_token(app_id, installation_id))

    except Exception:
        log.error("Unable to get and store token.")
        traceback.print_exc(file=sys.stderr)

    return redirect("https://www.github.com", code=302)


if __name__ == '__main__':
    app.run()