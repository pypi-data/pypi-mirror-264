from setuptools import setup, find_packages

setup(
    name="GCNCharge",
    version="1.1.1",
    packages=find_packages(),
    description="A partial atomic charge of nanoporous materials predicter",
    author="Guobin Zhao",
    author_email="sxmzhaogb@gmai.com",
    url="https://github.com/sxm13/GCNCharges",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        'GCNCharge': ['*.json', '*.pkl', '*.pth'],
        'test': ['Cu-BTC.cif'],
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "numpy>=1.13.3",
        "pymatgen>=2018.6.11",
        "ase>=3.19",
        "tqdm>=4.15",
        "pandas>=0.20.3",
        "scikit-learn>=0.19.1",
        "joblib>= 0.13.2",
        "torch"
    ],
)
