import tempfile
import os
import json
import hashlib
from subprocess import call
from secret_manager_cli.session import get_session
from rich import print


def get_secret_name(profile: str) -> list:
    """Retrieve cluster arn

    Args:
        profile (str): aws profile

    Returns:
        list: List of cluster(s) arn
    """

    list_secret_name = list()

    secret_name_response = get_session(
        profile=profile, resource="secretsmanager", action="list_secret_name"
    )
    for secret_name in secret_name_response["SecretList"]:
        list_secret_name.append(secret_name["Name"])
    
    return list_secret_name


def get_secret_value(profile: str, secret_name: str) -> str:
    """Retrieve secret value for editing

    Args:
        profile (str): aws profile
        secret_name (str): secret name

    Returns:
        str: Value of the secret
    """
    client = get_session(
        profile=profile,
        resource="secretsmanager",
    )
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        print(
            f"ERROR: The secret: {secret_name} doesn't exist within your profile: {profile}"
        )
        print(
            "HINT: Double check your credentials according the secret you want to update."
        )
        exit(-1)

    return response["SecretString"]


def edit_secret_value(secret_value: dict, type: str) -> str:
    """Edit the secret value

    Args:
        secret_value (str): secret string to update

    Returns:
        str: Value of the secret
    """
    try:
        # Get the text editor from the shell, otherwise default to Vim
        EDITOR = os.environ.get("EDITOR", "vim")

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".tmp", delete=True) as tf:
            
            if type == "json":
                json.dump(secret_value, tf, sort_keys=True, indent=4)
            elif type == "string":
                tf.write(secret_value)
                
            # Flush the I/O buffer to make sure the data is written to the file
            tf.flush()

            original_file_md5 = md5(tf.name)
            # Open the file with the text editor
            call([EDITOR, tf.name])

            # Reopen the file to read the edited data
            with open(tf.name, "r") as tf:

                # Read the file data into a variable
                edited_message = tf.read()

                # Return the data
                final_file_md5 = md5(tf.name)

                return original_file_md5, final_file_md5, edited_message

    except Exception as Err:
        print(f"ERROR: {Err}")
        exit(-1)


def update_secret_string(profile: str, secret_name: str, secret_string: str) -> str:
    """Update secret string for the secret name

    Args:
        profile (str): aws profile
        secret_name (str): secret name
        secret_string (str): secret string to update

    Returns:
        str: Value of the secret
    """
    client = get_session(
        profile=profile,
        resource="secretsmanager",
    )

    response = client.update_secret(SecretId=secret_name, SecretString=secret_string)
    return response


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True