#!/bin/bash

VIRT_ENV_HOME=orm_env

# Delete previously virtualenv home
if [ -d $VIRT_ENV_HOME ]; then
    rm -rf $VIRT_ENV_HOME
fi

# Create virtual environment
/usr/bin/virtualenv --no-site-packages orm_env
. $VIRT_ENV_HOME/bin/activate

# Install fabric package
pip install --quiet fabric
#pip install --quiet nose
#pip install --quiet ./
python setup.py develop

# Deploy requirements packages
fab install_req -H localhost

# Run unittests and coverage them
coverage erase
coverage run orm/tests/run.py --with-xunit
coverage xml

# Pep8 and Pylint violations
pep8 --repeat --ignore=E501,W391 orm | perl -ple 's/: ([WE]\d+)/: [$1]/' > reports/pylint.report
pylint --rcfile pylint.rc orm/*.py >> reports/pylint.report


echo "Jenkins script complete"