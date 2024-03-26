from setuptools import setup, find_packages

setup(
    name="python_runtime",
    version="24.3.27",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    author="Louie X. Walker",
    author_email="louiewalker.lw1@gmail.com",
    description="A middleware package to check for service expiration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
