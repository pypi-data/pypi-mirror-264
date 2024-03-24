import json
import os
import sys
import subprocess
import time
import typer

from echoprompt import EchoPrompt
from secret_manager_cli import __app_name__, __version__
from secret_manager_cli.menu import make_choice
from secret_manager_cli.helpers import get_secret_value
from secret_manager_cli.helpers import edit_secret_value
from secret_manager_cli.helpers import update_secret_string
from secret_manager_cli.helpers import is_json

from deepdiff import DeepDiff
from rich import print
from typing import Optional
from typing_extensions import Annotated


app = typer.Typer()
prompt = EchoPrompt("secret-manager")


@app.command()
def list_secret():
    """List secret(s) from AWS Secret Manager"""

    try:
        credentials_type = prompt.prompt_choice(
            "credentials_type",
            choices=("EC2_INSTANCE_METADATA", "AWS_CREDENTIALS_FILE"),
        )
        if credentials_type:
            profile_name = credentials_type
            if credentials_type == "AWS_CREDENTIALS_FILE":
                profile_name = prompt.prompt_choice(
                    "profile_name", choices=make_choice(choice="profile_name")
                )

            else:
                region = prompt.prompt_choice(
                    "region", choices=make_choice(choice="region")
                )
                if region:
                    os.environ["AWS_DEFAULT_REGION"] = region

        secret_name = prompt.prompt_choice(
            "secret_name",
            choices=make_choice(choice="secret_name", profile=profile_name),
        )

    except (KeyboardInterrupt, TypeError) as e:
        print("Bye bye !")
        sys.exit()

    return secret_name


@app.command("update-secret")
def update_secret(secret_name: Annotated[Optional[str], typer.Argument()] = None):
    """Update secret from secret manager"""
    try:
        credentials_type = prompt.prompt_choice(
            "credentials_type",
            choices=("EC2_INSTANCE_METADATA", "AWS_CREDENTIALS_FILE"),
        )
        if credentials_type:
            profile_name = credentials_type
            if credentials_type == "AWS_CREDENTIALS_FILE":
                profile_name = prompt.prompt_choice(
                    "profile_name", choices=make_choice(choice="profile_name")
                )

            else:
                region = prompt.prompt_choice(
                    "region", choices=make_choice(choice="region")
                )
                if region:
                    os.environ["AWS_DEFAULT_REGION"] = region

        # Check if a secret name has been passed as argument
        if secret_name is None:
            secret_name = prompt.prompt_choice(
                "secret_name",
                choices=make_choice(choice="secret_name", profile=profile_name),
            )

        # Retrieve secret string value
        initial_secret_value = get_secret_value(
            profile=profile_name, secret_name=secret_name
        )

        # Edit the secret value as a temporary file
        if is_json(initial_secret_value):
            try:
                original_file_md5, final_file_md5, updated_secret_string = (
                    edit_secret_value(secret_value=json.loads(initial_secret_value),type="json")
                )
            except Exception as Err:
                print(f"ERROR: {Err}")
                exit(-1)
        else:
            try:
                original_file_md5, final_file_md5, updated_secret_string = (
                    edit_secret_value(initial_secret_value, type="string")
                )
            except Exception as Err:
                print(f"ERROR: {Err}")
                exit(-1)

        # Check if the file has been modified.
        if original_file_md5 != final_file_md5:
            diff = DeepDiff(initial_secret_value, updated_secret_string)
            print(diff)
            confirmation_choice = prompt.prompt_choice(
                "Confirm the update ?",
                choices=("YES", "NO"),
            )

            if confirmation_choice == "YES":
                response = update_secret_string(
                    profile=profile_name,
                    secret_name=secret_name,
                    secret_string=updated_secret_string,
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    print(f"The secret {secret_name} has been successfully updated.")
                else:
                    print("Secret update canceled !")
        else:
            print(f"The secret {secret_name} has not been updated.")

    except (KeyboardInterrupt, TypeError) as e:
        try:
            time.sleep(2)
        except (KeyboardInterrupt, TypeError) as e:
            print("Bye bye !")
            sys.exit()
        else:
            pass


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
