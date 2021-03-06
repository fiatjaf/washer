from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='washer',
    version='0.7',
    py_modules=['washer'],
    install_requires=[
        'Click',
        'whoosh',
        'blessings'
    ],
    entry_points='''
        [console_scripts]
        washer=washer:main
    ''',
    description='A whoosh-based CLI indexer and searcher for your files.',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/fiatjaf/washer',
    long_description=long_description
)
