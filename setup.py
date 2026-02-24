from setuptools import setup, find_packages

setup(
    name="zahra",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kurigram",
        "motor",
        "py-tgcalls",
        "python-dotenv",
        "tgcrypto"
    ],
)
