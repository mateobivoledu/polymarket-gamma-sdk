from setuptools import setup, find_packages

setup(
    name="py-gamma-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ],
    author="Mateo Bivol",
    author_email="mateo.bivol@mail.utoronto.ca",
    description="Asynchronous Python SDK for Polymarket's Gamma API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mateo-bivol/polymarket-gamma-sdk",
    license="MIT",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
