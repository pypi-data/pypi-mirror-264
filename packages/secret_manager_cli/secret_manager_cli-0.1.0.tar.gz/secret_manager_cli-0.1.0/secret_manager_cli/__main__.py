from secret_manager_cli import cli, __app_name__


def main():
    print("\n")
    print("Welcome in secret manager Cli !\n")
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
