from setuptools import setup, find_packages

setup(
    name='tg_loger',
    version='0.1.0',
    description='Telegram bot loger for django',
    author='Bahodir',
    author_email='weebcreator94@gmail.com',
    packages=find_packages(),
    install_requires=[
        'telegraph',
    ],
)
