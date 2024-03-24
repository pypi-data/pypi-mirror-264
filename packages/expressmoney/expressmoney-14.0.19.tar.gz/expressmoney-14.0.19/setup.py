"""
py setup.py sdist
twine upload dist/expressmoney-14.0.19.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='14.0.19',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('python-json-logger==2.0.4',),
    python_requires='>=3.7',
)
