# openai_llm_tools
Bash CLI tools to access the OpenAI LLM APIs, starting with a ChatGPT client.

OpenAI serves a ChatGPT web client on its webpage, but I really prefer to keep
certain things in the terminal, especially if I often copy/paste the results
into a neighboring tmux pane.  There's another popular CLI based ChatGPT client
out there called [Shell-GPT](https://pypi.org/project/shell-gpt) which has many
nice aspects but I made my CLI more narrowly focused, with output formatting
that I prefer, and it's only about 100 lines in a single Bash script so it's
easy for me to follow exactly what it's doing.

Be aware any client outside of the one on OpenAI's website (which is free for
ChatGPT) requires an [API key](https://platform.openai.com/account/api-keys) to
access the API, and making calls to this API does 
[cost money](https://openai.com/pricing#language-models).
However, it's really cheap if just using it oneself for reference queries (as
opposed to serving it out to zillions of other users to use in a web app).
Like in two days of fairly heavy usage I've racked up a whole $0.20.


`chatgpt`: Basic command-line ChatGPT-API client in Bash, implementing shell
tools like readline, syntax highlighting, prompt formatting, etc.  No command
line arguments yet; currently the few options are at the top of the bash script
(I'll move them to command line args soon).  So for now simply run the
./chatgpt script and then you're at the client prompt.  Contents auto-wrap to
the width of the current terminal window.

------
![screenshot](screenshot.png "Screenshot")
------

## Usage

1. Get an [API key](https://platform.openai.com/account/api-keys) (requires
creating an OpenAI account if you don't have one already) and put that key in
your shell environment, e.g. `export OPENAI_API_KEY=xyz123...`

2. Install `jq` and `rlwrap`, which are standard linux tools.
(`sudo apt install jq` and `sudo apt install rlwrap`, or `brew install jq` and
`brew install rlwrap`...)

3. It's not required, but if you wish to have the syntax highlighting and other
formatting in running the client, you'll need to install `rich-cli`, either 
via `brew install rich-cli` or `pip install rich-cli`.
If you choose to skip installing this, set `use_formatter=0` in
the top of the chatgpt script.  (It's set to use it by default `=1`).  It can
always be changed later.

4. Run the chatgpt script - no arguments currently - and that'll start the
client.  Ctrl-C to quit.  The client's command line uses readline, so all the
usual hot keys / editing work including a command history via Ctrl-P and Ctrl-N.
Expect that there are definitely slow times for this popular API service.


## Dependencies
* bash
* jq
* rlwrap
* rich-cli (optional, adds syntax highlighting and other such formatting)


## Refs / more info

Model choices/explanations at:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models

More detailed usage instructions for these models in terms of crafting queries:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions

Details about additional chatgpt parameters for tuning functionality:

  https://platform.openai.com/docs/api-reference/chat/create

