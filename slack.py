from random import sample
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from socket import gethostname
from sys import platform
from textwrap import wrap
from warnings import warn

GREETINGS = ["Kia ora!", "Howdy partner.", "G'day mate.", "What up g? :sunglasses:", "Ugh finally, this shit is done.", "Kachow! :racing_car:", "Kachigga! :racing_car:", "Sup dude.", "Woaaaaahhhh, would you look at that!", "Easy peasy.", "Rock on bro. :call_me_hand:", "Leshgoooooo!", "Let's get this bread!", "You're doing great dude. :kissing_heart:", "Another one bits the dust...", "Sup, having a good day?", "Yeeeeeeehaw cowboy! :face_with_cowboy_hat:"] 
HAPPY_EMOJIS = [":tada:", ":cheering_bec:", ":smiley_mitch:", ":ecstatic_tom:", ":partying_face:", ":happy_patrick:", ":happy_tom:", ":dab_tom:"]
SAD_EMOJIS = [":sad_will:", ":sad_will_and_lucy:", ":cry:", ":disappointed_relieved:", ":angry_will:"]

SLACK_TOKEN = open("R:/admin/slack_token.txt".format("R:" if platform == "win32" else "/media/CivilSystems"), 'r').read().strip('\n')

DEFAULT_USER = "U015WCS0XU6" # Usercode for Sam Archie
DEFAULT_CHANNEL = "#spatial_optimization" 


def post_message_to_slack(message_type, identifier, message=None, greet=True, silent=True):
    """
    Posts a message to a Slack Channel or User.
    
    Parameters
    ----------
    message_type : String
        A string representing what type of message this post should be. There are currently three options: Information, Failure and Success. Each one will post a different amount of blocks, with differnt styles of wording within them.
    identifier: String
        A string that will be used in the header to help identify which simulation the message is referring to. It is recommended that the length of the identifier is kept under 100 characters in order to display the header on one line.
    message: String
        If the message_type is Information or Failure, the message will be used in a section below a divider and will typically be a informative message or an error traceback for the two message_types respectively. 
    greet: Bool
        If True, post a cheerful greeting before the message.
    silent: Bool
        If True, post the message in the default channel but the message will be hidden to everyone on the channel except the default user.
   
    Returns
    -------
    None : No parameters are outputted
    
    """
    
    header, header_lines = generate_header(message_type, identifier) 
    blocks = generate_blocks(message_type, message, header_lines, greet)

    try:
        if silent:
            _ = WebClient(SLACK_TOKEN).chat_postEphemeral(channel=DEFAULT_CHANNEL, blocks=blocks, user=DEFAULT_USER, text=header)
        else:
            _ = WebClient(SLACK_TOKEN).chat_postMessage(channel=DEFAULT_CHANNEL, blocks=blocks, text=header)
    
    except SlackApiError as error:
        warn("The message could not be posted to slack. Error: {}".format(error.response["error"]), UserWarning)


def generate_header(message_type, identifier):
    """
    Generates a header, or a list of headers depending on the length of the header, to be used to quickly summarise the message to be posted to the Slack channel or User.
    
    Parameters
    ----------
    message_type : String
        A string representing what type of message this post should be. There are currently three options: Information, Failure and Success. Each one will post a different amount of blocks, with differnt styles of wording within them.
    identifier: String
        A string that will be used in the header to help identify which simulation the message is referring to. It is recommended that the length of the identifier is kept under 100 characters in order to display the header on one line.
   
    Returns
    -------
    header: String
        A sentence split into 3 main parts - 1) the message_type surrounded by emojis (if applicable), 2) the identifier and 3) the name of the machine the code is currently running on
    header_lines: List of Strings
        If the header is equal to or above 150 characters long, then the string is split into multiple strings and returned in a list.
    
    """
    
    if message_type == 'Success':
        emojis = sample(HAPPY_EMOJIS, 2)
        header = f'{emojis[0]} {message_type.title()} {emojis[1]}|  {identifier}  |  Running on {gethostname()}'

    elif message_type == "Failure":
        emojis = sample(SAD_EMOJIS, 2)
        header = f'{emojis[0]} {message_type.title()} {emojis[1]}|  {identifier}  |  Running on {gethostname()}'
    
    else:
        header = f'{message_type.title()}|  {identifier}  |  Running on {gethostname()}'
    
    # Unfortunately, there is a 150 character limit on the header length, so split and send multiple if that is the case!
    header_lines = [header]
    if len(header) > 150:
        header_lines = wrap(header, width=100, break_long_words=False, break_on_hyphens=False)

    return header, header_lines


def generate_blocks(message_type, message, header_lines, greet):
    """
    Generates the blocks, a JSON-based list of structured blocks presented as URL-encoded strings, to be used to display message to be posted to the Slack channel or User.

    Example:
    [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]
    
    Parameters
    ----------
    message_type : String
        A string representing what type of message this post should be. There are currently three options: Information, Failure and Success. Each one will post a different amount of blocks, with differnt styles of wording within them.
    identifier: String
        A string that will be used in the header to help identify which simulation the message is referring to. It is recommended that the length of the identifier is kept under 100 characters in order to display the header on one line.
    greet: Bool
        If True, post a cheerful greeting before the message.

    Returns
    -------
    blocks: List
        A JSON-based list of structured blocks presented as URL-encoded strings
    
    """

    greeting = sample(GREETINGS, 1)[0] + " " if greet else ""

    blocks=[]
    for header_line in header_lines:
        blocks.append({"type": "header", 
                        "text":
                            {"type": "plain_text", 
                            "text": header_line, 
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
                                "text": f"{greeting}It is my pleasure to inform you that the program has been a success."}
                        })       
    elif message_type.title() == "Failure": 
        # Strip away any output in stdout before the error message begins
        lookout_phrase = "Traceback (most recent call last):"
        if lookout_phrase in message:
            start_index = message.index(lookout_phrase) 
            message = message[start_index+len(lookout_phrase)]

        blocks.extend([{"type": "section",
                        "text": {"type": "mrkdwn",
                                "text": f"{greeting}It is unfortunate that I must inform that something went wrong."}
                        },
                    {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": "*Error Traceback:*"}
                    },
                    {"type": "divider"},
                    {"type": "section",
                    "text": {"type": "mrkdwn",
                            "text": message.strip("\r\n")}
                    }])
    
    return blocks


def post_file_to_slack(filenames, message, greet=True):
    """
    Posts a file to a Slack Channel or User.
    
    Parameters
    ----------
    filenames : String or List of Strings
        A string representing the filepath to the file to be posted, or a list of strings to post.
    message: String
        A text message to display above the file in the Slack channel, primarily used to describe or introduce the file uploaded. 
    greet: Bool
        If True, post a cheerful greeting before the message.
   
    Returns
    -------
    None : No parameters are outputted
    
    """

    greeting = sample(GREETINGS, 1)[0] + " " if greet else ""
    
    # In case only one file was passed in, then 
    if type(filenames) == str:
        filenames = [filenames]

    try:
        for filename in filenames:
            _ = WebClient(SLACK_TOKEN).files_upload(channels=DEFAULT_CHANNEL, initial_comment=greeting+message, file=filename)
    
    except SlackApiError as error:
        warn("The file could not be posted to slack. Error: {}".format(error.response["error"]), UserWarning)

