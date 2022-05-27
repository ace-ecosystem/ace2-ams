from setuptools import setup, find_packages

setup(
    name='ace2',
    packages=['ace2'],
    python_requires='>=3.9',
    install_requires = [
        'boto3',
        'pydantic',
        'pyyaml',
    ],
)
