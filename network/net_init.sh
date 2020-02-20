#!/bin/sh
#Download ns-3.27

wget https://www.nsnam.org/releases/ns-allinone-3.29.tar.bz2
tar xvf ns-allinone*

sudo apt-get install gcc g++ python python3 python3-dev -y
sudo apt-get install python3-setuptools git mercurial -y 
sudo apt-get install qt5-default mercurial -y
sudo apt-get install gir1.2-goocanvas-2.0 python-gi python-gi-cairo python-pygraphviz python3-gi python3-gi-cairo python3-pygraphviz gir1.2-gtk-3.0 ipython ipython3 -y
sudo apt-get install openmpi-bin openmpi-common openmpi-doc libopenmpi-dev -y
sudo apt-get install autoconf cvs bzr unrar -y
sudo apt-get install gdb valgrind -y
sudo apt-get install uncrustify -y
sudo apt-get install doxygen graphviz imagemagick -y
sudo apt-get install texlive texlive-extra-utils texlive-latex-extra texlive-font-utils texlive-lang-portuguese dvipng latexmk -y
sudo apt-get install python3-sphinx dia -y
sudo apt-get install gsl-bin libgsl-dev libgsl23 libgslcblas0 -y
sudo apt-get install tcpdump -y
sudo apt-get install sqlite sqlite3 libsqlite3-dev -y 
sudo apt-get install libxml2 libxml2-dev -y
sudo apt-get install cmake libc6-dev libc6-dev-i386 libclang-6.0-dev llvm-6.0-dev automake -y
pip install cxxfilt
sudo apt-get install libgtk2.0-0 libgtk2.0-dev -y
sudo apt-get install vtun lxc uml-utilities -y
sudo apt-get install libboost-signals-dev libboost-filesystem-dev -y


#install libzmq libraries
sudo apt-get install libzmq5 libzmq3-dev libczmq-dev libczmq4 libxml2 libxml2-dev

#for gui
sudo apt-get install python-qt4
sudo apt install xterm
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module


HOME_DIR=$(pwd)
echo $HOME_DIR
NS3_HOME=$HOME_DIR/ns-allinone-3.29/ns-3.29
PATCH_PATH=$HOME_DIR/patches

#cd $NS3_HOME
ls -lrt
#patch the wscript file
cp $NS3_HOME/wscript $NS3_HOME/wscript_original
#cp $PATCH_PATH/wscript.patch .
patch $NS3_HOME/wscript -i $PATCH_PATH/wscript.patch -o $NS3_HOME/wscript_out
mv $NS3_HOME/wscript_out $NS3_HOME/wscript

#patch other files
cp $NS3_HOME/src/applications/model/packet-sink.h $NS3_HOME/src/applications/model/packet-sink.h_original
patch $NS3_HOME/src/applications/model/packet-sink.h -i $PATCH_PATH/packet-sink.h.patch  -o $NS3_HOME/src/applications/model/packet-sink.h_out
mv $NS3_HOME/src/applications/model/packet-sink.h_out $NS3_HOME/src/applications/model/packet-sink.h

#cp $NS3_HOME/src/mobility/model/constant-position-mobility-model.h $NS3_HOME/src/mobility/model/constant-position-mobility-model.h_original
#patch $NS3_HOME/src/mobility/model/constant-position-mobility-model.h -i $PATCH_PATH/constant-position-mobility-model.h.patch -o $NS3_HOME/src/mobility/model/constant-position-mobility-model.h_out
#mv $NS3_HOME/src/mobility/model/constant-position-mobility-model.h_out $NS3_HOME/src/mobility/model/constant-position-mobility-model.h


#Configure and build ns-3
cd $NS3_HOME
./waf configure --enable-examples --enable-tests
./waf

#Copy the uav-sim code to ns-3 scratch folder
cp -r $HOME_DIR/uav-net-sim $NS3_HOME/scratch/
cp $HOME_DIR/config.xml $NS3_HOME/
sudo chmod 777 $NS3_HOME/config.xml

