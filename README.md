# openai_llm_tools
CLI tools to access the OpenAI LLM APIs, starting with a ChatGPT client.

> **TL;DR:** get an OpenAPI key and put it in env var OPENAI_API_KEY, make a
> python env and pip install the openai, rich, & beautifulsoup4 packages, then
> run **python pygpt.py**.  Bashgpt is older, has some problems, and is just
> for reference.

OpenAI serves a ChatGPT web client on its webpage, but I really prefer to keep
certain things in the terminal, especially if I often copy/paste the results
into a neighboring tmux pane.  Plus scripts like this offer me the ability to
experiment with more detailed prompt engineering and the API output.

Be aware that any client outside of the one on OpenAI's website (which is free
for ChatGPT) requires an [API key](https://platform.openai.com/account/api-keys)
to access the API, and making calls to this API does 
[cost money](https://openai.com/pricing#language-models).
However, it's super cheap if just using it oneself for reference queries (e.g.
I generally just use it as a stand-in for Google/Wikipedia/StackOverflow),
as opposed to serving it out to zillions of other users to use in a web app.
Like in my initial two days of fairly heavy usage I racked up a whole $0.20;
after a few months of light-moderate usage since then, I'm now up to $0.50.

Two scripts here so far, which both provide very similar-looking CLI experience
for ChatGPT:

`pygpt`: Basic command-line ChatGPT-API client in Python, implementing packages
and tools like readline, syntax highlighting, prompt formatting, etc.  No command
line arguments yet; currently the few options are set inside the script, but I'll
add a click (or other) CLI soon that includes these.  Contents auto-wrap to the
width of the current terminal window.

`bashgpt`: *(deprecated)*:
Basic command-line ChatGPT-API client in Bash, implementing shell
tools like readline, syntax highlighting, prompt formatting, etc.  No command
line arguments; currently the few options are at the top of the bash script
(ideally I'd move them to command line args).  Contents auto-wrap to the width
of the current terminal window.
**Danger:** a trouble in this bash client is stabilizing escape-character
handling over looping/reuse of messages.  Escaping works in first few rounds but
can get lost later which breaks the app; usually it's a round or two after code
snippets that include characters like `*`, `\`, and `%` and can even cause
file listing of your local directory to leak into the prompt sent to ChatGPT API.
So I've moved on to the python client but leaving this bash one for reference.


------
![screenshot](screenshot.png "Screenshot")
------


## Usage

1. Get an [API key](https://platform.openai.com/account/api-keys) (requires
creating an OpenAI account if you don't have one already) and put that key in
your shell environment, e.g. `export OPENAI_API_KEY=xyz123...`

2. Install dependencies and run the app:

    1. for Python-based `pygpt`:
     
        1. create and enter a python environment, e.g. `python3 -m venv ~/.venv; source ~/.venv/bin/activate`
    
        2. install two python package dependencies:
           `pip install openai rich beautifulsoup4`
    
        3. run the app: `python /path/to/openai_llm_tools/pygpt.py`
           The client's command line uses readline, so all the usual hot keys /
           editing work including a command history via Ctrl-P and Ctrl-N.
    
        4. quit via: `quit` or `exit` or `q` or `ctrl-D` or `ctrl-C`.
     
    2. for Bash-based `bashgpt`:
     
        1. install `jq` and `rlwrap`, which are standard linux tools.
           (e.g. `sudo apt install jq` and `sudo apt install rlwrap`, or
           `brew install jq` and `brew install rlwrap`...)
    
        2. it's not required for bashgpt, but if you wish to have the syntax
           highlighting and other formatting in running the client, you'll need to
           install `rich-cli`, either via `brew install rich-cli` or
           `pip install rich-cli`.  If you choose to skip installing this, set
           `use_formatter=0` in the top of the bashgpt script.  (It's set to use it
           by default `=1`).  It can always be changed later.
    
        3. run the app: `/path/to/openai_llm_tools/bashgpt`
           no arguments currently - and that'll start the client.  Ctrl-C to quit.
           The client's command line uses readline, so all the usual hot keys /
           editing work including a command history via Ctrl-P and Ctrl-N.

3. Know that OpenAI's GPT API is an immensely popular service right now and
that regardless of which client you use (one of these CLI ones, their website
one, or any other), expect that there are definitely slow times.  I've
experienced response wait times of up to 20sec and once-in-a-while responses
of "too busy right now".  But *usually* the responses are within a few seconds.
These waits/too-busy are not about the client apps but about the API service.


## Refs / more info

Model choices/explanations at:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models

More detailed usage instructions for these models in terms of crafting queries:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions

Details about additional chatgpt parameters for tuning functionality:

  https://platform.openai.com/docs/api-reference/chat/create

Thoughts for values of temperature and top_p for different use-cases:

  https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api-a-few-tips-and-tricks-on-controlling-the-creativity-deterministic-output-of-prompt-responses/172683

  Use Case                 Temp  Top_p  Description
  ------------------------ ----  -----  ------------------------------------
  Code Generation           0.2  0.1    Generates code that adheres to established patterns and conventions. Output is more deterministic and focused. Useful for generating syntactically correct code.
  Creative Writing          0.7  0.8    Generates creative and diverse text for storytelling. Output is more exploratory and less constrained by patterns.
  Chatbot Responses         0.5  0.5    Generates conversational responses that balance coherence and diversity. Output is more natural and engaging.
  Code Comment Generation   0.3  0.2    Generates code comments that are more likely to be concise and relevant. Output is more deterministic and adheres to conventions.
  Data Analysis Scripting   0.2  0.1    Generates data analysis scripts that are more likely to be correct and efficient. Output is more deterministic and focused.
  Exploratory Code Writing  0.6  0.7    Generates code that explores alternative solutions and creative approaches. Output is less constrained by established patterns.


