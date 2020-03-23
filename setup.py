import re
import io
from setuptools import setup, find_packages
import codecs
from os import path

here = path.abspath(path.dirname(__file__))

with codecs.open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with io.open("nwpc_workflow_log_model/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="nwpc-workflow-log-model",

    version=version,

    description="A database model for workflow log in NWPC.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/nwpc-oper/nwpc-workflow-log-model",

    author="perillaroc",
    author_email="perillaroc@gmail.com",

    license="GPLv3",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],

    keywords="nwpc workflow log model",

    packages=find_packages(exclude=["docs", "tests", "tool"]),

    install_requires=[
        "loguru",
        "mongoengine",
        "sqlalchemy",
        "transitions>=0.8.0",
        "pygraphviz",
        "nwpc-workflow-model>=0.5,<0.6"
    ],

    extras_require={
        "tool": ["click"],
        "test": ["pytest"],
        "cov": ["pytest-cov", "codecov"]
    },

    entry_points={}
)
