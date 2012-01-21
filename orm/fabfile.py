#import fabric
from fabric.operations import sudo

#@fabric.roles('services')
#def services_deploy():
#    """ Deploy services """


def install_req():
    """ Install required packages"""
    print "Installing requirements"