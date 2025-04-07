from setuptools import setup, find_packages

setup(
    name="cosmoembeddings",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        
        # Embedding models
        "sentence-transformers>=2.2.0",
        
        # Cryptography
        "pynacl>=1.5.0",
        
        # Astronomy
        "skyfield>=1.42",
        
        # Utilities
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "tqdm>=4.62.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.1",
            "black>=21.9b0",
            "flake8>=3.9.2",
            "mypy>=0.910"
        ]
    },
    entry_points={
        "console_scripts": [
            "cosmoembeddings=cosmoembeddings.cli:main",
            "cosmoembeddings-test=cosmoembeddings.example_usage:main"
        ]
    },
    author="Armando Jaleo",
    author_email="armandojaleo@gmail.com",
    description="CosmoEmbeddings SDK for creating and validating knowledge blocks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/armandojaleo/CosmoEmbeddings",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires=">=3.8",
)
