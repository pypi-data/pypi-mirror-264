from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

setup(
    name="calculos_financeiros",
    version="0.0.1",
    author="Windlin",
    description="Calculos de operações financeiras",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=find_packages(),
    install_requires = None,
    python_requires='>=3.8',
)