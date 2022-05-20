import os
from setuptools import setup, find_packages
from setuptools.command.install import install

# locate project directory both inside and outside of tox
project_dir = os.path.dirname(os.environ['TOX_WORK_DIR']) if 'TOX_WORK_DIR' in os.environ else os.path.dirname(__file__)

def read(file_name):
    with open(os.path.join(project_dir, file_name)) as f:
        return f.read()

# read install requirements from both core and mods if there are any
install_requires = read('src/ace2/core/requires.txt').splitlines()
try:
    install_requires.extend(read('src/ace2/mods/requires.txt').splitlines())
except FileNotFoundError:
    pass

class Install(install):
    def run(self):
        # TODO: install other stuff like apt packages
        install.run(self)

setup(
    name='ace2',
    version='1.0',
    license='Apache 2.0',
    description='Library for creating ACE2 analysis modules',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Cole Robinette',
    author_email='robinette.31@gmail.com',
    url='https://github.info53.com/Fifth-Third/ice2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires = install_requires,
    cmdclass = {
        'install': Install,
    }
)
