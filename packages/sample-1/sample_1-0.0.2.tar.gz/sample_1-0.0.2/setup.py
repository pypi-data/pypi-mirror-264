import pathlib
from setuptools import setup, find_packages

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="sample_1",
    version="0.0.2",
    description="A user-friendly wrapper for the Kite Connect library",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/AST-LW/kite_connect_lite",
    packages=find_packages(exclude=["venv", "tests"]),
    install_requires=["kiteconnect", "pandas"],
    include_package_data=True,
)
