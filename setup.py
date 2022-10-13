from setuptools import setup, find_packages

setup(
    name="perun.proxygui",
    python_requires=">=3.9",
    url="https://github.com/CESNET/perun.proxygui",
    description="Module with gui for perun proxy",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "SATOSA==8.0.1",
        "PyYAML>=6.0<7",
        "Flask>=2.2.2<3",
        "jwcrypto>=1.3.1<2",
        "Flask-Babel>=2.0.0<3",
    ],
)
