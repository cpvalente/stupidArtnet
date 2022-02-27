from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='stupidArtnet',
      author='cpvalente',
      version='1.3.0',
      license='MIT',
      description='(Very) Simple implementation of the Art-Net protocol',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/cpvalente/stupidArtnet',
      project_urls={
          'Bug Tracker': 'https://github.com/cpvalente/stupidArtnet/issues',
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      keywords=['LIGHTING', 'DMX', 'LIGHTING CONTROL'],
      packages=['stupidArtnet'],
      package_data={'stupidArtnet': ['examples/*']},
      python_requires=">=3.6")
