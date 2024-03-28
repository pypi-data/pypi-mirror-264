import os

import requests
import typer
import yaml

def save_token(token) -> None:
    """
    Save the token to the .funcrunner file in the home directory.
    """
    home_dir = os.path.expanduser("~")
    funcrunner_path = os.path.join(home_dir, '.funcrunner')
    with open(funcrunner_path, 'w') as token_file:
        token_file.write(token)


def read_token() -> str:
    """
    Reads the saved token from the .funcrunner file in the home directory.
    """
    try:
        home_dir = os.path.expanduser("~")
        funcrunner_path = os.path.join(home_dir, '.funcrunner')
        with open(funcrunner_path, 'r') as token_file:
            token = token_file.read().strip()
        return token
    except Exception as e:
        typer.echo(f"Failed to read the token from .funcrunner: {e}")
        raise typer.Exit()


def read_assistant_id():
    """Reads the assistant ID from the local funcrunner.yml file."""
    try:
        with open('funcrunner.yml', 'r') as file:
            config = yaml.safe_load(file)  # Correct usage of PyYAML
            assistant_id = config.get('assistant', {}).get('id')
            if not assistant_id:
                typer.echo("Assistant ID is missing in funcrunner.yml.")
                raise typer.Exit()
            return assistant_id
    except FileNotFoundError:
        typer.echo("funcrunner.yml not found. Please ensure you are in the correct directory.")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred while reading funcrunner.yml: {e}")
        raise typer.Exit()


def fetch_assistant_details(assistant_id: str, token: str, proxy_url: str) -> dict:
    """Fetches assistant details through the OpenAI proxy."""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{proxy_url}/assistants/{assistant_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        typer.echo(f"Failed to fetch assistant details: {response.text}")
        raise typer.Exit(code=1)


def update_funcrunner_yml(assistant_details: dict, funcrunner_path: str = 'funcrunner.yml'):
    """Updates the funcrunner.yml with assistant details."""
    try:
        with open(funcrunner_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        config['assistant'] = assistant_details

        with open(funcrunner_path, 'w') as file:
            yaml.dump(config, file, sort_keys=False)  # Correct usage of PyYAML
    except Exception as e:
        typer.echo(f"Failed to update funcrunner.yml: {e}")
        raise typer.Exit()
