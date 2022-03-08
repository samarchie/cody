from random import sample
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from socket import gethostname
from sys import platform
from textwrap import wrap
from warnings import warn

GREETINGS = ["Kia ora!", "Howdy partner.", "G'day mate.", "What up g? :sunglasses:", "Ugh finally, this shit is done.", "Kachow! :racing_car:", "Kachigga! :racing_car:", "Sup dude.", "Woaaaaahhhh, would you look at that!", "Easy peasy.", "Rock on bro. :call_me_hand:", "Leshgoooooo!", "Let's get this bread!", "You're doing great dude. :kissing_heart:", "Another one bits the dust...", "Sup, having a good day?", "Yeeeeeeehaw cowboy! :face_with_cowboy_hat:"] 
HAPPY_EMOJIS = [":tada:", ":cheering-bec:", ":smiley_mitch:", ":ecstatic_tom:", ":partying_face:", ":happy-patrick:", ":happy_tom:", ":dabtom:"]
SAD_EMOJIS = [":sad_will:", ":sad_willandluci:", ":cry:", ":disappointed_relieved:", ":angywill:"]

BOT_USER_OAUTH_TOKEN = open("{}/admin/cody/bot_user_oauth_token.txt".format("R:" if platform == "win32" else "/media/CivilSystems"), 'r').read().strip('\n')


def post_message_to_slack(channel, message_type, identifier=None, message=None, greet=True, silent_username=None):
    """
    Posts a message to a Slack Channel or User.
    
    Parameters
    ----------
    channel: String
        A string representing the channel to post to. Note: if you keep on recieving a 'channel_not_found' error, note that a channel must start with a hashtag, and if that fails, then please check the spelling of the channel.
    message_type : String
        A string representing what type of message this post should be. There are currently three options: Information, Failure and Success. Each one will post a different amount of blocks, with differnt styles of wording within them.
    identifier: String
        A string that will be used in the header to help identify which simulation the message is referring to. It is recommended that the length of the identifier is kept under 100 characters in order to display the header on one line.
    message: String
        If the message_type is Information or Failure, the message will be used in a section below a divider and will typically be a informative message or an error traceback for the two message_types respectively. 
    greet: Bool
        If True, post a cheerful greeting before the message.
    silent_user: String or None
        If silent_user is specified, then the message is posted to the channel (irrelevant if public or private) but only the silent_user can see the message.
   
    Returns
    -------
    None : No parameters are outputted
    
    """
    
    if not channel.startswith("#"):
        channel = "#" + channel

    header, header_lines = generate_header(message_type, identifier) 
    blocks = generate_blocks(message_type, message, header_lines, greet)

    try:
        if silent_username != None:
            client = WebClient(token=BOT_USER_OAUTH_TOKEN)
            silent_user_id = get_users_information_from_name(silent_username, "id", client)
            _ = client.chat_postEphemeral(channel=channel, blocks=blocks, user=silent_user_id, text=header)
        else:
            _ = WebClient(token=BOT_USER_OAUTH_TOKEN).chat_postMessage(channel=channel, blocks=blocks, text=header)
    
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

    if identifier == None:
        return "", None

    if message_type == 'Success':
        emojis = sample(HAPPY_EMOJIS, 2)
        header = f'{emojis[0]} {message_type.title()} {emojis[1]} |  {identifier}  |  Running on {gethostname()}'

    elif message_type == "Failure":
        emojis = sample(SAD_EMOJIS, 2)
        header = f'{emojis[0]} {message_type.title()} {emojis[1]} |  {identifier}  |  Running on {gethostname()}'
    
    else:
        header = f'{message_type.title()} |  {identifier}'
    
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

    if header_lines != None:
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


