from setuptools import setup, find_packages

# Read the contents of your README.md file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ghostai',
    version='1.1.0',
    description='A Python library for interacting with the GhostAI API',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This indicates markdown content
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
