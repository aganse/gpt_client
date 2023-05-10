# openai_llm_tools
Bash CLI tools to access the OpenAI LLM APIs, starting with a ChatGPT client.

OpenAI serves a ChatGPT web client on its webpage, whereas this is a CLI in the
terminal for those of us who prefer that when possible (especially in my own
use I'm generally either verifying mathematical steps or asking ChatGPT for
code snippets that I'm pasting elsewhere in the same terminal.  There's another
popular CLI based ChatGPT client out there called 
[Shell-GPT](https://pypi.org/project/shell-gpt)
which has nice aspects but also some functionality I'd like to avoid such as
execution of ChatGPT results; this one I made is more narrowly focused, with
output formatting that I prefer, and is <100 lines in a single Bash script so
it's easy for me to follow exactly what it's doing.
Do note that any client outside of the one on OpenAI's website (which is free
for ChatGPT only) requires an
[API key](https://platform.openai.com/account/api-keys)
to access the API, and that making calls to this API does 
[cost money](https://openai.com/pricing#language-models).
However, notice that it's REALLY cheap as long as the context is just using
it oneself for reference (as opposed to serving it out to zillions of other
users to use in a web app).  In the past few days I've been using this script
to access ChatGPT, ie gpt-3.5-turbo, moderately heavily, and from that have
racked up a grand total by now of $0.20.  (Surely pricing will vary over time
and depend on details, but it gives you some frame of reference.)


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

1. Get yourself an 
[API key](https://platform.openai.com/account/api-keys).
(Requires creating an OpenAI account if you don't have one already.)

2. Put that key in your shell environment, e.g. `export OPENAI_API_KEY=xyz123...`

3. It's not required, but if you wish to have the syntax highlighting and other
formatting in running the client, you'll need to `pip install rich-cli`, whether
you prefer to do so in a python environment or in your user environment (for the
latter, ie applying everywhere in your linux account, append `--user` to the end
of that pip command line).  If you choose to skip this, set `use_formatter=0` in
the top of the chatgpt script.  It's set to use it by default (`=1`).

4. Run the chatgpt script - no arguments currently - and that'll start the repr.


## Dependencies
* bash
* jq
* rich-cli (optional, adds syntax highlighting and other such formatting)


## Refs / more info

Model choices/explanations at:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models

More detailed usage instructions for these models in terms of crafting queries:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions

Details about additional chatgpt parameters for tuning functionality:

  https://platform.openai.com/docs/api-reference/chat/create

