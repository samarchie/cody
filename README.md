<br />
<p align="center">
  <img src="https://avatars.slack-edge.com/2021-08-02/2324270040231_205f77f3db7ed63557bd_512.png" alt="Logo" width="250">
  </a>

  <h3 align="center">Cody</h3>

  <p align="center">
    Your friendly neighhbourhood Python bot to communicate and update you through Slack
    <br />
    <br />
    <a href="https://github.com/samarchie/cody/issues">Request Feature or Report Bug</a>
  </p>
</p>
<br />

### About Cody

Cody is API that allows users to write public/private messages, silent messages, upload files and control most aspects of Slack. Cody is pretty flexible - in the fact it doesn't have to be called from Python but can be called from most platforms using the slack token through an API call. However, as the team mainly works in Python, cody.py has been established to help you take care of mundane tasks.

### Getting Started

1. Create a Slack App, named Cody, to allow external programs (such as Python) to post messages to the Civil Systems Slack workspace. To do so, create the bot through a [Slack App](https://api.slack.com/apps), choose 'Bots' and 'Permissions' for the 'Features and Functionality', **and most importantly**: set the OAuth & Permissions Bot Scope to: **```chat:write, channels:read, users:read and files:write```**.

2. From the Slack App webpage, locate the 'Bot User OAuth Token' on the OAuth & Permissions page, and save this in a textfile at ```R:/admin/slack_token.txt```
This wil be in the form alike: ```xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy```

3. In your project virtual environmnet or global Python environment, install the required packages in ```requirements.txt```.

4. Inside your project code, place the following lines to import and use the function to post a message to slack.
```sh
from os.path import join; from sys import path
path.append(join("{}".format("R:\\" if platform == "win32" else "/media/CivilSystems"), "admin", "cody"))
from slack import post_message_to_slack, post_files_to_slack
post_message_to_slack(channel="#spatial_optimization", message_type="Information", identifier="Simulation 1", message="Hello World!", greet=True, silent_username="Sam")
post_files_to_slack(channel="#spatial_optimization", ["filepath1", "filepath2", "filepath3"], message='Here are my 3 files!', greet=True)
```

<br>

> I wish you all the best in using Cody to its full extent, and that you never recieve an error message in your code :heart:
> Yours truly, Sam Archie
