import json
import logging
import requests
import sys

from requests.auth import HTTPBasicAuth

# from gh_oauth_token import retrieve_token
from bot_config import API_BASE_URL, GH_USER_TOKEN, GH_USER

log = logging.getLogger(__name__)


def make_github_rest_api_call(api_path, method='GET', params=None):
    """Send API call to Github using a personal token.

Use this function to make API calls to the GitHub REST api

For example:

`GET` the current user
---
```py
me = make_github_rest_api_call('login')
```

`POST` to create a comment on a PR
---
```py
new_comment = make_github_rest_api_call(
    'repos/my_org/my_repo/issues/31/comments',
    'POST', {
        'body': "Hello there, thanks for creating a new Pull Request!"
    }
)
```
    """

    # token = retrieve_token()
    token = GH_USER_TOKEN

    # Required headers.
    headers = {'Accept': 'application/vnd.github.antiope-preview+json',
               'Content-Type': 'application/json',
               #    'Authorization': f'Bearer {token}'
               }

    # API url
    url = f'{API_BASE_URL}/{api_path}'
    log.info(
        f'sending {method.upper()} request to {url} w/ data {json.dumps(params)}')
    try:
        if method.upper() == 'POST':
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(params),
                auth=HTTPBasicAuth(GH_USER, GH_USER_TOKEN)  # basic auth
            )
        elif method.upper() == 'GET':
            response = requests.get(
                url,
                headers=headers,
                auth=HTTPBasicAuth(GH_USER, GH_USER_TOKEN)  # basic auth
            )
        else:
            raise Exception('Invalid Request Method.')
    except:
        log.exception("Could not make a successful API call to GitHub.")
