from ace2.service import Service
from pydantic import Field

def test_service():
    class MyService(Service):
        class Config(Service.Config):
            address: str = Field(default='127.0.0.3', description='pretend address for some fake service')

    service = MyService()
    assert service.config.address == '127.0.0.1'

    service = MyService('secondary')
    assert service.config.address == '127.0.0.2'

    service = MyService('tertiary')
    assert service.config.address == '127.0.0.3'
