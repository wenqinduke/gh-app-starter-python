import json
import logging

from flask import Flask, request
from objectify_json import ObjectifyJSON


log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:%(process)s:%(name)s:%(message)s')

app = Flask(__name__)
GITHUB_TOKEN = ""
API_BASE_URL = ""



@app.route('/webhook', methods=['POST'])
def process_message(message):
    log.info('Processing message...')
    webhook = ObjectifyJSON(request.json)

    if request.headers['X-Github-Event'] == 'pull_request' and str(webhook.action).lower() == 'opened':
        add_pr_comment(webhook)

    return 'GOOD'


def add_pr_comment(webhook):
    log.info('Processing Trunk Status Check')
    repo_full_name = str(webhook.repository.full_name)
    pr_number = None
    author = None

    comments_url = f'{API_BASE_URL}/repos/{repo_full_name}/issues/{pr_number}/comments'


def make_github_api_call(url, method, params=None):
    """Send API call to Github using a personal token."""
    headers = {'Accept': 'application/vnd.github.antiope-preview+json', 'Content-Type': 'application/json', 'Authorization': f'token {GITHUB_TOKEN}'}

    if method.upper() == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(params))
    elif method.upper() == 'GET':
        response = requests.get(url, headers=headers)
    else:
        raise Exception('Invalid Request Method.')

    print(response.status_code)
    return json.loads(response.text)


if __name__ == '__main__':
    app.run()