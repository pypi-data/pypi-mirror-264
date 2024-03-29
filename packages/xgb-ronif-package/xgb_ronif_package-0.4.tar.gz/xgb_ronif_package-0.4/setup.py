from setuptools import setup, find_packages

setup(
    name='xgb_ronif_package',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'xgboost',
        'joblib'
    ],
)
