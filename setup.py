from setuptools import setup, find_packages

requirements = [
    'wheel',
    'pycryptodome',
    'websockets',
    'pybase64',
    'aiohttp',
    'mutagen',
    'TinyTag',
]

with open("README.md", encoding="UTF-8") as f:
    readme = f.read()

setup(
    name = 'rubpy',
    version = '5.1.1',
    author='Shayan Heidari',
    author_email = 'snipe4kill@yahoo.com',
    description = 'This is an unofficial library and fastest library for deploying robots on Rubika accounts.',
    keywords = ['rubika', 'rubpy', 'rubikaio', 'chat', 'bot', 'robot', 'asyncio'],
    long_description = readme,
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/shayanheidari01/rubika',
    packages = find_packages(),
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)