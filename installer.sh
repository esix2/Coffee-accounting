#!/bin/bash

trap exit INT

path=~/coffee-accounting
echo -n "The default installation path is $path. Do you want to change it? [y/N] "
read key
case $key in
    y|Y|yes|Yes)
        echo 'It is possible to install into your home directory. Insert your desired path:';
        read newpath;
        path=$newpath;
esac

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

echo "Checking for system dependencies..."
if [ -z "`which python2.7`" ] ; then
    echo "Need python2.7, enter root password to install or hit CTRL+c to quit:"
    do_sudo "Installing python2.7" apt-get install python2.7
fi
if [ -z "`which pdflatex`" ] ; then
    echo "Need texlive, enter root password to install or hit CTRL+c to quit:"
    do_sudo "Installing latex" apt-get install texlive
fi
if [ -z "`which pip`" ] ; then
    echo "Need pip, enter root password to install or hit CTRL+c to quit:"
    do_sudo "Installing pip" sudo apt-get install python-pip
fi
if [ -z "`which virtualenv`" ] ; then
    echo "Need virtualenv, enter root password to install or hit CTRL+c to quit:"
    do_sudo "Installing virtualenv" pip install virtualenv
fi

echo "Checking for python dependencies..."
echo -n "Using virtualenv to install python dependencies. Continue? [Y/n] "
read key
case $key in
    n|N|no|No) ;;
    *)
        python2.7 -m virtualenv ~/coffee-accounting/venv
        source ~/coffee-accounting/venv/bin/activate
        pip install -r requirements.txt ;;
esac

if [ $path != $PWD ] ; then
    echo "Install to $path..."
    cp coffee.sh $path
    cp -r python/ $path
    echo "Done."
else
    echo 'Warning: Source and destination are unique.'
fi

