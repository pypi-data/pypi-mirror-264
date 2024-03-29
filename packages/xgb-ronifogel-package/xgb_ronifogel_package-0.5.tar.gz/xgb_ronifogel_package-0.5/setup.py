from setuptools import setup, find_packages

setup(
    name='xgb_ronifogel_package',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'xgboost',
        'joblib'
    ],
)
