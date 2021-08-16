from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='stupid-artnet',
      version='1.0',
      license='MIT',
      description='(Very) Simple Python library implementation of the Art-Net protocol',
      long_description=long_description,
      long_description_content_type="text/markdown",
	  url="https://github.com/cpvalente/stupidArtnet",
      packages=['lib'],
      zip_safe=False)