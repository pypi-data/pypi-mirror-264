"""
./deploy.ps1
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='14.0.26',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('requests', 'python-json-logger==2.0.4', 'django-phonenumber-field[phonenumberslite]==5.2.0'),
    python_requires='>=3.7',
)
