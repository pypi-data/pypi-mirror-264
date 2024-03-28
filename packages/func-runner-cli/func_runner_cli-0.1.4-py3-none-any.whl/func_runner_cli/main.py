import os.path
from getpass import getpass

import requests
import typer
import yaml

from helpers import save_token, read_token, read_assistant_id, fetch_assistant_details, update_funcrunner_yml
from models import Project

app = typer.Typer()

API_BASE_URL = "https://api.funcrunner.com"
# API_BASE_URL = "http://localhost:8000"


@app.command()
def login():
    url = f"{API_BASE_URL}/sign_in"
    username = typer.prompt("Enter your username")
    password = getpass("Enter your password: ")

    response = requests.post(url, data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get('access_token')
        if token:
            save_token(token)
            typer.echo("Login successful. Token saved.")
        else:
            typer.echo("Failed to retrieve token.")
    else:
        typer.echo("Login failed.")


@app.command()
def init():
    project = Project()

    # Create the project configuration file
    with open('funcrunner.yml', 'w') as file:
        yaml.dump(project.dict(), file)

    # Create the project development secrets file
    with open('.env', 'w') as file:
        file.writelines(["OPENAI_API_KEY="])

    if not os.path.isdir('functions'):
        os.mkdir('functions')


@app.command()
def deploy():
    """
    Deploys the assistant using the assistant ID from funcrunner.yml.
    Updates the assistant, uploads all functions, and then deploys.
    """
    token = read_token()
    if not token:
        typer.echo("You must be logged in to perform this action.")
        return

    assistant_id = read_assistant_id()

    # Read assistant configuration from funcrunner.yml
    try:
        with open('funcrunner.yml', 'r') as file:
            assistant_config = yaml.safe_load(file).get('assistant')
    except FileNotFoundError:
        typer.echo("funcrunner.yml not found. Please ensure you are in the correct directory.")
        raise typer.Exit()
    except Exception as e:
        typer.echo(f"An error occurred while reading funcrunner.yml: {e}")
        raise typer.Exit()

    # Update Assistant via Func Runner OpenAI Proxy
    update_assistant_url = f"{API_BASE_URL}/openai/{assistant_id}"  # Adjust the endpoint as needed
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    update_response = requests.put(update_assistant_url, headers=headers, json=assistant_config)
    if update_response.status_code != 200:
        typer.echo(f"Failed to update assistant: {update_response.text}")
        return
    typer.echo("Assistant updated successfully.")

    # Upload Functions
    functions_path = 'functions'
    if not os.path.isdir(functions_path):
        typer.echo("The 'functions' directory does not exist.")
        return

    upload_url = f"{API_BASE_URL}/assistants/{assistant_id}/source_code"
    for filename in os.listdir(functions_path):
        if filename.endswith('.py'):
            function_name = filename[:-3]  # Remove '.py' extension
            with open(os.path.join(functions_path, filename), 'r') as file:
                function_code = file.read()

            payload = {
                "function_name": function_name,
                "function_code": function_code
            }

            upload_response = requests.post(upload_url, headers=headers, json=payload)
            if upload_response.status_code != 200:
                typer.echo(f"Failed to upload function '{function_name}': {upload_response.text}")
                return
            typer.echo(f"Uploaded function '{function_name}' successfully.")

    # Deploy
    deploy_url = f"{API_BASE_URL}/assistants/{assistant_id}/deployments"
    deploy_response = requests.post(deploy_url, headers=headers)
    if deploy_response.status_code == 200:
        typer.echo("Deployment successful.")
    else:
        typer.echo(f"Deployment failed: {deploy_response.text}")


@app.command()
def sync():
    """
    Syncs data from the OpenAPI JSON spec to the funcrunner.yml.

    Args:
    - openapi_path: Path to the OpenAPI JSON specification file.
    - proxy_url: URL to fetch assistant details through the OpenAI proxy.
    """
    token = read_token()  # Assuming read_token function is defined elsewhere
    assistant_id = read_assistant_id()

    # Fetching assistant details from the OpenAI proxy
    assistant_details = fetch_assistant_details(assistant_id, token, f'{API_BASE_URL}/openai')

    # Updating funcrunner.yml with the fetched assistant details
    update_funcrunner_yml(assistant_details)

    typer.echo("funcrunner.yml has been successfully updated with the latest assistant details.")


@app.command()
def chat():
    pass


if __name__ == "__main__":
    app()
