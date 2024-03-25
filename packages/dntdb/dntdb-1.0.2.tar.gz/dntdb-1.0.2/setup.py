from setuptools import setup, find_packages
from glob import glob

with open("dntdb/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="dntdb",
    version="1.0.2",
    author="DNT",
    description="Update file so",
    long_description=open("dntdb/README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    data_files=[("dntdb", glob("dntdb/*.so"))],
)
