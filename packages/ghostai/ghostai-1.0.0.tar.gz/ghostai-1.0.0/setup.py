from setuptools import setup, find_packages

setup(
    name='ghostai',
    version='1.0.0',
    description='A Python library for interacting with the GhostAI API',
    url='https://github.com/The-UnknownHacker/ghostaiapi',
    author='CyberZenDev',
    author_email='cyberzendev@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0'
    ],
    python_requires='>=3.6',
)
