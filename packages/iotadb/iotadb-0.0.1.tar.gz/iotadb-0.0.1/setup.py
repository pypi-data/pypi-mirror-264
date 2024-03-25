from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_desc = f.read()

setup(
    name="iotadb",
    version="0.0.1",
    description="An easy-to-use, lightweight local embedding database.",
    package_dir={"": "iotadb"},
    packages=find_packages("iotadb"),
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/timothyckl/iota",
    author="timothyckl",
    author_email="timothy.ckl@outlook.com",
    license="MIT", 
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    install_requires=["numpy>=1.26.4", "sentence-transformers>=2.5.1"],
    extras_require={
        "dev": ["pytest>=8.1.1", "twine>=5.0.0"]
    },
    python_requires=">=3.11"
)
