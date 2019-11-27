import json
import logging
import requests
import sys

from flask import Flask, request
from objectify_json import ObjectifyJSON
from requests.auth import HTTPBasicAuth

from github_api import API_BASE_URL, make_github_api_call


log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:%(process)s:%(name)s:%(message)s')

# Requied constants. Fill in your details. Do not check this in with these credentials.
GITHUB_USER = ""
GITHUB_TOKEN = ""
API_BASE_URL = "https://api.github.com"

# Create the Flask App.
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def process_message():
    log.info('Incoming webhook')
    webhook = ObjectifyJSON(request.json)

    # Let's react only when a new Pull Requests has been opened.
    if request.headers['X-Github-Event'] == 'pull_request' and str(webhook.action).lower() == 'opened':
        # This webhooks has this schema - https://developer.github.com/v3/activity/events/types/#pullrequestevent
        add_pr_comment(webhook)
    else:
        log.info("Irrelavant webhook.")

    return 'GOOD'


def add_pr_comment(webhook):
    log.info('New Pull Request opened. Adding comment.')

    # Gather the requried information from the payload to send a successful request to GitHub REST API.
    repo_full_name = str(webhook.repository.full_name)
    pr_number = str(webhook.pull_request.number)

    comments_url = f'{API_BASE_URL}/repos/{repo_full_name}/issues/{pr_number}/comments'
    body = "Hello there, thanks for creating a new Pull Request!"

    # Make the API call.
    make_github_api_call(comments_url, 'POST', {'body': body})


def make_github_api_call(url, method, params=None):
    """Send API call to Github using a personal token."""

    # Required headers.
    headers = {'Accept': 'application/vnd.github.antiope-preview+json', 'Content-Type': 'application/json'}

    try:
        if method.upper() == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(params), auth=HTTPBasicAuth(GITHUB_USER, GITHUB_TOKEN))
        elif method.upper() == 'GET':
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(GITHUB_USER, GITHUB_TOKEN))
        else:
            raise Exception('Invalid Request Method.')
    except:
        log.exception("Could not make a successful API call to GitHub.")


if __name__ == '__main__':
    app.run()