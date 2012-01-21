#!/bin/bash

# Create virtual environment
/usr/bin/virtualenv --no-site-packages orm_env
. orm_env/bin/activate

# Install fabric package
pip install fabric

# Deploy requirements packages
fab install_requirements