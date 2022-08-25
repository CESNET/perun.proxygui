from setuptools import setup, find_packages

setup(
    name="perun.proxygui",
    python_requires=">=3.9",
    url="https://github.com/CESNET/perun.proxygui",
    description="Module with gui for perun proxy",
    packages=find_packages(),
    install_requires=[
        "setuptools"
    ],
)