def post_file_to_slack(channel, filenames, message, greet=True):
    """
    Posts a file to a Slack Channel or User.
    
    Parameters
    ----------
    channel: String
        A string representing the channel to post to. Note: if you keep on recieving a 'channel_not_found' error, note that a channel must start with a hashtag, and if that fails, then please check the spelling of the channel.
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

    if not channel.startswith("#"):
        channel = "#" + channel

    greeting = sample(GREETINGS, 1)[0] + " " if greet else ""
    
    # In case only one file was passed in, then chuck the string into a list by itself
    if type(filenames) == str:
        filenames = [filenames]

    try:
        inital_comment_sent = False
        for filename in filenames:
            if not inital_comment_sent:
                _ = WebClient(token=BOT_USER_OAUTH_TOKEN).files_upload(channels=channel, initial_comment=greeting+message, file=filename)
                inital_comment_sent = True
            else:
                _ = WebClient(token=BOT_USER_OAUTH_TOKEN).files_upload(channels=channel, file=filename)
    
    except SlackApiError as error:
        warn("The file could not be posted to slack. Error: {}".format(error.response["error"]), UserWarning)


def get_users_information_from_name(user_name, wanted_information, client):
    """
    Retrieves a specified *wanted_information* attribute of a user by the name of *user_name*. The *user_name* can be the full name of the individual or their display name. If no exact matches are found, then possible matches are considered by their full name, display name and by first name and surname.
    
    Parameters
    ----------
    user_name : String
        A string representing the name of the user to be contacted, e.g. 'Sam Archie' or 'tom'. 
    wanted_information: String
        A string representing the  
    greet: Bool
        If True, post a cheerful greeting before the message.
   
    Returns
    -------
    None : No parameters are outputted
    
    """

    # Change the user_name to title case so we can == compare it with the other fields
    user_name = user_name.title()
    
    # Create lists for exact and possible matches
    exact_matches = []
    possible_matches = []

    # Query the client for a list of members
    members = client.users_list()["members"]

    for member in members:
        # If inactive user or is a bot then continue to the next
        if member["deleted"] or member["is_bot"]:
            continue
        
        # Check for exact results of id! E.g. the user passed in the actual id of the person, so why bother looking any further!
        if member.get("id", "") == user_name:
            return user_name
        
        # Check for exact mataches against the profile
        profile_details = member.get("profile", {})
        if profile_details.get("real_name", "").title() == user_name:
            exact_matches.append(member)
        elif profile_details.get("display_name", "").title() == user_name:
            exact_matches.append(member)
        elif profile_details.get("real_name_normalized", "").title() == user_name:
            exact_matches.append(member)
        elif profile_details.get("display_name_normalized", "").title() == user_name:
            exact_matches.append(member)

        # Check for possible matches
        elif user_name in member.get("id", ""):
            possible_matches.append(member)
        elif user_name in profile_details.get("real_name", "").title():
            possible_matches.append(member)
        elif user_name in profile_details.get("display_name", "").title():
            possible_matches.append(member)
        elif user_name in profile_details.get("real_name_normalized", "").title():
            possible_matches.append(member)
        elif user_name in profile_details.get("display_name_normalized", "").title():
            possible_matches.append(member)
        elif user_name.split(" ")[0] in profile_details.get("first_name", "").title():
            possible_matches.append(member)
        elif user_name.split(" ")[-1] in profile_details.get("last_name", "").title():
            possible_matches.append(member)

    
    if len(exact_matches) == 1:
        # Best case scenario!
        chosen_user_details = exact_matches[0]

    elif len(exact_matches) > 1:
        print(f"Multiple users detected with the user_name '{user_name}'. Please define which user you are indending to post to from the current list:\n")
        counter = 1
        for exact_match in exact_matches:
            print(f"Possible Match {counter}:")
            print(exact_match, end="\n")
            counter +=1 
        correct_individual_number = input(f"From this list, which number (from 1 to {len(exact_matches)}) was the user you were wishing to post locate?")
        chosen_user_details = exact_matches[correct_individual_number - 1]
    
    else:
        if len(possible_matches) == 1:
            chosen_user_details = possible_matches[0]
            print(f"No exact matches were found for '{user_name}. However, multiple possible matches exists. Please define which user you are indending to post to from the current list:\n")
            counter = 1
            for possible_match in possible_matches:
                print(f"Possible Match {counter}:")
                print(possible_match, end="\n")
                counter +=1 
            correct_individual_number = input(f"From this list, which number (from 1 to {len(possible_matches)}) was the user you were wishing to post locate?")
            chosen_user_details = possible_matches[correct_individual_number - 1]

    # Now grab the wanted_information from the chosen_user_details
    if wanted_information in chosen_user_details:
        chosen_information = chosen_user_details[wanted_information]
    elif wanted_information in chosen_user_details["profile"]:
        chosen_information = chosen_user_details["profile"][wanted_information]
    else:
        keys = sorted(set(list(chosen_user_details.keys()) + list(chosen_user_details["profile"].keys())))
        correct_wanted_information = input(f"The user name {user_name} was found but the wanted information {wanted_information} is not within the recorded details. Please choose from the following:\n {keys}")
        if correct_wanted_information in chosen_user_details:
            chosen_information = chosen_user_details[correct_wanted_information]
        elif correct_wanted_information in chosen_user_details["profile"]:
            chosen_information = chosen_user_details["profile"][correct_wanted_information]
    
    return chosen_information