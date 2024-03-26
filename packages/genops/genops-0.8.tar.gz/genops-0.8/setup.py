from setuptools import setup, find_packages

setup(
    name="genops",
    version="0.8",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Ramsay Brown",
    author_email="ramsay@usemissioncontrol.com",
    description="Connect your python application to Mission Control's GenOps platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/airesponsibility/genops-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
