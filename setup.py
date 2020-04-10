from setuptools import setup

setup(name='unpywall',
      version='0.1',
      description='',
      url='https://github.com/naustica/unpywall',
      author='Nick Haupka',
      author_email='nick.haupka@gmail.com',
      license='MIT',
      packages=['unpywall'],
      install_requires=[
        'pandas',
        'requests'
      ],
      zip_safe=False)
