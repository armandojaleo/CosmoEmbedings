from setuptools import setup, find_packages

setup(
    name="cosmicembeddings",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "transformers>=4.15.0",
        "torch>=1.10.0",
        
        # Embedding models
        "sentence-transformers>=2.2.2",
        
        # Cryptography
        "ed25519>=1.5",
        
        # Astronomy
        "skyfield>=1.42",
        
        # Utilities
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "tqdm>=4.62.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "flake8>=3.9.2",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "cosmicembeddings=cosmicembeddings.cli:main",
            "cosmicembeddings-test=run_tests:main",
        ],
    },
    author="CosmoEmbeddings Team",
    author_email="team@cosmicembeddings.org",
    description="A decentralized semantic network for AIs built on embeddings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cosmicembeddings/sdk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
