from setuptools import setup, find_packages

setup(
    name='ace2',
    packages=find_packages('src'),
    package_dir={'', 'src'},
    python_requires='>=3.9',
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'boto3',
        'pydantic',
        'pyyaml',
    ],
)
