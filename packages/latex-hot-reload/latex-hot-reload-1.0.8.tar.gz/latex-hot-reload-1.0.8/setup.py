from setuptools import setup, find_namespace_packages

setup(
    name="latex-hot-reload",
    version="1.0.8",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
