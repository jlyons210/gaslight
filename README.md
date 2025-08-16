# GASLIGHT
**gaslight.py** is a quickly thrown together proof-of-concept to see how various OpenAI chat models react to spoofed `assistant` prompts. It can also be used as a basic chat interface, if no spoofing is used. It can yield entertaining results - YMMV. It runs interactively; just provide a valid OpenAI API key, and optionally, specify a chat model other than the default `gpt-3.5-turbo`.

## Preparing your environment
```sh
python3 -m venv .venv
pip install -r requirements.txt
```

## Usage
```sh
source .venv/bin/activate
./gaslight.py -a [openai_api_key] -m [chat_model]
```
## Demo
![screenshot](gaslight_demo.png)
