from setuptools import setup, find_packages

setup(
    name='pingdomv3',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hello = pingdomv3.hello:say_hello'
        ]
    }
)

