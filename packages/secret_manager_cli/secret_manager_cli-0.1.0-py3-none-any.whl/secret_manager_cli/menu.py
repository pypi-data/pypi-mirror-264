from secret_manager_cli.credentials import check_credentials
from secret_manager_cli.credentials import which_credentials
from secret_manager_cli.credentials import which_region
from secret_manager_cli.helpers import get_secret_name


def make_choice(
    choice: str = None,
    profile: str = None,
    cluster_name: str = None,
    service_name: str = None,
    task_name: str = None,
) -> str:
    """Generic function to make choice in a list displayed

    Args:
        profile (str, optional): aws profile. Defaults to None.
        cluster_name (str, optional): name of the cluster to retrieve service. Defaults to None.
        service_name (str, optional): name of the service to retrieve task. Defaults to None.
        task_name (str, optional): name of the task to retrieve the container name. Defaults to None.

    Returns:
        str: String of the choice in the menu
    """

    list_results = ""

    # choose_secret
    if choice == "secret_name":
        list_results = get_secret_name(profile)

    # choose_credentials_profile
    elif choice == "profile_name":
        list_results = check_credentials()

    # choose which type of credentials to use
    elif choice == "credentials_type":
        list_results = which_credentials()

    # choose which region to use
    elif choice == "region":
        list_results = which_region()


    return list_results
