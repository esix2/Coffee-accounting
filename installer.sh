#!/bin/sh
if [ ! -z "`which sudo`" ] ; then
        use_sudo=1
else
        use_sudo=0
fi

do_sudo() {
        msg=$1 ; shift
        if [ "$use_sudo" = 1 ] ; then
                sudo -p "$msg, please enter your password: " $*
        else
                if [ "`id -u`" != 0 ] ; then
                        echo "$msg, please enter root password..."
                fi
                su -c "$*"
        fi
}
if [ -z "`which python2.7`" ] ; then
        echo "You really need iselect for apt-iselect, installing..."
        do_sudo "Installing iselect" apt-get install python2.7
fi
if [ -z "`which pdflatex`" ] ; then
        echo "You really need iselect for apt-iselect, installing..."
        do_sudo "Installing iselect" apt-get install texlive
fi
pip install pandas==0.20.1
do_sudo "Installing openpyxl" pip install openpyxl==1.8.2
do_sudo "Installing numpy1.7.1" pip install numpy==1.7.1
do_sudo "Installing keyring10.3.2" pip install keyring==10.3.2
do_sudo "Installing getent" pip install getent==0.2
path=~/kitchen
echo "the default installation path is $path. Do you want to change it [y/N]?"
read key
case $key in
  y|Y|yes|Yes)
  echo 'Insert your desired path. It is highly recommended to install in your home directory:';
  read newpath;
  path=$newpath;
esac
mkdir $path;
cp -r src $path;
