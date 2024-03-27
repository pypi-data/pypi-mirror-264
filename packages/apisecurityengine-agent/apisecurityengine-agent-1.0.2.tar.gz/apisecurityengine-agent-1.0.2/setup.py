from setuptools import setup, find_packages

setup(
    name='apisecurityengine-agent',
    version='1.0.2',
    author='CyberUltron',
    description='An agent that captures the API traffic coming to the host application and sends it to apisecurityengine service for checking security vulnerabilities.',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
)
