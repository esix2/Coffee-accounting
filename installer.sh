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
        echo "You really need python2.7 for apt-iselect, installing..."
        do_sudo "Installing python2.7" apt-get install python2.7
fi
if [ -z "`which pdflatex`" ] ; then
        echo "You really need texlive for apt-iselect, installing..."
        do_sudo "Installing latex" apt-get install texlive
fi
if [ -z "`which pip`" ] ; then
        echo "You really need pip for apt-iselect, installing..."
        do_sudo "Installing pip" sudo apt-get install python-pip
fi
#if [ -z "`which setuptools`" ] ; then
#        echo "You really need setuptools for apt-iselect, installing..."
#        do_sudo "Installing setuptools" sudo apt-get install python-setuptools
#fi
if [ -z "`which setuptools`" ] ; then
        echo "You really need setuptools for apt-iselect, installing..."
        do_sudo "Installing virtualenv" pip install virtualenv
fi

python2.7 -m virtualenv VirtualEnv
source VirtualEnv/bin/activate
do_sudo "Installing dependencies in virtual envirnoment" pip install -r requirements.txt

path=~/Coffee-accounting
echo "the default installation path is $path. Do you want to change it [y/N]?"
read key
case $key in
  y|Y|yes|Yes)
  echo 'Insert your desired path. It is highly recommended to install in your home directory:';
  read newpath;
  path=$newpath;
esac
mkdir $path;
cd ../
mv Coffee-accounting/ $path;
cd $path
