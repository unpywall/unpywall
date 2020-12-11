from setuptools import setup
from os import path

dir = path.abspath(path.dirname(__file__))
with open(path.join(dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(name='unpywall',
      version='0.2',
      description='Interfacing the Unpaywall Database with Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/unpywall/unpywall',
      author='Nick Haupka, bganglia',
      author_email='nick.haupka@gmail.com, bganglia892@gmail.com',
      license='MIT',
      packages=['unpywall'],
      keywords=['Unpaywall', 'Open Access', 'full text'],
      project_urls={
        'Documentation': 'https://unpywall.readthedocs.io/en/latest/',
        'Source': 'https://github.com/unpywall/unpywall',
        'Tracker': 'https://github.com/unpywall/unpywall/issues'
      },
      install_requires=[
        'pandas',
        'requests'
      ],
      extras_require={
       'dev': [
           'pytest',
           'coverage',
           'pytest-cov',
           'sphinx',
           'alabaster'
       ]
      },
      entry_points={
        'console_scripts': [
            'unpywall = unpywall.__main__:main'
        ]
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
      ],
      zip_safe=False)
