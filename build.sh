#!/usr/bin/env bash

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
SITE_PACKAGES=$(pipenv --venv)/lib/python3.6/site-packages
echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
echo "Do fresh install to make sure everything is there"
pipenv sync

# Get Dependencies
cd $SITE_PACKAGES
zip -r9 $DIR/package.zip *

# Get function Code
cd $DIR
zip -g package.zip lambda_function.py

# Remove unnecessary bloat
zip --delete package.zip "wheel*"
zip --delete package.zip "setup*"
zip --delete package.zip "easy*"
zip --delete package.zip "pip*"
zip --delete package.zip "boto*"
zip --delete package.zip "s3*"
zip --delete package.zip "docutils*"
zip --delete package.zip "future*"
zip --delete package.zip "pkg*"
zip --delete package.zip "six*"
