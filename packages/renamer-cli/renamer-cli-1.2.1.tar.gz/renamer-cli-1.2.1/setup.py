from setuptools import setup

setup(
    name='renamer-cli',
    version='1.2.1',
    py_modules=['renamer'],
    author='READMEmaybe',
    author_email='READMEmaybe@protonmail.com',
    description='A command-line tool for fast and flexible file and directory renaming.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/READMEmaybe/renamer',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'renamer = renamer:main',
        ],
    },
)
