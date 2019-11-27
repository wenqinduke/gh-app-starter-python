import datetime
import json
import jwt
import logging
import os
import requests
import sys
import time
import traceback
import uuid


log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:%(process)s:%(name)s:%(message)s')


def get_token(app_id, installation_id):
    """Get a token from GitHub."""
    token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    temp_state = str(uuid.uuid4())
    private_key = get_private_key()

    # Required params.
    params = {
        'iat': int(time.time()),
        'exp': int(time.time() + 500),
        'iss': app_id,
        'state': temp_state
    }

    try:
        # Create a Json Web Token object with the required params.
        encoded = jwt.encode(params, private_key, algorithm='RS256').decode("utf-8")
        headers = {'Accept': 'application/vnd.github.machine-man-preview+json', 'Authorization': f'Bearer {encoded}'}

        # Send request to GitHub.
        response = requests.post(token_url, headers=headers)
    
    except Exception as exc:    
        log.error(f"Could get token for App - {app_id}")
        traceback.print_exc(file=sys.stderr)
        raise

    # Add Installation ID and App ID to the Response before returning it
    response_json = json.loads(response.text)
    response_json['installation_id'] = installation_id
    response_json['app_id'] = app_id

    return json.dumps(response_json)


def store_token(app_id, token_json):
    if app_id and token_json:
        try:
            if os.path.exists(f".secret-{app_id}"):
                os.unlink(f".secret-{app_id}")
            
            with open(f".secret-{app_id}", 'w') as secret_file:
                secret_file.write(json.dumps(token_json))

        except Exception as exc:    
            log.error(f"Could not write secret file for App - {app_id}")
            traceback.print_exc(file=sys.stderr)

    else:
        log.error(f"Invalid token for app - {app_id}")


def peek_app_token(app_id):
    """Peek on secret file that has the token, deserialize it and return the dict."""
    if not os.path.exists(f".secret-{app_id}"):
        return None

    try:
        with open(f".secret-{app_id}") as secret_file:
            return json.loads(secret_file.read())

    except Exception as exc:    
        log.error(f"Could not read secret file for App - {app_id}")
        traceback.print_exc(file=sys.stderr)


def refresh_token(app_id):
    """Refresh tokens of an individual app."""
    try:
        deserialized_message = peek_app_token(app_id)
        app_id = deserialized_message.get('app_id')
        installation_id = deserialized_message.get('installation_id')
        store_token(app_id, get_token(app_id, installation_id))

    except Exception as exc:
        log.error(f"Could not refresh token for app - {app_id}")
        traceback.print_exc(file=sys.stderr)


def retrieve_token(app_id):
    """Retrieve latest token. If expired, refresh it."""
    try:
        deserialized_message = peek_app_token(app_id)

        expires_at = deserialized_message.get('expires_at')
        if expires_at and check_expired_time(expires_at):  # Token is good, return it
            return deserialized_message
        else:  # Token expired, refresh it
            refresh_token(app_id)

            deserialized_message = peek_app_token(app_id)
            expires_at = deserialized_message.get('expires_at')
            if expires_at and check_expired_time(expires_at):  # Token is good, return it
                return deserialized_message
            else:
                raise  # When all else fails

    except Exception as exc:
        log.error(f"Could not refresh token for app - {app_id}")
        traceback.print_exc(file=sys.stderr)

    return None


def get_private_key():
    """Read private key from hidden file and return it."""
    if not os.path.exists(".private-key"):
        return None

    try:
        with open(".private-key") as secret_file:
            return secret_file.read()

    except Exception as exc:    
        log.error("Could not read private key.")
        traceback.print_exc(file=sys.stderr)


def check_expired_time(date_time_str, date_time_format=None, buffer=300):
    """Given a DateTime string, check if that time has expired while taking into account the buffer time."""
    date_format = "%Y-%m-%dT%H:%M:%SZ"  # "2019-09-16T19:04:13Z"
    date_time_obj = datetime.datetime.strptime(date_time_str, date_format)

    return date_time_obj.timestamp() > datetime.datetime.utcnow().timestamp() + buffer