# pyKinML: Package for training Neural Net Potential Energy Surfaces

## Description

This repository contains the code to train NNPESs and use those models with an ASE calculator.

### How to install

This package can be installed with pip or by cloning this repo and installing it locally.
First, make sure to have pytorch installed:

    https://pytorch.org/

This package relies on pytorch_scatter to sum the atomic contributions to energy. Ensure you have the proper version. Instructions for installing torch_scatter can be found at:

    https://github.com/rusty1s/pytorch_scatter


## Install with pip:
    pip install pykinml

### Clone from repo:
    git clone git@github.com:sandialabs/pykinml.git

We also highly recomend (required for force training) using the aevmod package for calculation of the aevs and their jacobians:
https://github.com/sandialabs/aevmod.git

For transition state optimization, we recomend Sella:
https://github.com/zadorlab/sella
