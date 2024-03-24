from setuptools import setup, find_packages

setup(name='coderadar',
      version='0.5.0',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['coderadar=coderadar.__main__:main'],
          }
     )
