from setuptools import setup

setup(
    name='gptcli',
    version='0.0.1',
    py_modules=['gptcli'],
    install_requires=[
        'Click',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'gpt = gptcli:cli',
        ],
    },
)