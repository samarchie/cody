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

### Purpose

The purpose of Cody is two-fold:
1. To send messages to a designated person or channel to notify you of code updates
2. To send files to a designated person or channel


### Installation

##### If installing for the first time into the Slack Workspace:

1. Create a Slack API App, named Cody, to allow external programs (such as Python) to post messages to the Civil Systems Slack workspace. To do so, create the bot through a [Slack App](https://api.slack.com/apps), choose 'Bots' and 'Permissions' for the 'Features and Functionality', **and most importantly**: set the OAuth & Permissions Bot Scope to at least allow: 

| Bot Token Scope   | Description                                       |
|-------------------|---------------------------------------------------|
| chat:write        | Send messages as @cody                            |
| chat:write.public | Send messages to channels @cody isn't a member of |
| files:write       | Upload, edit, and delete files as Cody            |
| im:write          | Start direct messages with people                 |
| users:read        | View people in a workspace                        |

2. From the Slack App webpage, locate the 'Bot User OAuth Token' on the OAuth & Permissions page, and save this in a textfile at ```R:/admin/bot_user_oauth_token.txt```
This wil be in the form alike: ```xoxb-17653672481-19874698323-pdFZKVeTuE8sk7oOcBrzbqgy```

##### Installing into your Python environment

3. In your project virtual environmnet or global Python environment, install the [required packages](requirements.txt) using: ```pip install -r requirements.txt```.

4. Inside your project code, place the following lines to import and use the function to post a message to slack.
```sh
import sys
sys.path.append("{}/admin/cody".format("R:" if sys.platform == "win32" else "/media/CivilSystems"))
from cody import post_message_to_slack, post_files_to_slack
```

### Usage

Once imported, Cody is easy to use and the doc-strings exist to walk you through each variable. The examples below should guide you which each keyword does and the output that Cody can achieve.

##### Example 1: Information Post
```sh
post_message_to_slack(where_to_post="Sam", message_type="Information", identifier="Example Post", message="This is the first example of using Cody to personally message yourself! :tada:", greet=True) 
```
![Image](docs/info_screenshot.png)

##### Example 2: Hidden Public Post
```sh
post_message_to_slack(where_to_post="#random", message_type="Information", identifier="A Wonderful Introduction", message="This is the first example of using Cody to personally message yourself in a general channel but only the nominated person can see it! :tada:", greet=False, silent_username="Sam") 
```
![Image](docs/hidden_screenshot.png)

##### Example 3: Error Post
```sh
try:
    raise ValueError("This is an example error")
except:
    import traceback
    post_message_to_slack(where_to_post="Sam", message_type="Failure", identifier="Some Project", message=traceback.format_exc(), emojis=True)
```
![Image](docs/error_screenshot.png)

##### Example 4: Files Post
```sh
post_files_to_slack(where_to_post="Sam", filenames=[r"R:\projects\urban-optim\figures\colourbar.pdf", r"R:\projects\urban-optim\figures\nz.png"], message="Here are the completed files from today's analysis", greet=True)
```
![Image](docs/files_post_screenshot.png)


### Things to Remember

1. This is an API service, and it has its own rate limits as defined by the [Slack Rate Limits](https://api.slack.com/docs/rate-limits)
Posting message: Varies but most likely 1 message per second
Posting message hidden to 1 person: 100 messages per minute
Posting files: 20 files per minute

2. The API key allows access for anyone to post into CivilSystems Slack
Do not share the API key, which is stored in the ```bot_user_oauth_token.txt``` file. If uploaded to Github or the internet, it will be cancelled and I will have to generate a new key for us all to post again.

3. Be considerate as anyone can post anywhere or to anywhere anonymously under the "Cody" name

<br>

> I wish you all the best in using Cody to its full extent, and that you never recieve an error message in your code :heart:
> Yours truly, Sam Archie
