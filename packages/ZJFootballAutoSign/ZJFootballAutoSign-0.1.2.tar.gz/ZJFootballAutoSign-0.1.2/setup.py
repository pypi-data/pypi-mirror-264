from distutils.core import setup
from setuptools import find_packages

setup(name='ZJFootballAutoSign',
        version='0.1.2',
        packages=find_packages(),
        include_package_data=False,
        package_data={'data': []},
        install_requires = ['selenium'],
        description='A script used for automatically signing in on Zhejiang Professional Football Club\'s website.',
        author='konata321',
        author_email='megumi321@163.com',
        license='MIT',
        python_requires=">=3.6,<3.11",
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        ],
        )