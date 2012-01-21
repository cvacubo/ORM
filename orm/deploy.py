#import fabric
from fabric.operations import sudo

#@fabric.roles('services')
#def services_deploy():
#    """ Deploy services """


def install_requirements():
    """ Install required packages"""
    sudo("pip install sqlalchemy")
    sudo("pip install pyramid")
    sudo("pip install transaction")
    sudo("pip install pyramid_tm")
    sudo("pip install pyramid_debugtoolbar")
    sudo("pip install zope.sqlalchemy")
    sudo("pip install PasteScript")