from setuptools import setup, find_packages

setup(
    name='xgb_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'xgboost',
        'joblib'
    ],
)
