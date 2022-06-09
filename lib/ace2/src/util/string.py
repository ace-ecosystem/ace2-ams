import re

camel = re.compile(r'([^A-Z])([A-Z])')

def camel_to_snake(value:str) -> str:
    return camel.sub(r'\1_\2', value).lower()
