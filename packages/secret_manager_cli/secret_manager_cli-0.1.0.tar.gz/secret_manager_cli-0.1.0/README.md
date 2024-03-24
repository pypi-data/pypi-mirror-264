# secret_manager_cli

AWS aws-secret-manager-cli tool is aimed to :

- list all the secrets under your AWS account
- edit your secret directly from you terminal editor

&nbsp;

Examples: 

```bash
❯ python -m secret_manager_cli update-secret your-secret-name
❯ python -m secret_manager_cli update-secret
❯ python -m secret_manager_cli list-secret
```

&nbsp;

## Installation

**Requirements**


- Install awscli via [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html] (not necessary if you are connected to an EC2 instance)


&nbsp;

You should install the requirements via the pip install below.

&nbsp;

Create a virtualenv with python >= 3.9

&nbsp;

```bash
source .venv_3.11.0/bin/activate
pip install secret_manager_cli
```

&nbsp;

if it is the first time you connect to aws-cli, you have to get credentials key from your aws administrator.

&nbsp;

## Usage

```bash
❯ python -m secret_manager_cli --help


Welcome in secret manager Cli !

                                                                                                                                                      
 Usage: secret_manager_cli [OPTIONS] COMMAND [ARGS]...                                                                                                
                                                                                                                                                      
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show the application's version and exit.                                                                           │
│ --install-completion            Install completion for the current shell.                                                                          │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                   │
│ --help                          Show this message and exit.                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list-secret                             List secret(s) from AWS Secret Manager                                                                     │
│ update-secret                           Update secret from secret manager                                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

&nbsp;

Thanks to Typer from [@tiangolo](https://typer.tiangolo.com/)
