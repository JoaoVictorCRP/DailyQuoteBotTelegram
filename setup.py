from distutils.core import setup
from setuptools import find_packages

setup(
    name='QuoachBotTelegram',
    version='1.0.0',
    packages=find_packages(),
    author='JoaoVictorCRP',
    description='A motivational quote bot for telegram',
    install_requires=[
        'python-telegram-bot[ext]',
        'requests'
    ],
)

# "pip install ." -> Install dependencies