from setuptools import setup, find_packages
from os import path

dir = path.abspath(path.dirname(__file__))
with open(path.join(dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(name='unpywall',
      version='0.1.6',
      description='Interfacing the Unpaywall Database with Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/unpywall/unpaywall-python',
      download_url='',
      author='Nick Haupka, bganglia',
      author_email='nick.haupka@gmail.com, bganglia892@gmail.com',
      license='MIT',
      packages=find_packages(),
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
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3'
      ],
      zip_safe=False)
