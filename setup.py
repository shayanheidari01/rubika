from setuptools import setup, find_packages


requirements = ['wheel', 'pycryptodome', 'websockets', 'ujson', 'pybase64', 'urllib3', 'mutagen', 'TinyTag', 'httpx']

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name = 'rubpy',
    version = '4.6.9',
    author='Shayan Heidari',
    author_email = 'snipe4kill@yahoo.com',
    description = 'This is an unofficial library and fastest library for deploying robots on Rubika accounts.',
    keywords = ['rubika', 'rubpy', 'rubikaio', 'chat', 'bot', 'robot', 'asyncio'],
    long_description = readme,
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/snipe4kill/rubika/',
    packages = find_packages(),
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)