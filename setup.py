from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='tg_api_autoreg',
      version='0.1.2',
      description='Library for automatic registration telegram User Api (beta)',
      install_requires=['requests'],
      author='Alexandr Macheck',
      url="https://github.com/youbrain/tg_user_api_autoreg",
      packages=find_packages(),
      author_email='647533sancho@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
