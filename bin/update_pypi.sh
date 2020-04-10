#!/bin/bash

cd ../unpywall
python setup.py sdist
twine upload dist/* 
