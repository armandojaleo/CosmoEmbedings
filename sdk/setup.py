from setuptools import setup, find_packages

setup(
    name="cosmicembeddings",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
        "transformers>=4.0.0",
        "torch>=1.8.0",
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "skyfield>=1.42",
        "ed25519>=1.5",
    ],
    entry_points={
        "console_scripts": [
            "cosmic=cosmicembeddings.cli:main",
        ],
    },
    author="CosmicEmbeddings Team",
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
