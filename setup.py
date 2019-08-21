from setuptools import setup

PKG_NAME = 'xnat_eeg_upload'

setup(
    name=PKG_NAME,
    version=0.1,
    author='James T. Morrow',
    author_email='james.morrow@monash.edu',
    py_modules=['xnat_eeg_upload'],
    entry_points={
        'console_scripts': ['xnat-eeg-upload = xnat_eeg_upload:eeg_upload']},
    url='http://github.com/MonashBI/xnat_eeg_upload',
    license='The MIT License (MIT)',
    description=(
        'A simple script for uploading EEG data to XNAT.'),
    long_description=open('README.rst').read(),
    install_requires=['xnatutils>=0.5.3'],
    python_requires='>=3.4',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps."])
