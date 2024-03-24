from setuptools import setup

setup(
    name='kagtool',
    version='1.2.0',
    description='Helpers For Kaggle Competition',
    author='Your Name',
    author_email='your@email.com',
    packages=['kagtool'],
    install_requires=[
        'kaggle',
        'sentencepiece',
        'transformers',
    ],
)
