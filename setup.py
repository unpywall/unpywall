from setuptools import setup

setup(name='unpywall',
      version='0.1',
      description='Interfacing the Unpaywall Database with Python',
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
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
      ],
      zip_safe=False)
