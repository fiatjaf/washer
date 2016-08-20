from setuptools import setup

setup(
    name='washer',
    version='0.2',
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
)
