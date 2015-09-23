# Digital Forensics Framework

![alt text](http://www.arxsys.fr/wp-content/uploads/2015/09/dff_logo_new_title_dark.png "Digital Forensics Framework")

DFF is an Open Source computer forensics platform built on top of a dedicated Application Programming Interface (API). DFF proposes an alternative to the aging digital forensics solutions used today. Designed for simple use and automation, DFF interface guides the user through the main steps of a digital investigation so it can be used by both professional and non-expert to quickly and easily conduct a digital investigation and perform incident response. 

DFF follows three main goals :

0. __Modularity__ In contrary to the monolithic model, the modular model is based on a core and many modules. This modular conception presents two advantages : it permits to improve rapidly the software and to split easily tasks for developers.
0. __Scriptability__ It is obvious that the ability to be scripted gives more flexibility to a tool, but it also enables automation and gives the possibility to extend features
0. __Genericity__ the project tries to remain Operating System agnostic. We want to help people where they are ! Letting them choose any Operating System to use DFF.

# Installation

## Packages

DFF can be installed with the package manager of your distribution

### Debian

#### Jessie

echo "deb http://repo.digital-forensic.org/debian jessie main" > /etc/apt/sources.list.d/arxsys.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7DC18D60
apt-get update
apt-get install dff

#### Stretch

echo "deb http://repo.digital-forensic.org/debian stretch main" > /etc/apt/sources.list.d/arxsys.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7DC18D60
apt-get update
apt-get install dff

### Ubuntu

#### Trusty

apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7DC18D60
add-apt-repository "deb http://repo.digital-forensic.org/ubuntu trusty main"
apt-get update
apt-get install dff


### Fedora, CentOS, OpenSuSE

yum-config-manager --add-repo http://www.cert.org/forensics/repository/
yum update --disableexcludes=all
yum install dff


## From source

### GNU/Linux

TODO
