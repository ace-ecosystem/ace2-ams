import io
import os
from setuptools import setup, find_packages
from setuptools.command.install import install

def read(file_name):
    with io.open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8') as f:
        return f.read()

def readlines(file_name):
    path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.isfile(path):
        with io.open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8') as f:
            return f.readlines()
    else:
        return []

install_requires = readlines('src/ace2/core/requires.txt')
install_requires.extend(readlines('src/ace2/mods/requires.txt'))

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
