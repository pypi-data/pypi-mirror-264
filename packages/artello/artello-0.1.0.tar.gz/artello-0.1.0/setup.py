from setuptools import setup, find_packages

setup(
    name="artello",
    version="0.1.0",
    author="Seetam Divkar",
    author_email="sup@artello.org",
    description="A simple package for creating nano LLMs with PyTorch.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seetam-cto/artello",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
