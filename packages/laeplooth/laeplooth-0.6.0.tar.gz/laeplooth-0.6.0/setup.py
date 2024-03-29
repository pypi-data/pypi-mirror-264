from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='laeplooth',
    packages=find_packages(include=['laeplooth']),
    version='0.6.0',
    description='Translator for loo language',
    author='most.warong',
    install_requires=[
       'pythainlp==2.1.4'
    ],
    entry_points={
        'console_scripts': [
            'laeplooth = laeplooth:loo'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
