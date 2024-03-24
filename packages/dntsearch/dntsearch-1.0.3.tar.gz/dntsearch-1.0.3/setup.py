from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()
setup(
    name="dntsearch",
    version="1.0.3",
    author="DNT",
    author_email="duongngocthien402@gmail.com",
    description="Search Engine",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
