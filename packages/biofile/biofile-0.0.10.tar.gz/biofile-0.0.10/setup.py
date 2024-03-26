from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="biofile",
    version='0.0.10',
    author="Tiezheng Yuan",
    author_email="tiezhengyuan@hotmail.com",
    description="Process various file format for RNA-Seq data analysis",
    url = "https://github.com/Tiezhengyuan/bio_file",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "Bio",
        "biosequtils",
        "numpy",
        "pandas",
    ],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
