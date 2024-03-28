from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.1'
DESCRIPTION = "This module is helful for removing daily use chatting and business words from any string."

# Setting up
setup(
    name="internet_words_remover",
    version=VERSION,
    author="Qadeer Ahmad",
    author_email="<mrqadeer1231122@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts":[
            'words_remover=internet_words_remover:words_remover'
        ]
    },
    keywords=['python', 'internet words', 'chatting words', 'words remover','nlp','textual data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    
)