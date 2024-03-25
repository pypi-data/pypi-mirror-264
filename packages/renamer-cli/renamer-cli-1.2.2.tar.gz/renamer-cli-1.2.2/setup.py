from setuptools import setup

setup(
    name='renamer-cli',
    version='1.2.2',
    py_modules=['renamer'],
    author='READMEmaybe',
    author_email='READMEmaybe@protonmail.com',
    description='A command-line tool for fast and flexible file and directory renaming.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/READMEmaybe/renamer-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'renamer = renamer:main',
        ],
    },
)
