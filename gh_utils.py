import json
import logging
import requests
import sys

from requests.auth import HTTPBasicAuth

from gh_token import retrieve_token
from bot_config import API_BASE_URL, GITHUB_TOKEN, GITHUB_USER

log = logging.getLogger(__name__)


"""
GITHUB REST API CALL FN
========================

Use this function to make API calls to the GitHub REST api

For example:

# GET the current user
me = make_github_rest_api_call('login')

# POST to create a comment on a PR

new_comment = make_github_rest_api_call(
    'repos/my_org/my_repo/issues/31/comments',
    'POST', {
        'body': "Hello there, thanks for creating a new Pull Request!"
    }
)


"""


def make_github_rest_api_call(api_path, method='GET', params=None):
    """Send API call to Github using a personal token."""

    token = retrieve_token()

    # Required headers.
    headers = {'Accept': 'application/vnd.github.antiope-preview+json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'}

    try:
        if method.upper() == 'POST':
            response = requests.post(f'{API_BASE_URL}/{api_path}', headers=headers, data=json.dumps(
                params))
        elif method.upper() == 'GET':
            response = requests.get(f'{API_BASE_URL}/{api_path}', headers=headers)
        else:
            raise Exception('Invalid Request Method.')
    except:
        log.exception("Could not make a successful API call to GitHub.")
