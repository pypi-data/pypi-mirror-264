#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [
    'pip==19.2.3',
    'bump2version==0.5.11',
    'wheel==0.33.6',
    'watchdog==0.9.0',
    'flake8==3.7.8',
    'tox==3.14.0',
    'coverage==4.5.4',
    'Sphinx==1.8.5',
    'twine==1.14.0',
    'Click==7.1.2',
    'annotated-types==0.6.0',
    'anyio==3.7.1',
    'arrow==1.3.0',
    'async-generator==1.10',
    'babel==2.14.0',
    'binaryornot==0.4.4',
    'cashews==7.0.0',
    'certifi==2024.2.2',
    'chardet==5.2.0',
    'charset-normalizer==3.3.2',
    'click==8.1.7',
    'cookiecutter==2.5.0',
    'distlib==0.3.8',
    'distro==1.7.0',
    'exceptiongroup==1.2.0',
    'filelock==3.13.1',
    'grpcio==1.60.0',
    'h11==0.14.0',
    'httpcore==1.0.4',
    'httpx==0.26.0',
    'idna==3.6',
    'Jinja2==3.1.3',
    'markdown-it-py==3.0.0',
    'MarkupSafe==2.1.5',
    'mdurl==0.1.2',
    'noneprompt==0.1.9',
    'platformdirs==4.2.0',
    'podman-compose==1.0.6',
    'prompt-toolkit==3.0.43',
    'protobuf==4.25.3',
    'pydantic==2.6.2',
    'pydantic_core==2.16.3',
    'pyfiglet==1.0.2',
    'Pygments==2.17.2',
    'python-dateutil==2.8.2',
    'python-dotenv==1.0.1',
    'python-slugify==8.0.4',
    'PyYAML==6.0.1',
    'requests==2.31.0',
    'rich==13.7.0',
    'six==1.16.0',
    'sniffio==1.3.0',
    'text-unidecode==1.3',
    'tomlkit==0.12.3',
    'types-python-dateutil==2.8.19.20240106',
    'typing_extensions==4.9.0',
    'urllib3==2.2.1',
    'virtualenv==20.25.0',
    'watchfiles==0.21.0',
    'wcwidth==0.2.13'
]

setup(
    author="buaatjr",
    author_email='tjr20202021@163.com',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    description="a cli tool for detensor",
    entry_points={
        'console_scripts': [
            'detensor = detensor_cli.__main__:main',
        ],
    },
    install_requires=test_requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='detensor_cli',
    name='detensor_cli',
    packages=find_packages(include=['detensor_cli','detensor_cli.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tjr20202021@163.com/detensor_cli',
    version='0.1.7',
    zip_safe=False,
)
