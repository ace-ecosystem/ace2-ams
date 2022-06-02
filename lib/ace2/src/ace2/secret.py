import boto3

class SecretString(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=session.region_name)
        secret = client.get_secret_value(SecretId=value)
        return secret['SecretString']
