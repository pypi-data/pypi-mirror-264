from setuptools import setup

with open("./README.md", "r") as f:
    long_desc = f.read()

setup(
    name="iotadb",
    version="0.0.12",
    description="Minimal implementation of a local embedding database",
    packages=["iotadb"],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/timothyckl/iota",
    author="timothyckl",
    author_email="timothy.ckl@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "torch==2.2.1+cpu",
        "transformers==4.38.2",
        "tqdm==4.66.2",
        "numpy==1.26.4", 
        "scikit-learn==1.4.1.post1",
        "scipy==1.12.0",
        "nltk==3.8.1",
        "sentencepiece==0.2.0",
        "sentence-transformers==2.6.1"
    ],
    dependecy_links=[
        "https://download.pytorch.org/whl/torch_stable.html"
    ],
    extras_require={"dev": ["pytest", "twine"]},
    python_requires=">=3.8",
)
