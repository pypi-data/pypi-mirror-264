from setuptools import setup


setup(
    # other setup options...
    entry_points={
        'console_scripts': [
            'noscop3r = nosc0pe.noscop3r:main',
        ],
    },
)