XNAT EEG Upload
===============

A simple interactive script for uploading EEG/COG data to XNAT


Installation
------------

XNAT EEG Upload requires Python 3 with the ``pip3`` installed.

How you install Python 3 will depend on the system you are using and whether
there is another Python 3 already installed it on it or not. If Python 3 isn't
installed I would strongly recommend using a package manager such as

* Homebrew (http://brew.sh) - MacOS
* Chocolately (http://chocolatey.org) - Windows
* Apt/Yum/Apk/etc... - Linux

These Python versions should come with ``pip3`` already installed but if you don't
have it installed, it can be downloading https://bootstrap.pypa.io/get-pip.py and
running `python3 get-pip.py`.

Once pip3 is installed you can install the EEG upload by cloning this repository
with `git` (you can install git with one of the aforementioned package managers)
or downloading and unzipping somewhere sensible on your computer, then run::

    pip3 install -e <where-you-saved-the-cloned/downloaded-directory>


Running
-------

You run the script with the command::

    xnat-eeg-upload
    
(NB: if you are on Linux and installed without 'sudo' you will probably need to add $HOME/.local/bin
to your PATH variable)
