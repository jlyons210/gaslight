#!/usr/bin/env python3

"""
Attempt to gaslight OpenAI's chat models by spoofing its output.
"""

import sys
import argparse
from openai import OpenAI, OpenAIError


def generate_response(message_list, apikey, model) -> str:
    """
    Generate a response from the OpenAI chat model.
    """

    try:
        client = OpenAI(
            api_key=apikey,
            timeout=10,
            max_retries=3,
        )

        response = client.chat.completions.create(
            messages=message_list,
            model=model,
            max_tokens=1024,
            temperature=0.8,
        )

        prompt = response.choices[0].message.content
        print(prompt)

    except OpenAIError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    return {
        'role': 'assistant',
        'content': prompt,
    }


def input_assistant_response() -> str:
    """
    Prompt the user for the assistant's response.
    """

    prompt = input('Assistant (blank to poll API): ')

    if prompt == '':
        return ''

    else:
        return {
            'role': 'assistant',
            'content': prompt,
        }


def input_system_prompt() -> str:
    """
    Prompt the user for the system prompt.
    """

    prompt = input('System prompt: ')

    return {
        'role': 'system',
        'content': prompt,
    }


def input_user_prompt() -> str:
    """
    Prompt the user for the user's prompt.
    """

    prompt = input('User: ')

    return {
        'role': 'user',
        'content': prompt,
    }


def gaslight(args) -> None:
    """
    Gaslight OpenAI's chat models by spoofing its output.
    """

    try:
        message_list = []
        message_list.append(input_system_prompt())
        print('-' * 80)

        while True:
            message_list.append(input_user_prompt())
            print('\n')

            assistant_response = input_assistant_response()
            if assistant_response == '':
                assistant_response = generate_response(message_list, args.apikey, args.model)
            message_list.append(assistant_response)
            print('\n')

    except EOFError:
        print(f'message_list:\n{message_list}', file=sys.stderr)

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


def print_banner() -> None:
    """
    Print the program banner.
    """

    print(
        (
            "\n"
            " ░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ \n"
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            "░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            "░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░  ░▒▓█▓▒░     \n"
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n"
            " ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     \n" 
            "\n"
            "Attempt to gaslight OpenAI's chat models by spoofing its output.\n"
            "Press Ctrl+C to exit, or Ctrl+D to print the message list.\n"
        )
    )

def main() -> None:
    """
    Main entry point.
    """

    args = parse_args()

    print_banner()
    gaslight(args)


if __name__ == '__main__':
    main()
