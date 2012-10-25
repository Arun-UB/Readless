Readless
========

An intelligent feed reader 

Setup
-----

To start off, make a blank directory and enter it

    mkdir Readless && cd Readless


Then clone this repository

    git clone https://github.com/ajy/Readless.git


Get all submodules(like the angularjs subrepo)

    git submodule init
    git submodule update


Create a Virtualenv

    virtualenv venv-Readless --distribute


To work within the new environment, you will need to activate it:

    source venv-Readless/bin/activate


This will change your prompt to include the project name.
(You must source the virtualenv environment for each terminal session where you wish to run your app.)

To exit the environment:

    deactivate


Use pip to install all required dependencies

    pip install -r requirements.txt

