from json import dumps
from requests import post
from random import randint
from socket import gethostname
from sys import platform
from textwrap import wrap

GREETINGS = ["Kia ora!", "Howdy partner.", "G'day mate.", "What up g? :sunglasses:", "Ugh finally, this shit is done.", "Kachow! :racing_car:", "Kachigga! :racing_car:", "Sup dude.", "Woaaaaahhhh, would you look at that!", "Easy peasy.", "Rock on bro. :call_me_hand:", "Leshgoooooo!", "Let's get this bread!", "You're doing great dude. :kissing_heart:", "Another one bits the dust...", "Sup, having a good day?", "Yeeeeeeehaw cowboy! :face_with_cowboy_hat:"]  

if platform == "win32":
    SLACK_TOKEN = open("R:/admin/slack_token.txt", 'r').read().strip('\n')
elif platform == "linux":
    SLACK_TOKEN = open("/media/CivilSystems/admin/slack_token.txt", 'r').read().strip('\n')


def post_message_to_slack(where_to_post, message_type, identifier, message=None, greet=True):
    """
    Posts a message to a Slack Channel or User through the use of blocks.
    
    Parameters
    ----------
    where_to_post : String
        A string representing the (public or private) channel or User ID for the message to be sent to. Channels must start with a hastag, such as #smco_code_updates for example. To privately message someone, specify there User ID (which can be found by viewing their full profile and looking under the More section) such as U015WCS0XU6 for example.
    message_type : String
        A string representing what type of message this post should be. There are currently three options: Information, Failure and Success. Each one will post a different amount of blocks, with differnt styles of wording within them.
    identifier: String
        A string that will be used in the header to help identify which simulation the message is referring to. It is recommended that the length of the identifier is kept under 100 characters in order to display the header on one line.
    message: String
        If the message_type is Information or Failure, the message will be used in a section below a divider and will typically be a informative message or an error traceback for the two message_types respectively. 
    greet: Bool
        If True, post a cheerful greeting before the message.
   
    Returns
    -------
    None : No parameters are outputted
    
    """
    
    greeting = GREETINGS[randint(0, max(len(GREETINGS) - 1, 0))] + " " if greet else ""
    
    # Unfortunately, there is a 150 character limit on the header length, so split and send multiple if that is the case!
    header_lines = ["{}  |  {}  |  Running on {}".format(message_type.title(), identifier, gethostname())]
    if len(header_lines[0]) > 150:
        header_lines = wrap(header_lines[0], width=100, break_long_words=False, break_on_hyphens=False)
    
    blocks=[]
    for header in header_lines:
        blocks.append({"type": "header", 
                        "text":
                            {"type": "plain_text", 
                            "text": header, 
                            "emoji": True}
                        })
    blocks.append({"type": "divider"})

    if message_type.title() ==  "Information":
        blocks.append({ "type": "section",
                        "text": {"type": "mrkdwn",
                                "text": message}
                        })       
    elif message_type.title() == "Success":
        blocks.append({"type": "section",
                        "text": {"type": "mrkdwn",
                                "text": "{}It is my pleasure to inform you that the program has been a success. The full results are available by veiwing the terminal/code editors screen on the aforementioned computer.".format(greeting)}
                        })       
    elif message_type.title() == "Failure":  
        blocks.extend([{"type": "section",
                        "text": {"type": "mrkdwn",
                                "text": "{}It is unfortunate that I must inform that something went wrong. The full details are available by viewing the terminal/code editors screen on the aforementioned computer.".format(greeting)}
                        },
                    {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": "*Error Traceback:*"}
                    },
                    {"type": "divider"},
                    {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": message.strip("Traceback (most recent call last):\r\n  ")}
                    }])

    _ = post('https://slack.com/api/chat.postMessage', {
    'token': SLACK_TOKEN,
    'channel': where_to_post,
    'blocks': dumps(blocks)})
    