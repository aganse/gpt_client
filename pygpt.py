""" Little python-based terminal/readline based ChatGPT CLI app.

Start via:  python3 pygpt.py

Note you must have your OPENAI_API_KEY env var set.
And you must be in an environment with the following python packages:
  * openai (for the open api)
  * rich (for the markdown/syntax-highlighting formatting)
  * darkdetect (for putting code syntax or webpage into light/dark mode)
  * beautifulsoup4 (for reading contents of urls)

python3 -m venv .venv
source .venv/bin/activate
pip install openai rich darkdetect beautifulsoup4

"""

from cmd import Cmd
import os
import re
import readline
# import gnureadline as readline  # for macos
import urllib

from bs4 import BeautifulSoup
import darkdetect
# import gradio as gr
import openai
from rich.console import Console
from rich.markdown import Markdown


openai.api_key = os.environ["OPENAI_API_KEY"]


def submit_to_gpt(messages, model, temperature, top_p):

    metadata = {}
    try:
        chat = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        metadata["prompt_tokens"] = chat.usage.prompt_tokens
        metadata["completion_tokens"] = chat.usage.completion_tokens
    except openai.OpenAIError as e:
        errormsg = e.response["error"]["message"]
        print(f"OpenAI API Error: {errormsg}")
        return ""
    except openai.error.RateLimitError as e:
        print(f"Sorry, hit a too-many-users limit: {e.reason}.")
        return ""
    except openai.error.InvalidRequestError as e:
        print(f"Sorry, hit a too-long-submission limit: {e.reason}.")
        return ""
    except openai.error.Timeout as e:
        print(f"Sorry, request apparently timed out: {e.reason}.")
        return ""
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

    return reply, metadata


def get_url_contents(url_search):

    skip_input = False
    url = url_search.group(1)
    try:
        maxchar = 15000
        # values = {"name": "Michael Foord",
        #           "location": "Northampton",
        #           "language": "Python"}
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
        # resp = requests.get("https://www.embassy-worldwide.com", headers=headers)

        # data = urllib.parse.urlencode(values)
        # data = data.encode("ascii")
        req = urllib.request.Request(url, headers=headers)
        # req = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(req).read()
        # html = urllib.request.urlopen(url).read()
        webpagetext = BeautifulSoup(html, "html.parser").get_text()
        webpagetext = webpagetext.replace("\n", " ")
        orig_length_webpagetext = len(webpagetext)
        if orig_length_webpagetext > maxchar:
            user_input = input(
                "Warning: length of webpagetext string "
                f"= {len(webpagetext)} which will rapidly use up your "
                f"tokens; also must be truncated to first {maxchar} "
                "chars.  Continue?  (yN): ")
            if user_input.lower() != "y" and user_input.lower() != "yes":
                skip_input = True
            else:
                webpagetext = (
                    "GPT please note that due to length, "
                    f"webpage truncated to first {maxchar} characters,"
                    f"about {maxchar/orig_length_webpagetext*100.0}%, "
                    "which may affect your interpretation of it:\n"
                    "------------------\n") + webpagetext
                webpagetext = webpagetext[:maxchar]
    except urllib.error.HTTPError as e:
        print(f"Sorry, HTTP error: {e.code} in trying to access URL..")
        # line = re.sub("<<.*>>", f"<<HTTP error {e.code}>>", line)
        skip_input = True
    except urllib.error.URLError as e:
        print(f"Sorry, URL error: {e.reason} in trying to access URL.")
        # line = re.sub("<<.*>>", f"<<URL error {e}>>", line)
        skip_input = True
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        skip_input = True

    return webpagetext, skip_input


def generate_response(input,
                      messages=None,
                      model=None,
                      temperature=None,
                      top_p=None):
    """Check for input plugins (like webpage urls), retrieve them, submit input
    to GPT model and return reply.  Args set to None use default value."""

    # Set messages default here instead of inline to handle None='default'
    if model is None:
        model = "gpt-4"  # "gpt-3.5-turbo"
    if temperature is None:
        temperature = 1
    if top_p is None:
        top_p = 1
    if messages is None:
        messages = [{
            "role": "system", "content": "The following is a conversation with"
            " an AI assistant. The assistant is helpful, creative, friendly. "
            "Its answers are polite but brief, only rarely exceeding "
            "a single paragraph when really necessary to explain a point. "
            "The assistant labels all markdown code snippets with the code "
            "language. Mathematical answers and expressions written by the "
            "assistant are always formatted in unicode characters rather than "
            "latex, using full mathematical notation rather than programming "
            "notation. The assistant only very occasionally uses emojis to "
            "show enthusiasm."
        }]

    # check for possible URL in user-submitted text
    webpagetext = None
    skip_input = False
    url_search = re.search("<<(.*)>>", input, re.IGNORECASE)

    if url_search:
        webpagetext, skip_input = get_url_contents(url_search)

    if not skip_input:

        if input:
            messages.append({"role": "user", "content": input})
            if webpagetext is not None:
                messages.append({"role": "user", "content": webpagetext})

        # print("Debug generate_response :")
        # print(f"messages: {messages}")
        # print(f"model: {model}")
        # print(f"temperature: {temperature}")
        # print(f"top_p: {top_p}")

        reply, metadata = submit_to_gpt(messages,
                                        model,
                                        temperature,
                                        top_p)

    return reply, metadata


