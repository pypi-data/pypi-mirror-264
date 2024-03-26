# Installation 

## Environment setup 

This section covers the setup of the environment used for running the library. Please make sure that you follow the instructions in the given order. 

:::{important}
If you are a developer just set up the conda environment as below and follow with the [developer install](#developer-install).
:::

1. Install python version 3.12. It is recommended to install [anaconda](https://www.anaconda.com/download) or [miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html). After doing so, open the command prompt and follow the next steps.
   - Create a new environment with : 
   ```bash
    conda create --name pycfs python=3.12
    ```
   - Switch to new environment with : 
    ```bash
    conda activate pycfs
    ```
2. Install *pyCFS* 
   - If you are using conda as suggested just run :
    ```bash
    python -m pip install --upgrade pycfs
    ```
   - If you are using your system python :
    ```bash
    pip install --upgrade pycfs
    ```

## Developer install 

First you will need to clone the repository and `cd` into the repository root. As a developer you will need to install 
a few dependencies more than what is needed to just use the package. 

1. Install the requirements by running : 
   ```bash
   python -m pip install -r requirements/dev.txt
   ```
2. To install the package make sure you're in the root directory. If you are 
using an anaconda distribution just run : 
```
$ python -m pip install -e .
```
the `-e` flag (editable install) applies the changes you make while developing directly to the package so that you can easily test it while developing in this source directory.

3. If you are using the system python run : 
```
pip3 install -r requirements/dev.txt
pip3 install -e .
```
This will install the required packages and then the `pyCFS` package itself.