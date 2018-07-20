from distutils.core import setup
from setuptools import find_packages

setup(name='gitlab-cli',
      version='0.0.1',
      packages=find_packages(),
      install_requires=['requests'],
      description='CLI interface for gitlab',
      author='Oskar Hladky',
      author_email='oskyks1@gmail.com',
      url='https://github.com/oskyk/gitlab-cli',
      python_requires='>=3',
      download_url='https://github.com/oskyk/gitlab-cli/archive/0.0.1.tar.gz',
      scripts=['gitlab-cli'],
      keywords=['gitlab', 'cli']
)