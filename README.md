# PyGPT - A lightweight, python-based, open-source, OpenAPI GPT client.

Compared to the ChatGPT website this is more configurable, is only a few
hundred lines of open-source code so is easy to understand/follow/modify,
allows GPT-4 and plug-in options like inserting weblinks without paying the
hefty monthly fee for ChatGPT-Plus.  (However, note it does involve paying fees
for API calls - but for personal use rather than public internet app use, this
is literally pennies per month.)

------
![screenshot](screenshot.png "Screenshot")
------


## Usage

1. Get an [API key](https://platform.openai.com/account/api-keys) (requires
creating an OpenAI account if you don't have one already) and put that key in
your shell environment, e.g. `export OPENAI_API_KEY=xyz123...`

2. Install dependencies and run the app:

Can be run either as a terminal/readline based ChatGPT CLI app or as a
browser-based web-app:

```bash
Usage:  python3 pygpt.py           # for CLI
   or:  python3 pygpt.py --gradio  # for web-app
```

Note that any client outside of the one on OpenAI's website (which is free
for ChatGPT) requires an [API key](https://platform.openai.com/account/api-keys)
to access the API, and making calls to this API does 
[cost money](https://openai.com/pricing#language-models).
However, it's super cheap if just using it oneself for reference queries (e.g.
I generally just use it as a stand-in for Google/Wikipedia/StackOverflow),
as opposed to serving it out to zillions of other users to use in a web app.
Like in my initial two days of fairly heavy usage I racked up a whole $0.20;
after a few months of light-moderate usage since then, I'm now up to $0.50.

You must run this in an environment with the following python packages:
  * openai (for the core Open API calls)
  * beautifulsoup4 (for reading contents of urls)
  * rich (for the markdown/syntax-highlighting formatting in CLI)
  * darkdetect (for putting code syntax or webpage into light/dark mode in CLI)
  * gradio (for the quickie webapp interface)

```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install openai rich darkdetect beautifulsoup4 gradio
  export OPENAI_API_KEY=xyz123xyz123...
  python pygpt.py
```

The command line (CLI) client uses readline, so all the usual hot keys /
editing work including a command history via Ctrl-P and Ctrl-N.  Quit via:
`quit` or `exit` or `q` or `ctrl-D` or `ctrl-C`.

The web-app is a quickie implemention via Gradio - after starting the app
it'll output the local URL to paste into your web browser to access the app.

Lastly know that OpenAI's GPT API is an immensely popular service right now and
that regardless of which client you use (one of these, or the ChatGPT website
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

  Arbitrary example table below comes from a forum entry at:
  https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api-a-few-tips-and-tricks-on-controlling-the-creativity-deterministic-output-of-prompt-responses/172683

  Use Case                 Temp  Top_p  Description
  ------------------------ ----  -----  ------------------------------------
  Code Generation           0.2  0.1    Generates code that adheres to established patterns and conventions. Output is more deterministic and focused. Useful for generating syntactically correct code.
  Creative Writing          0.7  0.8    Generates creative and diverse text for storytelling. Output is more exploratory and less constrained by patterns.
  Chatbot Responses         0.5  0.5    Generates conversational responses that balance coherence and diversity. Output is more natural and engaging.
  Code Comment Generation   0.3  0.2    Generates code comments that are more likely to be concise and relevant. Output is more deterministic and adheres to conventions.
  Data Analysis Scripting   0.2  0.1    Generates data analysis scripts that are more likely to be correct and efficient. Output is more deterministic and focused.
  Exploratory Code Writing  0.6  0.7    Generates code that explores alternative solutions and creative approaches. Output is less constrained by established patterns.


