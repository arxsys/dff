#!/bin/sh

echo "Installing mandatory tools and libraries"
apt-get install git cmake build-essential debhelper fakeroot autotools-dev devscripts lintian diffutils patchutils swig python-all-dev python-qt4 pyqt4-dev-tools qt4-dev-tools libicu-dev libtre-dev qt4-linguist-tools libfuse-dev libudev-dev libavformat-dev libavdevice-dev libavutil-dev libswscale-dev flex bison devscripts pkg-config autotools-dev automake autoconf autopoint zlib1g-dev libtool libssl-dev wget scons libtalloc-dev libarchive-dev clamav-daemon python-pyclamd python-uno

arch=`uname -m`
if [ $arch = "i686" ]
then
    arch=i386;
else
    arch=amd64;
fi

distribution=`lsb_release -s -i`
codename=`lsb_release -s -c`
basedir=`pwd`

echo "Building DFF and dependencies for $arch platform"

echo "Building libbfio"
git clone https://github.com/libyal/libbfio.git
cd libbfio/
./synclibs.sh
./autogen.sh
./configure
cp -r dpkg/ debian
sed -i "s/\()\)/~$distribution~$codename\1/" debian/changelog
dpkg-buildpackage
cd ..
dpkg -i $basedir/libbfio_*_*$arch.deb
dpkg -i $basedir/libbfio-dev*$arch*.deb

echo "Building libpff"
git clone https://github.com/libyal/libpff.git
cd libpff/
./synclibs.sh
./autogen.sh
./configure
dpkg-buildpackage
cp -r dpkg/ debian
sed -i "s/\()\)/~$distribution~$codename\1/" debian/changelog
dpkg-buildpackage
cd ..
dpkg -i $basedir/libpff_*_*$arch.deb
dpkg -i $basedir/libpff-dev*$arch.deb

echo "Building libewf"
git clone https://github.com/libyal/libewf.git
cd libewf/
./synclibs.sh
sed -i '/ewftools/d' Makefile.am
sed -i '/ewftools/d' configure.ac
./autogen.sh
./configure
cp -r dpkg/ debian
sed -i "s/\()\)/~$distribution~$codename\1/" debian/changelog
sed -i '/libewf-tools/d' debian/rules
dpkg-buildpackage
cd ..
dpkg -i $basedir/libewf_*_*$arch.deb
dpkg -i $basedir/libewf-dev*$arch.deb

echo "Building libvshadow"
git clone https://github.com/libyal/libvshadow.git
cd libvshadow/
./synclibs.sh
./autogen.sh
./configure
cp -r dpkg/ debian
sed -i "s/\()\)/~$distribution~$codename\1/" debian/changelog
dpkg-buildpackage
cd ..
dpkg -i $basedir/libvshadow_*_*$arch.deb
dpkg -i $basedir/libvshadow-dev*$arch.deb

echo "Building libbde"
git clone https://github.com/libyal/libbde.git
cd libbde/
./synclibs.sh
./autogen.sh
./configure
cp -r dpkg/ debian
sed -i "s/\()\)/~$distribution~$codename\1/" debian/changelog
dpkg-buildpackage
cd ..
dpkg -i $basedir/libbde_*_*$arch.deb
dpkg -i $basedir/libbde-dev*$arch.deb

echo "Building volatility"
cd volatility/
./build.sh

echo "Building pefile"
cd ../pefile/
./build.sh

echo "Building pyregfi"
cd ../pyregfi/
./build.sh

#echo "Building DFF Community Edition"
#cd ../dff-ce/
#./build.sh

echo "Building DFF Professional Edition"
cd ../dff-pro/
./build.sh

#echo "Building DFF Case Edition"
#echo ../dff-case
#./build.sh
