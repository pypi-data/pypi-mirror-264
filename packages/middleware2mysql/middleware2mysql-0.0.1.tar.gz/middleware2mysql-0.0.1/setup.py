from setuptools import setup, find_packages


setup(
    name='middleware2mysql',
    version='0.0.1',
    packages=find_packages(),
    author='hanhang',
    author_email='hanhang@360.com',
    description='use kafka and redis by mysql',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hanhang-han/mysqlplus_pkg',
    install_requires=[
        "aiomultiprocess>=0.9.0",
        "async-timeout",
        "dill>=0.3.8",
        "greenlet>=3.0.3",
        "multiprocess>=0.70.16",
        "mysql==0.0.3",
        "mysql-connector-python>=8.3.0",
        "mysqlclient>=2.2.4",
        "PyMySQL>=1.1.0",
        "SQLAlchemy>=2.0.28",
        "typing_extensions>=4.10.0"
    ]
)
