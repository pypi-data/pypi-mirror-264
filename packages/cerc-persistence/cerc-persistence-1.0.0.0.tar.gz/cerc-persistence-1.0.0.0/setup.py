import glob
import pathlib
from distutils.util import convert_path

from setuptools import setup

with pathlib.Path('requirements.txt').open() as r:
  install_requires = [
    str(requirement).replace('\n', '')
    for requirement
    in r.readlines()
  ]
install_requires.append('setuptools')

main_ns = {}
version = convert_path('cerc_persistence/version.py')
with open(version) as f:
  exec(f.read(), main_ns)

setup(
  name='cerc-persistence',
  version=main_ns['__version__'],
  description="",
  long_description="",
  classifiers=[
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],
  include_package_data=True,
  packages=[
    'cerc_persistence',
    'cerc_persistence.models',
    'cerc_persistence.repositories'
  ],
  setup_requires=install_requires,
  install_requires=install_requires,
  data_files=[
    ('cerc_persistence', glob.glob('requirements.txt')),
  ],
)
