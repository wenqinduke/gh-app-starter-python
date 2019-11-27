# Python Webhooks Bot

This app is meant to serve as an application to help you onboard to the GitHub ecosystem and start using Webhooks.

## How to set it up and use it
* Generate a Personal Access Token on GitHub - https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
* Clone/Fork this repo
* Enter your GitHub Username and Access Token on Line 17 and 18 of app.py
* Generate your virutal environment - `python3 -m venv .env`
* Activate your environment - `source .env/bin/activate`
* Install dependencies - `pip3 install -r requirements.txt`
* Run the app - `python3 app.py`

## How to use Webhooks
* Create a new repository at https://github.com/li-playground/
* Visit https://smee.io/ and click on `Start a new Channel` and note the URL
* Go to your Repository's Settings -> Webhooks -> Add Webhook
* Enter the Smee URL from the above step here and set Content Type to `application/json`, skip the secret and select `Send me everything`
* Open a new terminal window and navigate to where you checked out this repo and activate virual environment as above - `source .env/bin/activate`
* Run `pysmee forward <SMEE_URL> http://127.0.0.1:5000/webhook` - this will forward all events to your app.

## See it in action
* Go ahead and create a new Pull Request in the repository you just added the webhook to
* Voila! A new comment should be added to it.
