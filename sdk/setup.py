from setuptools import setup, find_packages

setup(
    name="cosmicembeddings",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "skyfield",
        "ed25519",
    ],
    entry_points={
        "console_scripts": [
            "cosmicembeddings=cosmicembeddings.cli:main"
        ]
    },
)
