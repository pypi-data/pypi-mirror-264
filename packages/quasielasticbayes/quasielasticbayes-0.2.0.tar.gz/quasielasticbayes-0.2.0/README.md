# quasielasticbayes

This package provides a convenient set of Python wrappers
for a set of routines used to perform Bayesian analysis
on quasi-elastic neutron-scattering data.

## Setup

The simplest way to build the distribution is to use [conda](https://docs.conda.io/en/latest/miniconda.html) to create
a separate environment to build the distribution.

Create a minimal conda environment:

### Windows - Python 3.10

```sh
mamba env create -f qeb-dev-win-py310.yml
conda activate qeb-dev-py310
```

### Linux - Python 3.10

```sh
mamba env create -f qeb-dev-linux-py310.yml
conda activate qeb-dev-py310
```

### Windows - Python 3.8

We currently rely on an external fortran compiler, `tdm64-gcc 4.6.1`, as the current code is sensitive
to the compiler version. To install:

- Download [tdm64-gcc-4.6.1.exe](https://sourceforge.net/projects/tdm-gcc/files/TDM-GCC%20Installer/Previous/1.1006.0/tdm64-gcc-4.6.1.exe/download) and install it to ``C:\MinGW64``
- Download [gcc-4.6.1-tdm64-1-fortran.zip](https://sourceforge.net/projects/tdm-gcc/files/TDM-GCC%20Old%20Releases/TDM-GCC%204.6%20series/4.6.1-tdm64-1/gcc-4.6.1-tdm64-1-fortran.zip/download)
- Right-click on ``gcc-4.6.1-tdm64-1-fortran.zip``, select "Extract All" and enter the location as ``C:\MinGW64``
- Add ``C:\MinGW64\bin`` to your ``PATH`` environment variable ([instructions here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/))
- Restart any terminal or powershell instances to capture the new environment variable settings

Then create a developer conda environment:

```sh
mamba env create -f qeb-dev-win-py38.yml
conda activate qeb-dev-py38
```

### Linux - Python 3.8

```sh
mamba env create -f qeb-dev-linux-py38.yml
conda activate qeb-dev-py38
```

## Build and Test

From the root of this repository:

To build a wheel, run

```sh
python setup.py bdist_wheel
```

To install the wheel, run

```sh
pip install --force-reinstall dist/quasielasticbayes-0.2.0-cp310-cp310-*.whl
```

To run the tests

```sh
pytest quasielasticbayes/test
```

## Building for PyPi

If this is your first time interacting with PyPi then please see [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) for instructions of how to setup accounts and API tokens. 

Once built the wheel can be uploaded using twine:

```
twine upload ./dist/name_of_wheel
```

### Linux Notes

Linux wheels require a docker image to produce a `manylinux2010` wheel. For more details see this blog https://uwekorn.com/2019/09/15/how-we-build-apache-arrows-manylinux-wheels.html

### macOS Notes

Unfortunately we cannot avoid a dynamic link to libquadmath on OSX. This appears to be a licencing issue with GCC and the conda gfortran package doesn't include the static version of quadmath.
So in order to use this package you'll need to have a system install of gfortran. We're not the only ones with this issue, e.g. https://github.com/aburrell/apexpy/issues/69 
