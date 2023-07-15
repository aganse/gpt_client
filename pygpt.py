""" Little python-based terminal/readline based ChatGPT CLI app.

Start via:  python3 pygpt.py

Note you must have your OPENAI_API_KEY env var set.
And you must be in an environment with the following python packages:
  * openai (for the open api)
  * rich (for the markdown/syntax-highlighting formatting)

"""

from cmd import Cmd
import os
import re
import readline
import urllib

from bs4 import BeautifulSoup
import openai
from rich.console import Console
from rich.markdown import Markdown


openai.api_key = os.environ["OPENAI_API_KEY"]
code_theme = "default"  # "default" (for light), "monokai" (for dark)

# set up the readline handling:
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
history_file = os.path.expanduser('~/.gpt_history')
if os.path.exists(history_file):
    readline.read_history_file(history_file)
console = Console()

# set basic behavior of the ai agent here
messages = [
    {"role": "system", "content": "The following is a conversation with "
     "an AI assistant. The assistant is helpful, creative, clever, friendly. "
     "Its answers are polite and friendly but brief, only rarely exceeding "
     "a single paragraph when really necessary to explain a point. "
     "The assistant labels all markdown code snippets with the code language. "
     "Mathematical answers and expressions written by the assistant are "
     "always formatted in unicode characters rather than latex, using full "
     "mathematical notation rather than programming notation. "
     "The assistant only very occasionally uses emojis to show enthusiasm."}
]


def generate_response(input, supplemental, model):
    if input:
        messages.append({"role": "user", "content": input})
        if supplemental is not None:
            messages.append({"role": "user", "content": supplemental})
        metadata = {}
        try:
            chat = openai.ChatCompletion.create(
                model=model, messages=messages
            )
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            metadata["prompt_tokens"] = chat.usage.prompt_tokens
            metadata["completion_tokens"] = chat.usage.completion_tokens
        except openai.OpenAIError as e:
            errormsg = e.response["error"]["message"]
            console.print(f"[bold red]OpenAI API Error:[/bold red] {errormsg}")
            return ""
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")
            return ""
    return reply, metadata


class GptInterpreter(Cmd):
    model = "gpt-4"  # set this in one spot with default & cmdline arg
    # model = "gpt-3.5-turbo"  # set this in one spot with default & cmdline arg
    # prompt = "Me: "
    # prompt = "\x01\n\033[01;32m\x02Me:\x01\033[00m\x02 "  # color
    prompt = "\x01\033[1m\x02Me:\x01\033[0m\x02 "  # bold only
    # prompt = "\n\033[01;32m😃\033[37m\033[01;32m Me:\033[00m "
    # gptprompt = "GPT: "
    # gptprompt = "\x01\033[01;36m\x02GPT:\x01\033[00m\x02 "
    gptprompt = "\x01\033[1m\x02GPT:\x01\033[0m\x02 "  # bold only
    # gptprompt = "\033[01;32m🤖\033[37m\033[01;36m GPT:\033[00m "
    # gptprompt = "\n[bold blue]GPT[/bold blue]:  "  # use 'rich' formatting

    def __init__(self):
        Cmd.__init__(self)
        self.cmdloop(intro=f"Welcome to model {self.model}!\nNote you can "
                     "enter page contents of a URL by putting the URL in "
                     "double chevrons like this: <<URL>>\n")

    def cmdloop(self, intro):
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            print()
            self.do_exit()
        except EOFError:
            self.do_exit()

    def emptyline(self):
        pass

    def do_exit(self, line=None):
        print(" Ok, goodbye...")
        readline.write_history_file(history_file)
        return True

    do_EOF = do_exit  # enables ctrl-D to exit

    def default(self, line):
        if line == "exit" or line == "quit" or line == "q":
            return self.do_exit()

        # check for possible URL in user-submitted text
        webpagetext = None
        skip_input = False
        url_search = re.search("<<(.*)>>", line, re.IGNORECASE)
        if url_search:
            url = url_search.group(1)
            try:
                maxchar = 15000
                html = urllib.request.urlopen(url).read()
                webpagetext = BeautifulSoup(html, "html.parser").get_text()
                webpagetext = webpagetext.replace("\n", " ")
                orig_length_webpagetext = len(webpagetext)
                if orig_length_webpagetext > maxchar:
                    user_input = input("Warning: length of webpagetext string "
                        f"= {len(webpagetext)} which will rapidly use up your "
                        f"tokens; also must be truncated to first {maxchar} "
                        "chars.  Continue?  (yN): ")
                    if user_input.lower() != "y" and user_input.lower() != "yes":
                        skip_input = True
                    else:
                        webpagetext = ("GPT please note that due to length, "
                            f"webpage truncated to first {maxchar} characters,"
                            f"about {maxchar/orig_length_webpagetext*100.0}%, "
                            "which may affect your interpretation of it:\n"
                            "------------------\n") + webpagetext
                        webpagetext = webpagetext[:maxchar]
            except urllib.error.HTTPError as e:
                print(f"Sorry, HTTP error: {e.code} in trying to access URL..")
                line = re.sub("<<.*>>", f"<<HTTP error {e.code}>>", line)
                skip_input = True
            except urllib.error.URLError as e:
                print(f"Sorry, URL error: {e.reason} in trying to access URL.")
                line = re.sub("<<.*>>", f"<<URL error {e}>>", line)
                skip_input = True
            # let's also catch this error:
            # openai.error.RateLimitError: That model is currently overloaded
            # with other requests. You can retry your request, or contact us
            # through our help center at help.openai.com if the error persists.
            # (Please include the request ID 73ac0a3985379d57d5992b960d7ec24f
            # in your message.)

        if not skip_input:
            reply, metadata = generate_response(line, webpagetext, self.model)

            # handle markdown and syntax highlighting and word/line wrapping;
            # technically could just use print() instead, just not as pretty:
            console.print(f"[grey78][{metadata['prompt_tokens']} prompt-tokens; "
                          "includes resubmission of all history this session plus "
                          "page contents of any urls given...][/grey78]")
            console.print(" ")
            console.print(Markdown(self.gptprompt + reply, code_theme=code_theme))
            console.print(f"[grey78][{metadata['completion_tokens']} "
                          "completion-tokens just for this response...][/grey78]")
            console.print(" ")


def main():
    GptInterpreter()


if __name__ == '__main__':
    main()
