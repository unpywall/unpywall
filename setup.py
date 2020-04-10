from setuptools import setup
from os import path

dir = path.abspath(path.dirname(__file__))
with open(path.join(dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(name='unpywall',
      version='0.1.6',
      description='Interfacing the Unpaywall Database with Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/naustica/unpywall',
      download_url='',
      author='Nick Haupka',
      author_email='nick.haupka@gmail.com',
      license='MIT',
      packages=['unpywall'],
      keywords=['Unpaywall'],
      install_requires=[
        'pandas',
        'requests'
      ],
      extras_require={
       'dev': [
            'pytest',
            'pytest-cov',
            'coverage'
       ]
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
      ],
      zip_safe=False)
