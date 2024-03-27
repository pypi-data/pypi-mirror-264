from setuptools import setup, find_packages

setup(
    name='tctk',
    version='0.1.3',
    packages=find_packages(where="/src"),
    url='https://github.com/nhgritctran/tctk',
    license='GPL-3.0',
    author='Tam Tran',
    author_email='tam.c.tran@outlook.com',
    description='A collection of mini tools.',
    install_requires=[
        "connectorx",
        "google-cloud-bigquery",
        "hail",
        "polars",
        "pyarrow",
        "tqdm"
    ]
)
