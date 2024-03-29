__author__ = "Alex DeLorenzo"
from setuptools import setup
from pathlib import Path


NAME = "minimalsound"
VERSION = "0.1.0"
LICENSE = "LGPL-3.0"

DESC = "🔊 Play music and sounds in your Python scripts"

README = Path('README.md').read_text()


setup(
  name=NAME,
  version=VERSION,
  description=DESC,
  long_description=README,
  long_description_content_type="text/markdown",
  author=__author__,
  license=LICENSE,
  packages=[NAME],
  zip_safe=False,
  install_requires=['playsound', 'sniffio', 'boombox', 'anyio'],
  python_requires='>=3.6',
  include_package_data=True,
  package_data={'minimalsound': ['assets/*']},
)
