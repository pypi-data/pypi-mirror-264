from setuptools import setup, find_packages

setup(
    name="rpc-solana-client",
    version="0.1.0",
    author="Tsunami43",
    author_email="tsucintosh@gmail.com",
    description="A async_client for interacting with Solana RPC HTTP endpoint.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tsunami43/RPC-Solana-API",
    packages=find_packages(),
    install_requires=[
        "httpx",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
