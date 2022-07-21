from boto3.session import Session

def get_secret(secret_id: str) -> str:
    ''' gets a secret string from Secrets Manager

    Args:
        secret_id: the id of the secret string to get the value of

    Returns:
        the value of the secret
    '''

    # get the secret
    session = Session()
    client = session.client(service_name='secretsmanager', region_name=session.region_name)
    return client.get_secret_value(SecretId=secret_id)['SecretString']
