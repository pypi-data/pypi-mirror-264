from setuptools import setup, find_packages

setup(
    name='ikctl',
    version='1.2.0',
    description="App to installer packages on remote servers",
    author="David Moya López",
    author_email="3nueves@gmail.com",
    license="Apache v2.0",
    packages=find_packages(include=['ikctl','ikctl.*']),
    install_requires=[
        'paramiko',
        'pyaml',
        'envyaml'
    ],
    entry_points={
        'console_scripts': [
            # 'ikctl=ikctl.main:create_parser'
            'ikctl=main:create_parser'
        ]
    }
)
