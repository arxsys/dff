# Digital Forensics Framework

![Digital Forensics Framework](http://www.arxsys.fr/wp-content/uploads/2015/09/dff_logo_new_title_dark.png)

[![Build Status](https://scan.coverity.com/projects/dff/badge.svg)](https://scan.coverity.com/projects/dff)

DFF is an Open Source computer forensics platform built on top of a dedicated Application Programming Interface (API). DFF proposes an alternative to the aging digital forensics solutions used today. Designed for simple use and automation, DFF interface guides the user through the main steps of a digital investigation so it can be used by both professional and non-expert to quickly and easily conduct a digital investigation and perform incident response.

DFF follows three main goals :

0. __Modularity__ In contrary to the monolithic model, the modular model is based on a core and many modules. This modular conception presents two advantages : it permits to improve rapidly the software and to split easily tasks for developers.
0. __Scriptability__ It is obvious that the ability to be scripted gives more flexibility to a tool, but it also enables automation and gives the possibility to extend features
0. __Genericity__ the project tries to remain Operating System agnostic. We want to help people where they are ! Letting them choose any Operating System to use DFF.

Amongst supported features of DFF :

* Automated analysis
  * Mount partitions, file systems and extract files metadata and other usefull information in an automated way.
  * Generate an HTML report with System & User activity
* Direct devices reading support
* Supported forensic image file formats
  * AFF, E01, Ex01, L01, Lx01, dd, raw, bin, img
* Supported volumes & File systems with unallocated space, deleted items, slack space, ...
  * DOS, GPT, VMDK, Volume Shadow Copy, NTFS, HFS+, HFSX, EXT2, EXT3, EXT4, FAT12, FAT16, FAT32
* Embeded viewers for videos, images, pdf, text, office documents, registry, evt, evtx, sqlite, ...
* Outlook and Echange mailboxes (PAB, PST, OST)
* Metadata extraction 
  * Compound files (Word, Excel, Powerpoint, MSI, ...)
  * Windows Prefetch
  * Exif information
  * LNK
* Browser history
  * Firefox, Chrome, Opera
* System & Users activity
  * connected devices, user accounts, recent documents, installed software, network, ...
* Volatile memory analysis with graphical interface to Volatility
* Videos thumbnails generation
* Support for Sqlite, Windows Registry, Evt and Evtx
* Full Skype analysis (Sqlite and old DDB format)
* Timeline based on all gathered timestamps (file systems and metadata)
* Hashset supports with automatic "known bad", "known good" tagging
* Mount functionnality to access recovered files and folders from your local system
* In place carving
* ...

# Dependencies

Some optional dependencies are optional and are rarely packaged on GNU/Linux distrubition. If you need associated features, you will have to install them by yourself:

* The following dependencies must be installed before compilation:
  * [Libpff](https://github.com/libyal/libpff) to support Outlook & Exchange mailboxes
  * [Libewf](https://github.com/libyal/libewf) to support EnCase forensic containers
  * [Libvshadow](https://github.com/libyal/libvshadow) to support Volume Shadow Copy

* The following dependencies can be installed after compilation
  * [Pyregfi and reglookup](http://projects.sentinelchicken.org/reglookup/download/) to support Windows registry parsing
  * [Volatility](https://github.com/volatilityfoundation/volatility) to support volatile memory analyse
  * ["Pefile"](https://github.com/erocarrera/pefile) to enhance metadata extracted from recovered binary in volatile memory


# Install

## Packages

DFF can be installed with the package manager of your distribution

### Debian

#### Jessie

<pre>
echo "deb http://repo.digital-forensic.org/debian jessie main" > /etc/apt/sources.list.d/arxsys.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7DC18D60
apt-get update
apt-get install dff
</pre>

#### Stretch
<pre>
echo "deb http://repo.digital-forensic.org/debian stretch main" > /etc/apt/sources.list.d/arxsys.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7DC18D60
apt-get update
apt-get install dff
</pre>

### Ubuntu

#### Trusty
<pre>
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7DC18D60
add-apt-repository "deb http://repo.digital-forensic.org/ubuntu trusty main"
apt-get update
apt-get install dff
</pre>

### Fedora, CentOS, OpenSuSE
<pre>
yum-config-manager --add-repo http://www.cert.org/forensics/repository/
yum update --disableexcludes=all
yum install dff
</pre>

## From source

### GNU/Linux

#### Debian based distribution

<pre>
apt-get install cmake build-essential swig python-qt4 pyqt4-dev-tools qt4-dev-tools libicu-dev libtre-dev qt4-linguist-tools python-magic libfuse-dev libudev-dev libavformat-dev libavdevice-dev libavutil-dev libswscale-dev flex bison devscripts pkg-config autotools-dev automake autoconf autopoint zlib1g-dev libtool libssl-dev wget scons libtalloc-dev clamav
git clone https://github.com/arxsys/dff/
cd dff
git submodule init
git submodule update
mkdir build
cd build
cmake ..
make -j`getconf _NPROCESSORS_ONLN`
</pre>


# Pointers

Website: http://www.digital-forensic.org/

IRC: irc.freenode.net #digital-forensic

Twitter: @dfforg