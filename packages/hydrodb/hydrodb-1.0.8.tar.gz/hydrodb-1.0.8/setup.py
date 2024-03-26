from setuptools import setup

__project__ = "hydrodb"
__version__ = "1.0.8"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

__description__ = readme
__packages__ = ["hydrodb"]
__author__ = "Caio Teixeira de Paula"
__contact_email__ = "caio.teixeira.paula@gmail.com"

__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]

__key_words__ = ["db", "data_base", "back-end"]

__requires__ = ["yaspin"]

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    author=__author__,
    author_email=__contact_email__,
    classifiers=__classifiers__,
    keywords=__key_words__,
    requires=__requires__,
    download_url="https://github.com/CaioTeixeiraDePaula/HydroDB/archive/refs/tags/v1.0.5.zip",
    long_description=readme,
    install_requires=["yaspin"]

)
