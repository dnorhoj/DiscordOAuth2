# DiscordOAuth
This was made for testing purposes by @dnorhoj#1337
The idea is that the source is available, so that people doesn't have to try their way through like I am while making this.

## How to install
Guide to setting up the application.

### Create app
First go to [discord developer portal](https://discordapp.com/developers/applications).
Then click on the **New Application** button.

Give the application a name, and click **Create**.
Give it a description if you feel like it.

Write down the *client id* and *client secret*, we will need it later.

### Set up OAuth
Navigate to the OAuth2 section.

![](https://i.imgur.com/dcQ1JUR.png)

Click **Add Redirect** and in the box type in `localhost:8000/callback` and save.

### Configure the code
Clone the source, and open it up in a [text editor](https://code.visualstudio.com/).

Create a file called `auth.py` in the source folder.
Copy+paste this and change what you need to:

```py
id = '[Put Client ID here]'
secret = '[Client Secret]'
secretkey = "[A random string of chars]"
redirect = 'http://localhost:8000/callback'
scopes = 'email identify guilds'
```

### Install requirements
Before continuing, you need to have the following requirements:
* Python 3
* Pip

To install the requirements, simply open a cmd/terminal window and navigate to the source code directory.

Now do `pip install -r requirements.txt`

### Start the app
Now launch `main.py` in a command window.
It should start the flask application.

Go to `localhost:8000` in your browser.

## More
Have a good day.