class CmdLineInterpreter(Cmd):
    """REPL command line interpreter based on built-in python Cmd package."""

    # Set default CmdLinInterpreter interface options:
    # prompt = "\x01\033[1m\x02Me:\x01\033[0m\x02 "  # bold only
    # prompt = "Me: "
    # prompt = "\x01\n\033[01;32m\x02Me:\x01\033[00m\x02 "  # color
    prompt = "\n\033[01;32m😃\033[37m\033[01;32m Me:\033[00m "
    # gptprompt = "\x01\033[1m\x02GPT:\x01\033[0m\x02 "  # bold only
    # gptprompt = "GPT: "
    # gptprompt = "\x01\033[01;36m\x02GPT:\x01\033[00m\x02 "
    gptprompt = "\033[01;32m🤖\033[37m\033[01;36m GPT:\033[00m "
    # gptprompt = "\n[bold blue]GPT[/bold blue]:  "  # use 'rich' formatting
    intro = ""
    allow_injections = True
    if darkdetect.isDark():
        code_theme = "monokai"
    elif darkdetect.isLight():
        code_theme = "default"
    history_file = os.path.expanduser('~/.gpt_history')

    # Set default GPT options (None means use the default in generate_response)
    messages = None
    model = None
    temperature = None
    top_p = None

    console = Console()

    def __init__(self,
                 prompt=None,
                 gptprompt=None,
                 code_theme=None,
                 intro=None,
                 messages=None,
                 model=None,
                 temperature=None,
                 top_p=None,
                 allow_injections=None,
                 history_file=None,
                 ):

        # If constructor args specified any of these variables, update defaults
        if prompt is not None:
            self.prompt = prompt
        if gptprompt is not None:
            self.gptprompt = gptprompt
        if code_theme is not None:
            self.code_theme = code_theme
        if intro is not None:
            self.intro = intro
        if messages is not None:
            self.messages = messages
        if model is not None:
            self.model = model
        if temperature is not None:
            self.temperature = temperature
        if top_p is not None:
            self.top_p = top_p
        if allow_injections is not None:
            self.allow_injections = allow_injections
        if history_file is not None:
            self.history_file = history_file

        # Initialize the greeting/intro message on startup
        Cmd.__init__(self)
        if self.model is not None:
            self.intro += f"model={self.model}  "
        if self.temperature is not None:
            self.intro += f"temp={self.temperature}  "
        if self.top_p is not None:
            self.intro += f"top_p={self.top_p}  "
        if self.allow_injections:
            self.intro += ("\nYou can enter page contents of a URL by putting "
                           "the URL in double chevrons like this: <<URL>> ")
        self.intro += "\n"
        self.cmdloop(intro=self.intro)

        # Set up the readline handling:
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        if os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)

    def cmdloop(self, intro):
        try:
            Cmd.cmdloop(self, self.intro)
        except KeyboardInterrupt:
            print()
            self.do_exit()
        except EOFError:
            self.do_exit()

    def emptyline(self):
        pass

    def do_exit(self, line=None):
        print(" Ok, goodbye...")
        readline.write_history_file(self.history_file)
        # readline.append_history_file(readline.get_current_history_length(),
        #                              self.history_file)

        return True

    do_EOF = do_exit  # enables ctrl-D to exit

    def default(self, line):
        if line == "exit" or line == "quit" or line == "q":
            return self.do_exit()

        # print("Debug CmdLineInterpreter check:")
        # print(f"messages: {self.messages}")
        # print(f"model: {self.model}")
        # print(f"temperature: {self.temperature}")
        # print(f"top_p: {self.top_p}")

        reply, metadata = generate_response(line,
                                            self.messages,
                                            self.model,
                                            self.temperature,
                                            self.top_p)

        # handle markdown and syntax highlighting and word/line wrapping;
        # technically could just use print() instead, just not as pretty:
        self.console.print(
            f"[grey78][{metadata['prompt_tokens']} prompt-tokens; "
            "includes resubmission of all history this session plus "
            "page contents of any urls given...][/grey78]")
        self.console.print(" ")
        self.console.print(
            Markdown(self.gptprompt + reply, code_theme=self.code_theme)
        )
        self.console.print(
            f"[grey78][{metadata['completion_tokens']} "
            "completion-tokens just for this response...][/grey78]"
        )
        self.console.print(" ")


# def runChatWebApp():
#     """Start a gradio-based webapp for the chat interface"""

#     def chat(user_input):
#         return "You said: " + user_input

#     iface = gr.Interface(chat, "text", "text", title="My Chat App")
#     iface.launch()


if __name__ == '__main__':

    CmdLineInterpreter(temperature=0.2, top_p=0.1)

    # runChatWebApp()  # for gradio
