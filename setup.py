from setuptools import setup, find_packages

with open("README.md", "r") as fd:
    long_description = fd.read()
    

requirements = [
    'requests',
    'click'
]

name = 'weather_cli'

setup(
    name = name,
    version = '1.0.0',
    packages = ['weather_cli'],
    description = 'python version implementation of `wego` which is a weather forecast client for the terminal.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = 'Faris Shi',
    author_email = 'faris.shi84@gmail.com',
    url = 'https://github.com/faris-shi/py_weather_cli',
    license = 'MIT',
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts':[
            'weather_cli=weather_cli.main:cli' 
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Utilities',

        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords = 'wego-python weather english cli forecast ascii-art'
)