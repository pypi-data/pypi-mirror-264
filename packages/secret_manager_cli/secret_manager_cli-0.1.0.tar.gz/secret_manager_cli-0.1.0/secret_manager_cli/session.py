import boto3


def get_session(
    profile: str = None,
    resource: str = None,
    cluster_name: str = None,
    service_name: str = None,
    task_name: str = None,
    task_definition_arn: str = None,
    action: str = None,
) -> list:
    """Generic function to call boto3 function to retrieve data from AWS

    Args:
        profile (str, optional): aws profile. Defaults to None.
        cluster_name (str, optional): name of the cluster to retrieve service. Defaults to None.
        service_name (str, optional): name of the service to retrieve task. Defaults to None.
        task_name (str, optional): name of the task to retrieve the container name. Defaults to None.
        task_definition_arn (str, optional): task definition arn to retrieve log group. Defaults to None.
        action (str, optional): boto3 action to call. Defaults to None.

    Returns:
        list: JSON response from boto3 call
    """
    try:
        if profile == "EC2_INSTANCE_METADATA":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=profile)
        
        client = session.client(resource)

        if resource == "secretsmanager":
            if action == "list_secret_name":
                response = client.list_secrets(
                    MaxResults=100,
                    SortOrder='asc'
                )
            else:
                return client
        
    except Exception as Err:
        print(f"ERROR: {Err}")
        exit(-1)

    return response
