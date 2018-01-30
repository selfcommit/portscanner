from setuptools import setup
from datetime import datetime

version = datetime.now().strftime("%Y%m%d.%H%M%S")

setup(
    name='IPScanner',
    version=version,
    packages=[
        'IPScanner'
    ],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    package_data={
        '': ['*.json']
    },
    entry_points='''
        [console_scripts]
        ipscanner=IPScanner.scanner:start
    ''',
)
