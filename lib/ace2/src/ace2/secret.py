from boto3.session import Session

class Secret(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        session = Session()
        client = session.client(service_name='secretsmanager', region_name=session.region_name)
        secret = client.get_secret_value(SecretId=value)
        return secret['SecretString']
