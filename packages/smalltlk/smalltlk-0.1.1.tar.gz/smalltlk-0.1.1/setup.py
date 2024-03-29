from setuptools import setup, find_packages

setup(
    name='smalltlk',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'nltk',
        #'transformers',
        #'scikit-learn',
    ],
    entry_points={
        "console_scripts":[
            "smalltlk-hello = smalltlk_hello:hello",
        ],
    },
)