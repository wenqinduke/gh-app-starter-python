# Python GitHub App

This app is meant to serve as an application to help you onboard to the GitHub ecosystem and start using GitHub Webhooks & Apps.

## Getting Started

### Initial Project Setup

- Clone/Fork this repo
- Generate your virutal environment

```sh
python3 -m venv venv
```

- Activate your environment

```sh
source venv/bin/activate
```

- Install dependencies

```sh
pip3 install -r requirements.txt
```

- Run the app

```
flask run
```


## How to set it up and use it

- Generate a Personal Access Token on GitHub - https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
- Copy `.env.example` to `.env`
- Add this Personal Access Token and your GitHub Username to `.env` on Line 7 and 14.

## How to use Webhooks

- Create a new repository at https://github.com/gh-training/
- Visit https://smee.io/ and click on `Start a new Channel` and note the URL
- Go to your Repository's Settings -> Webhooks -> Add Webhook
- Enter the Smee URL from the above step here and set Content Type to `application/json`, skip the secret and select `Send me everything`
- Open a new terminal window and navigate to where you checked out this repo and activate virual environment as above - `source venv/bin/activate`
- Run `pysmee forward <SMEE_URL> http://127.0.0.1:5000/webhook` - this will forward all events to your app.

## See it in action

- Go ahead and create a new Pull Request in the repository you just added the webhook to
- Voila! A new comment should be added to it.

## Legal

&copy; 2019 LinkedIn
