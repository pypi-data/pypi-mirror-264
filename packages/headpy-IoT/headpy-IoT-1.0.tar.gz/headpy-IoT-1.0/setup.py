from setuptools import setup, find_packages

setup (
    name='headpy-IoT',
    version='1.0',
    author='Dragos Lazea',
    author_email='dragos.lazea@cs.utcluj.ro',
    description='Anomaly detection framwork for HE IoT data',
    packages=find_packages(),
    license='GPL-3',   
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.8',
)