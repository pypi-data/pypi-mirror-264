from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.12'''
DESCRIPTION = '''Some useful Bluestacks stuff'''

# Setting up
setup(
    name="getbstacksinfo",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/getbstacksinfo',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['ctypes_window_info', 'list_all_files_recursively', 'nodepsutils', 'pidconnectioninfos', 'regex', 'regex4numbers', 'reggisearch', 'tkkillablethreads'],
    keywords=['utils', 'Bluestacks'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['ctypes_window_info', 'list_all_files_recursively', 'nodepsutils', 'pidconnectioninfos', 'regex', 'regex4numbers', 'reggisearch', 'tkkillablethreads'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*