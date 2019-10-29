#! /bin/sh
python3 setup.py clean 
python3 setup.py build 
python3 setup.py build install 
python3 setup.py sdist bdist_wheel 
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose