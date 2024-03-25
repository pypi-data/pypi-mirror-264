on anaconda/ubuntu:
pip install "/mnt/e/PhD/UNIL/Python_Programs/Tnseeker/dist/tnseeker-1.0.5-py3-none-any.whl"

To make wheel
on windows powersheel (on correct directory):
python setup.py sdist bdist_wheel

To upload to PyPI:
twine upload dist/*
username: afombravo