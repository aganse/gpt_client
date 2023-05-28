""" Little python-based terminal/readline based ChatGPT CLI app.

Start via:  python3 pygpt.py

Note you must have your OPENAI_API_KEY env var set.
And you must be in an environment with the following python packages:
  * openai (for the open api)
  * rich (for the markdown/syntax-highlighting formatting)

"""

from cmd import Cmd
import os
import readline

import openai
from rich.console import Console
from rich.markdown import Markdown


openai.api_key = os.environ["OPENAI_API_KEY"]

# set up the readline handling:
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
history_file = os.path.expanduser('~/.gpt_history')
if os.path.exists(history_file):
    readline.read_history_file(history_file)
console = Console()

# set basic behavior of the ai agent
messages = [
    {"role": "system", "content": "The following is a conversation with "
     "an AI assistant. The assistant is helpful, creative, clever, friendly. "
     "Its answers are polite and friendly but brief, only rarely exceeding "
     "a single paragraph when really necessary to explain a point. "
     "The assistant labels all markdown code snippets with the code language. "
     "Mathematical answers and expressions written by the assistant should "
     "are always formatted in unicode characters rather than latex. "
     "The assistant uses occasional emojis in writing to show enthusiasm."}
]


def generate_response(input):
    # hmm "if input:" doesn't seem to catch empty input as expected...?
    # might have to do with escape chars in prompt...?
    # works at first but not after there's been a response from gpt...
    if input:
        messages.append({"role": "user", "content": input})
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
        except openai.OpenAIError as e:
            errormsg = e.response["error"]["message"]
            console.print(f"[bold red]OpenAI API Error:[/bold red] {errormsg}")
            return ""
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")
            return ""
    return reply


class GptInterpreter(Cmd):
    model = "gpt-3.5-turbo"  # set this in one spot with default & cmdline arg
    # prompt = "\033[1mMe:\033[0m "  # replaces default of "(Cmd) " in cmdloop
    prompt = "\n\033[01;32m😃\033[37m\033[01;32m Me:\033[00m "
    # gptprompt = "\033[1mGPT:\033[0m "
    gptprompt = "\033[01;32m🤖\033[37m\033[01;36m GPT:\033[00m "
    # gptprompt = "\n[bold blue]GPT[/bold blue]:  "  # use 'rich' formatting

    def __init__(self):
        Cmd.__init__(self)
        self.cmdloop(intro=f"Welcome to model {self.model}!\n")

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
        print("in default()")
        if line == "exit" or line == "quit" or line == "q":
            return self.do_exit()

        output = generate_response(line)

        # handle markdown and syntax highlighting and word/line wrapping;
        # technically could just use print() instead, just not as pretty:
        console.print(" ")
        console.print(Markdown(self.gptprompt + output))
        console.print(" ")


def main():
    GptInterpreter()


if __name__ == '__main__':
    main()
