from setuptools import setup, find_packages

setup(
    name='ace2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.9',
    install_requires = [
        'boto3',
        'pydantic',
        'pytest',
        'pytest-datadir',
        'pyyaml',
    ],
)
