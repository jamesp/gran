# This file allows the installation of gran as a python library 'gran'
# Suggested installation procedure:
# 		$ git clone https://github.com/jamesp/gran
# 		$ cd gran
#		$ pip install -e .
# This installs the package in *development mode* i.e. any changes you make to these files
# or any additional files you add will be immediately available.
# In a new python console, from any directory, you can now use the gran code:
# 		>>> from gran import util
#		>>> d = gran.util.resample_latlon(...)
#

from distutils.core import setup

setup(name='gran',
      version='0.1',
      description='GCM run analysis tools',
      author='James Penn',
      url='https://github.com/jamesp/gran',
      packages=['gran'],
      install_requires=[
        'numpy',
        'xarray',
        'scipy'
      ]
     )