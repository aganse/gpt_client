# openai_llm_tools
Bash CLI tools to access the OpenAI LLM APIs, starting with a chat client.


`chatgpt`: Basic command-line ChatGPT-API repr in Bash, implementing shell
tools like readline, syntax highlighting, prompt formatting, etc.  No command
line arguments; currently the few options are at the top of the bash script
(I'll move them to command line args soon).  So for now simply run the
./chatgpt script and then you're in the repr.  Auto-wraps to the width of the
current terminal window.
![screenshot](screenshot.png "Screenshot")


## Dependencies:
* bash
* jq
* rich-cli (optional, adds syntax highlighting and other such formatting)


## Refs / more info:

Model choices/explanations at:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/models

More detailed usage instructions for these models in terms of crafting queries:

  https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions

Details about additional chatgpt parameters for tuning functionality:

  https://platform.openai.com/docs/api-reference/chat/create

