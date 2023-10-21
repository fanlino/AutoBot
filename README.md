# Telegram Bot

## Creating Telegram Bot

You can clone this repository to create this application.

`app.py` is the file which does all the work. Make sure to update the `username` in app.py before running the script. 

As we are using sensitive information like tokens and secrets, we will use **Kubernetes Secrets** to store these and access them in the code

- `consumer_key` - Consumer Key
- `consumer_secret` - Consumer Secret
- `access_token` - OAuth Access Token
- `access_token_secret` - OAuth Access Token Secret

Start by encoding all the keys and secrets

```bash
echo -n 'chat_token' | base64
EncodedChatToken==

echo -n 'chat_id' | base64
EncodedChatId==
```

Create a new `secrets.yaml` file and add the encoded strings as data. We would be accessing these secrets from our code. Refer to our [documentation on accessing secrets in Fission](https://fission.io/docs/usage/function/access-secret-cfgmap-in-function/) from code.

```yaml
apiVersion: v1
kind: Secret
metadata:
  namespace: default
  name: telegram-secret
data:
  chat_token: EncodedChatToken==
  chat_id:  EncodedChatId==
type: Opaque
```

Deploy the secret using `kubectl apply -f secrets.yaml`

## Steps to Execute

Create a Python environment

```bash
fission environment create --name python --image fission/python-env-3.10 --builder fission/python-builder-3.10
```

Create a zip archive as sample.zip archive by executing package.sh script

```bash
./package.sh
```

Create a Package

```bash
fission package create --name autobot-pkg --sourcearchive pkg.zip --env python --buildcmd "./build.sh"
```

Create the tweetbot fission function

```bash
fission fn create --name autobot --pkg autobot-pkg --env python --entrypoint "app.main" --secret telegram-secret
```

## Test and Execute

Before you run the application, send a tweet to the user whom you're tracking. Test the function by executing the following command:

```bash
fission fn test --name autobot
```

You should see that your bot has replied to the latest tweet that mentioned you. It has also sent a note in your slack workspace.

There are multiple ways to automate this, in this case we are using Fission Time Trigger to execute the function every 1m. You can change this according to your needs.

```bash
fission timer create --name minute --function autobot --cron "@every 1m"
```

## Fission Spec

```bash
fission spec init
fission environment create --name python --image fission/python-env-3.10 --builder fission/python-builder-3.10 --spec
fission package create --name autobot-pkg --sourcearchive pkg.zip --env python --buildcmd "./build.sh" --spec
fission fn create --name autobot --pkg autobot-pkg --entrypoint "app.main" --secret telegram-secret --spec
fission timer create --name minute --function autobot --cron "@every 1m" --spec
```
