"""Top-level package for askchat."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '1.1.2'

import asyncio
from pathlib import Path
import click

# Main environment file
CONFIG_PATH = Path.home() / ".askchat"
CONFIG_FILE = CONFIG_PATH / ".env"
MAIN_ENV_PATH = Path.home() / '.askchat' / '.env'
ENV_PATH = Path.home() / '.askchat' / 'envs'

# Autocompletion
# environment name completion
class EnvNameCompletionType(click.ParamType):
    name = "envname"
    def shell_complete(self, ctx, param, incomplete):
        return [
            click.shell_completion.CompletionItem(path.stem) for path in ENV_PATH.glob(f"{incomplete}*.env")
        ]
# chat file completion
class ChatFileCompletionType(click.ParamType):
    name = "chatfile"
    def shell_complete(self, ctx, param, incomplete):
        return [
            click.shell_completion.CompletionItem(path.stem) for path in CONFIG_PATH.glob(f"{incomplete}*.json")
            if not path.name.startswith("_")
        ]

# common functions
async def show_resp(chat, **options):
    msg = ''
    async for char in chat.async_stream_responses(textonly=True, **options):
        print(char, end='', flush=True)
        msg += char
        await asyncio.sleep(0.01)
    if not msg.endswith('\n'):
        print() # add a newline if the message doesn't end with one
    return msg

def write_config(config_file, api_key, model, base_url, api_base):
    """Write the environment variables to a config file."""
    def write_var(f, var, value, desc):
        value = value if value else ""
        f.write(f"\n\n# {desc}\n")
        f.write(f'{var}="{value}"')
    with open(config_file, "w") as f:
        f.write("#Description: Env file for askchat.\n" +\
                "#Current version: " + __version__)
        # write the environment table
        write_var(f, "OPENAI_API_BASE", api_base, "The base url of the API (with suffix /v1)" +\
                    "\n# This will override OPENAI_API_BASE_URL if both are set.")
        write_var(f, "OPENAI_API_BASE_URL", base_url, "The base url of the API (without suffix /v1)")

        write_var(f, "OPENAI_API_KEY", api_key, "Your API key")
        write_var(f, "OPENAI_API_MODEL", model, "The model name\n" +\
                    "# You can use `askchat --all-valid-models` to see supported models")