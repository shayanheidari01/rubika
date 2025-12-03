from setuptools import setup, find_packages

requirements = [
    'aiohttp',
    'pycryptodome',
    'aiofiles',
    'markdownify',
    'mutagen'
]

with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name = 'rubpy',
    version = '7.2.8',
    author='Shayan Heidari',
    author_email = 'contact@shayanheidari.info',
    description = 'Elegant, modern and asynchronous Rubika API framework in Python for users and bots',
    keywords = ['rubika', 'rubpy', 'chat', 'bot', 'robot', 'asyncio'],
    long_description = readme,
    python_requires='~=3.7',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/shayanheidari01/rubika',
    packages = find_packages(),
    exclude_package_data = {'': ['*.pyc', '*__pycache__*']},
    install_requires = requirements,
    extras_require={
        'cv': ['opencv-python'],
        'movie': ['numpy', 'moviepy', 'pillow'],
        'pil': ['pillow'],
        'rtc': ['aiortc']
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)