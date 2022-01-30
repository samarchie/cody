from json import dumps
from requests import post
from random import randint

# Specify where to post the message. If it is a channel, place a hashtag in front. Otherwise, use the User ID such as: U015WDS0XU6
WHERE_TO_POST = "#smco_code_updates"
TOKEN_FP = "src/slack_token.txt"

GREETINGS = ["Kia ora!", "Howdy partner.", "G'day mate.", "What up g? :sunglasses:", "Ugh finally, this shit is done.", "Kachow! :racing_car:", "Kachigga! :racing_car:", "Sup dude.", "Woaaaaahhhh, would you look at that!", "Easy peasy.", "Rock on bro. :call_me_hand:", "Leshgoooooo!", "Let's get this bread!", "You're doing great dude. :kissing_heart:", "Another one bits the dust...", "Sup, having a good day?", "Yeeeeeeehaw cowboy! :face_with_cowboy_hat:"]  


def post_message_to_slack(messages, greet=True):
    """
    Function to post a message to a Slack channel or user.
    
    :param messages: A list of strings to post to the slack channel or user.
    :param greet: Default: True. If True, post a cheerful greeting before the message.

    """
    
    if greet:
        messages.insert(0, GREETINGS[randint(0, max(len(GREETINGS) - 1, 0))])
    
    blocks = []
    for message in messages:
        if type(message) == str:
            blocks.append(
            {"type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
                }
            })
        else:
            raise NotImplementedError("Sorry! {} is not currently accepted to be posted to slack!".format(message))

    _ = post('https://slack.com/api/chat.postMessage', {
        'token': open(TOKEN_FP, 'r').read().strip('\n'),
        'channel': WHERE_TO_POST,
        'blocks': dumps(blocks) if blocks else None
    })
