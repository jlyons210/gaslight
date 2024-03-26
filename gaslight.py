#!/usr/bin/env python3

"""
Attempt to gaslight OpenAI's chat models by spoofing its output.
"""

import os
import sys
import argparse
import json
from openai import OpenAI, OpenAIError


def display_startup_banner(model: str) -> None:
    """
    Print the startup banner.

    Args:
        model: The OpenAI model to use.
    """

    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    print(
        (
            "\n"
            "  ░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ \n"
            " ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            " ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            " ░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░  ░▒▓█▓▒░     \n"
            " ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            " ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            "  ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n" 
            "\n"
            " Attempt to gaslight OpenAI's chat models by spoofing its output.\n"
            " Press Ctrl+C to exit, or Ctrl+D to print the message list.\n"
            f" Using model: {model}\n"
        )
    )


def generate_chat_response(
        message_list:   dict[str, str],
        apikey:         str,
        model:          str,
    ) -> str:
    """
    Generate a response from the OpenAI chat model.

    Args:
        message_list: The message list to send to the chat model.
        apikey: The OpenAI API key.
        model: The OpenAI model to use.

    Returns:
        The response from the OpenAI chat model.
    """

    try:
        client = OpenAI(
            api_key=apikey,
            # timeout=10,
            # max_retries=3,
        )

        response = client.chat.completions.create(
            messages=message_list,
            model=model,
            max_tokens=1024,
            temperature=0.8,
        )

        response_content = response.choices[0].message.content
        print(response_content)
        return response_content

    except OpenAIError as e:
        print(f'Error: {e}', file=sys.stderr)
        print(f'message_list:\n{json.dumps(message_list, indent=2)}', file=sys.stderr)
        sys.exit(1)


def get_assistant_response(message_list, args) -> str:
    """
    Prompt the user for the assistant's response.
    """

    prompt = input('Assistant (blank to poll API): ')

    if prompt == '':
        prompt = generate_chat_response(message_list, args.apikey, args.model)

    return {
        'role': 'assistant',
        'content': prompt,
    }


def gaslight(args) -> None:
    """
    Gaslight OpenAI's chat models by spoofing its output.
    """

    try:
        message_list = []
        message_list.append(set_prompt('system'))
        print('-' * 100)

        while True:
            message_list.append(set_prompt('user'))
            print()
            message_list.append(get_assistant_response(message_list, args))
            print()

    except EOFError:
        print(f'message_list:\n{json.dumps(message_list, indent=2)}', file=sys.stderr)
        sys.exit(2)

    except KeyboardInterrupt:
        print('\nGoodbye.', file=sys.stderr)
        sys.exit(0)


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--apikey', '-a',
        help='OpenAI API key',
        required=True,
    )
    parser.add_argument(
        '--model', '-m',
        default='gpt-3.5-turbo',
        help='OpenAI model to use',
    )

    return parser.parse_args()


def set_prompt(prompt_type: str) -> str:
    """
    Set an incoming prompt.

    Args:
        prompt_type: The type of prompt to set.

    Returns:
        The incoming prompt.
    """

    prompt = input(f'{prompt_type.capitalize()} prompt: ')

    return {
        'role': prompt_type,
        'content': prompt,
    }


def main() -> None:
    """
    Main entry point.
    """

    args = parse_args()

    display_startup_banner(args.model)
    gaslight(args)


if __name__ == '__main__':
    main()
