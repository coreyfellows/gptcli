Acts as a command line version of the ChatGPT converstaion app.

State is stored in `~/.chatgpt`

You need an api key, so you pay as you go

```
pip install git+https://github.com/coreyfellows/gptcli.git
gpt --help
```

Basic Usage:

Calling `gpt` followed by a prompt will output the response to that prompt. Subsequent calls to `gpt` will continue the conversation.

If you want to start a new conversation use the `gpt -n` flag.

If you want to see the whole converstion, use `gpt -r`.

To see a list of all conversations, `gpt --list`

To swap between conversations `gpt -s <integer>` where the integer is the conversation you want to go back to

`gpt -i` will open an interactive shell to allow immediate follow ups. `q` or keyboard interrupt to quit.





