from boto3.session import Session

class Secret(str):
    ''' special model for translating a aws secrets manager id into the secret value '''

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value:str) -> str:
        ''' translates the secret id into a secret value

        Args:
            value: the secret id to translate

        Returns:
            the secret value string
        '''

        session = Session()
        client = session.client(service_name='secretsmanager', region_name=session.region_name)
        return client.get_secret_value(SecretId=value)['SecretString']
