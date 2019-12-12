import logging
from gh_utils import make_github_rest_api_call

"""
SPECIALIZED WEBHOOK HANDLERS 
=======================

Becaue we may receive many webhooks for many different reasons, it's a good idea
to "hand off" control from `process_message()` to a dedicated function ASAP.

This is a good place for these specialized handlers

"""
log = logging.getLogger(__name__)


def add_pr_comment(webhook):
    log.info('New Pull Request opened. Adding comment.')
