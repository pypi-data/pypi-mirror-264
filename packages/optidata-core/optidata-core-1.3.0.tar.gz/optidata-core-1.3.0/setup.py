from setuptools import setup
from setuptools.config.expand import find_packages

VERSION = '1.3.0'
DESCRIPTION = 'Paquete de Python para OptiData'
LONG_DESCRIPTION = 'Paquete para OptiData que contiene funcionalidades para realizar una Conciliación con Pandas y Vaex'

# Configurando
setup(
    name="optidata-core",
    version=VERSION,
    author="Gonzalo Torres Moya",
    author_email="<gtorres@optimisa.cl>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'optidata-core'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)